"""
Core del Backend (FastAPI + Gemini AI).
Este es el cerebro de la aplicación.
- Configura e inicializa la API con FastAPI.
- Gestiona la conexión con Google Firestore y Gemini AI.
- Define el "Sistema Operativo" del mesero virtual 'Pepe' (prompts, herramientas).
- Maneja el endpoint principal /chat, coordinando memoria, lógica de negocio (precios, tiempos),
  persistencia de datos y respuesta generativa.
"""
import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional
from dotenv import load_dotenv
from google.cloud import firestore
from datetime import datetime, timedelta, timezone
import uuid
import asyncio
import json

# Importamos modelos actualizados
from models import Order, OrderItem, OrderStatus, ChatMessage

# --- CONFIGURACIÓN ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    raise ValueError("FATAL: Falta GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

try:
    db = firestore.Client(project=PROJECT_ID)
    print(f"✅ Conectado a Firestore: {db.project}")
except Exception as e:
    print(f"⚠️ Error Firestore: {e}")
    db = None

# --- MENU CACHE ---
MENU_CACHE = {}

def cargar_menu_cache():
    """Carga el menú desde Firestore a memoria."""
    global MENU_CACHE
    if not db:
        return
    try:
        docs = db.collection('menu').where(filter=firestore.FieldFilter("disponible", "==", True)).stream()
        for doc in docs:
            data = doc.to_dict()
            # Normalizamos la llave para búsqueda más fácil (ej. "latte", "bagel")
            # Usaremos el nombre como llave aproximada para startswith o exact match
            # O mejor, guardamos un dict con el ID y otro con nombres para búsqueda
            # Simplificación: Usaremos el nombre exacto como key principal, y tokenizada para búsqueda
            MENU_CACHE[data['nombre'].lower()] = data
            # También guardamos por ID por si acaso
            MENU_CACHE[doc.id] = data
        print(f"🍽️ Menú cargado: {len(MENU_CACHE)} items en cache.")
    except Exception as e:
        print(f"❌ Error cargando menú: {e}")

# Cargar al inicio
cargar_menu_cache()

def buscar_en_menu(nombre_buscado: str):
    """Busca un producto en el cache del menú."""
    nombre_buscado = nombre_buscado.lower()
    # 1. Búsqueda exacta
    if nombre_buscado in MENU_CACHE:
        return MENU_CACHE[nombre_buscado]
    
    # 2. Búsqueda parcial (contiene)
    for key, data in MENU_CACHE.items():
        if nombre_buscado in key:
            return data
    
    return None

# --- UTILS ---
def recursive_to_native(d):
    if hasattr(d, 'items'):
        return {k: recursive_to_native(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)) or (hasattr(d, '__iter__') and not isinstance(d, (str, bytes))):
        return [recursive_to_native(x) for x in d]
    return d

# --- TOOLS ---
def interpretar_orden(items: List[Dict[str, Any]]):
    """Agrega items a la orden. SI el usuario da una hora específica, inclúyela en notas."""
    return items

def cancelar_orden(razon: str):
    """Cancela la orden pendiente actual si existe."""
    return razon

tools_list = [interpretar_orden, cancelar_orden]

# --- SYSTEM INSTRUCTION (DINAMICO) ---
# Construimos la lista de productos y precios para el prompt
menu_prompt_list = []
for key, item in MENU_CACHE.items():
    # Solo agregamos entradas únicas (evitar duplicados por id/nombre)
    if 'nombre' in item: 
        entry = f"- {item['nombre']}: ${item['precio']} (Prep: {item.get('tiempo_prep', 5)}min)"
        if entry not in menu_prompt_list:
            menu_prompt_list.append(entry)

menu_text_block = "\n".join(set(menu_prompt_list))

instruccion_sistema = f"""
### ROL
Eres 'Pepe', el mesero digital de la cafetería 'Justicia y Café'.
Tu tono es amable, coloquial (mexicano neutro) y eficiente.

### MENÚ DISPONIBLE (PRECIOS REALES)
{menu_text_block}

### OBJETIVO
Gestionar la toma de pedidos, dudas y cancelaciones de los clientes mediante el uso estricto de herramientas.

### DIRECTRICES DE COMPORTAMIENTO (JSON)
{{
  "personalidad": {{
    "tono": "Amigable, servicial, proactivo",
    "estilo": "Breve y directo. Evita bloques de texto largos."
  }},
  "reglas_negocio": {{
    "precios": "Usa los precios del menú. Si no está en menú, di que no tenemos eso.",
    "confirmacion": "Siempre confirma lo que entendiste antes de procesar.",
    "cierre": "Siempre pregunta '¿Algo más?' o '¿Todo bien?' al final."
  }},
  "manejo_herramientas": {{
    "interpretar_orden": "USAR CUANDO: El cliente pide alimentos o bebidas. INCLUSO si es un item adicional ('y también una dona').",
    "cancelar_orden": "USAR CUANDO: El cliente explícitamente pide cancelar, borrar o dice que se equivocó en el pedido anterior."
  }}
}}

### FORMATO DE RESPUESTA (IMPORTANTE)
Si tu respuesta es solo texto (sin llamar a una tool), PUEDES devolver una lista JSON de strings para simular mensajes de WhatsApp separados.
Ejemplo válido: ["¡Claro que sí!", "¿De qué sabor quieres tu dona?"]
"""

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=tools_list,
    system_instruction=instruccion_sistema
)

app = FastAPI()

class ChatRequest(BaseModel):
    mensaje: str
    telefono: str

# --- GESTOR DE MEMORIA ---
async def obtener_historial(telefono: str, limit: int = 10):
    if not db:
        return []
    try:
        mensajes_ref = db.collection('clientes').document(telefono).collection('chat_history')
        query = mensajes_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        historial_gemini = []
        msgs = list(docs)[::-1]
        for doc in msgs:
            datos = doc.to_dict()
            role = "user" if datos['role'] == "user" else "model"
            historial_gemini.append({"role": role, "parts": [datos['content']]})
        return historial_gemini
    except Exception:
        return []

async def guardar_mensaje(telefono: str, role: str, content: str):
    if not db:
        return
    try:
        mensajes_ref = db.collection('clientes').document(telefono).collection('chat_history')
        nuevo_msg = ChatMessage(role=role, content=content)
        mensajes_ref.add(nuevo_msg.to_firestore())
    except Exception as e:
        print(f"Error guardando mensaje: {e}")

# --- GLOBALES PARA DEBOUNCE BUFFER ---
message_buffer: Dict[str, List[str]] = {}
latest_request_token: Dict[str, str] = {}

# --- ENDPOINT CHAT ---
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # LÓGICA DE DEBOUNCE / BUFFER
        phone = request.telefono
        if phone not in message_buffer:
            message_buffer[phone] = []
        
        # 1. Agregar mensaje al buffer
        message_buffer[phone].append(request.mensaje)
        
        # 2. Generar token único para esta solicitud
        current_token = str(uuid.uuid4())
        latest_request_token[phone] = current_token
        
        # 3. Esperar tiempo de agrupación (Buffer)
        await asyncio.sleep(2.0)
        
        # 4. Verificar si sigue siendo la última solicitud
        if latest_request_token.get(phone) != current_token:
            # Si el token cambió, significa que llegó otro mensaje después.
            # Esta solicitud se descarta (será procesada por la siguiente).
            return {"tipo": "ignorar", "mensaje": "Mensaje agrupado."}
        
        # 5. Si es la última, unificamos y procesamos
        full_message = " ".join(message_buffer[phone])
        message_buffer[phone] = [] # Limpiar buffer
        
        # --- PROCESAMIENTO GEMINI (Usando full_message) ---
        
        # 1. Recuperar Memoria
        historial = await obtener_historial(request.telefono)

        # 2. Iniciar Chat con Memoria
        chat_session = model.start_chat(history=historial, enable_automatic_function_calling=False)
        
        # 3. Guardar mensaje usuario (El unificado)
        await guardar_mensaje(request.telefono, "user", full_message)
        
        # 4. Enviar a Gemini
        response = await chat_session.send_message_async(full_message)
        
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            
            # CASO A: ORDEN / AGREGAR ITEMS
            if part.function_call and part.function_call.name == 'interpretar_orden':
                args_native = recursive_to_native(part.function_call.args)
                raw_items = args_native.get('items', [])
                
                # Convertir input a objetos OrderItem (con cálculo de costos y tiempos reales)
                new_order_items = []
                total_prep_time_items = 0
                
                for item_data in raw_items:
                    nombre = item_data.get('nombre_producto', 'Item')
                    cantidad = int(item_data.get('cantidad', 1))
                    
                    # --- BÚSQUEDA EN MENU REAL ---
                    menu_item = buscar_en_menu(nombre)
                    if menu_item:
                        precio = float(menu_item.get('precio', 50.0))
                        tiempo_prep_unit = int(menu_item.get('tiempo_prep', 5))
                    else:
                        precio = float(item_data.get('precio_unitario', 50.0))
                        tiempo_prep_unit = 5 # Default 5 min si no está en menú

                    costo_estimado = precio * 0.30
                    total_prep_time_items += (tiempo_prep_unit * cantidad)
                    
                    obj_item = OrderItem(
                        nombre_producto=nombre,
                        cantidad=cantidad,
                        precio_unitario=precio,
                        costo_unitario=costo_estimado,
                        modificadores_seleccionados=item_data.get('modificadores_seleccionados', []),
                        notas_especiales=item_data.get('notas_especiales')
                    )
                    new_order_items.append(obj_item)

                # Cálculo de Tiempos
                buffer_tiempo = 5 # minutos extra
                tiempo_prep_total = total_prep_time_items + buffer_tiempo
                
                # LÓGICA DE COMANDA ABIERTA
                orden_existente_doc = None
                if db:
                    query = db.collection('pedidos').where(filter=firestore.FieldFilter("id_cliente", "==", request.telefono))\
                                                    .where(filter=firestore.FieldFilter("estado", "==", "pendiente"))\
                                                    .limit(1)
                    docs = list(query.stream())
                    if docs:
                        orden_existente_doc = docs[0]

                if orden_existente_doc:
                    # -- ACTUALIZAR ORDEN EXISTENTE --
                    data_existente = orden_existente_doc.to_dict()
                    items_actuales = data_existente.get('items', [])
                    
                    # Convertimos los nuevos a dict y los sumamos
                    nuevos_items_dicts = [item.to_firestore() for item in new_order_items]
                    lista_final_items = items_actuales + nuevos_items_dicts
                    
                    # Recalcular total y tiempos
                    nuevo_total = sum(i['cantidad'] * i['precio_unitario'] for i in lista_final_items)
                    
                    # Actualizar tiempo total acumulado (simplificado: sumamos lo nuevo a lo viejo, o recalculamos todo si tuviéramos info detallada, por ahora asumimos aditivo)
                    # Lo ideal: recalcular en base a todos los items del menú, pero items_actuales es dict.
                    # Estimación rápida:
                    tiempo_anterior = data_existente.get('tiempo_preparacion_total', 0)
                    nuevo_tiempo_total = tiempo_anterior + total_prep_time_items # Agregamos solo el tiempo de los nuevos items
                    
                    hora_entrega_estimada = datetime.now() + timedelta(minutes=nuevo_tiempo_total)
                    
                    orden_existente_doc.reference.update({
                        "items": lista_final_items,
                        "total": nuevo_total,
                        "tiempo_preparacion_total": nuevo_tiempo_total,
                        "hora_entrega_estimada": hora_entrega_estimada
                    })
                    
                    order_id = orden_existente_doc.id
                    hora_entrega_str = hora_entrega_estimada.strftime("%H:%M")
                    
                    mensaje_bot = f"¡Listo! Agregado. Total: ${nuevo_total}. Tiempo estimado total: {nuevo_tiempo_total} min (aprox {hora_entrega_str})."
                    await guardar_mensaje(request.telefono, "model", mensaje_bot)
                    
                    return {
                        "tipo": "orden_actualizada",
                        "mensaje": mensaje_bot,
                        "orden": {"id": order_id, "total": nuevo_total, "items": lista_final_items}
                    }

                else:
                    # -- CREAR NUEVA ORDEN --
                    total_calculado = sum(item.subtotal for item in new_order_items)
                    order_id = f"ord_{uuid.uuid4().hex[:8]}"
                    
                    hora_entrega_estimada = datetime.now() + timedelta(minutes=tiempo_prep_total)
                    
                    nueva_orden = Order(
                        id=order_id,
                        id_cliente=request.telefono,
                        items=new_order_items,
                        total=total_calculado,
                        tiempo_preparacion_total=tiempo_prep_total,
                        hora_entrega_estimada=hora_entrega_estimada
                    )
                    
                    if db:
                        db.collection('pedidos').document(order_id).set(nueva_orden.to_firestore())
                    
                    hora_entrega_str = hora_entrega_estimada.strftime("%H:%M")
                    mensaje_bot = f"¡Órale! Confirmado. Son ${total_calculado}. Queda listo en ~{tiempo_prep_total} min (a las {hora_entrega_str})."
                    await guardar_mensaje(request.telefono, "model", mensaje_bot)
                    
                    return {
                        "tipo": "orden_creada",
                        "mensaje": mensaje_bot,
                        "orden": nueva_orden.to_firestore()
                    }

            # CASO B: CANCELAR ORDEN (CON REGLA 5 MINUTOS)
            elif part.function_call and part.function_call.name == 'cancelar_orden':
                razon = recursive_to_native(part.function_call.args).get('razon', 'Sin razón')
                
                respuesta_texto = "No encontré ninguna orden pendiente pa' cancelar."
                tipo_resp = "texto"
                
                if db:
                    query = db.collection('pedidos').where(filter=firestore.FieldFilter("id_cliente", "==", request.telefono))\
                                                    .where(filter=firestore.FieldFilter("estado", "==", "pendiente"))\
                                                    .limit(1)
                    docs = list(query.stream())
                    if docs:
                        doc = docs[0]
                        data_doc = doc.to_dict()
                        
                        # --- CORRECCIÓN DE ZONA HORARIA ---
                        # Firestore guarda en UTC. Obtenemos esa fecha.
                        fecha_orden = data_doc.get('fecha_creacion')
                        
                        # Hora actual en UTC explícito
                        ahora_utc = datetime.now(timezone.utc)
                        
                        # Validar diferencia
                        minutos_pasados = 0
                        if fecha_orden:
                            # Aseguramos que fecha_orden tenga zona horaria para la resta (si viene naive, asumimos UTC)
                            if fecha_orden.tzinfo is None:
                                fecha_orden = fecha_orden.replace(tzinfo=timezone.utc)
                            
                            diferencia = ahora_utc - fecha_orden
                            minutos_pasados = diferencia.total_seconds() / 60
                            
                            print(f"DEBUG: Orden {fecha_orden} vs Ahora {ahora_utc} -> Diff: {minutos_pasados:.2f} min")
                        
                        if minutos_pasados > 5: # Límite de 5 minutos
                            respuesta_texto = f"Híjole, ya pasaron {int(minutos_pasados)} minutos y tu pedido ya está en preparación. No puedo cancelarlo. 🍳"
                            tipo_resp = "texto"
                        else:
                            # Si es < 5 min, procede a cancelar...
                            doc.reference.update({"estado": OrderStatus.CANCELADO})
                            respuesta_texto = f"Estás a tiempo (pasaron sólo {int(minutos_pasados)} min). Cancelada la orden {doc.id}."
                            tipo_resp = "orden_cancelada"

                await guardar_mensaje(request.telefono, "model", respuesta_texto)
                return {"tipo": tipo_resp, "mensaje": respuesta_texto}
            
            # CASO C: TEXTO NORMAL
            else:
                texto_respuesta = response.text
                try:
                    posibles_mensajes = json.loads(texto_respuesta)
                    if isinstance(posibles_mensajes, list):
                        full_text = " ".join(posibles_mensajes)
                        await guardar_mensaje(request.telefono, "model", full_text)
                        return {"tipo": "texto", "mensajes": posibles_mensajes, "mensaje": full_text}
                except:
                    pass
                
                await guardar_mensaje(request.telefono, "model", texto_respuesta)
                return {"tipo": "texto", "mensaje": texto_respuesta}
                
        return {"tipo": "error", "mensaje": "Sin respuesta válida"}
    except Exception as e:
        return {"tipo": "error", "mensaje": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
