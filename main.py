import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Union
from dotenv import load_dotenv
from google.cloud import firestore
from datetime import datetime
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

# --- UTILS ---
def recursive_to_native(d):
    if hasattr(d, 'items'):
        return {k: recursive_to_native(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)) or (hasattr(d, '__iter__') and not isinstance(d, (str, bytes))):
        return [recursive_to_native(x) for x in d]
    return d

# --- TOOLS ---
def interpretar_orden(items: List[Dict[str, Any]]):
    """Agrega items a la orden (nueva o existente)."""
    return items

def cancelar_orden(razon: str):
    """Cancela la orden pendiente actual si existe."""
    return razon

tools_list = [interpretar_orden, cancelar_orden]

# --- SYSTEM INSTRUCTION ---
instruccion_sistema = """
### ROL
Eres 'Pepe', el mesero digital de la cafetería 'Justicia y Café'.
Tu tono es amable, coloquial (mexicano neutro) y eficiente.

### OBJETIVO
Gestionar la toma de pedidos, dudas y cancelaciones de los clientes mediante el uso estricto de herramientas.

### DIRECTRICES DE COMPORTAMIENTO (JSON)
{
  "personalidad": {
    "tono": "Amigable, servicial, proactivo",
    "estilo": "Breve y directo. Evita bloques de texto largos."
  },
  "reglas_negocio": {
    "precios": "Si el cliente no especifica, asume $50.00 MXN por item.",
    "confirmacion": "Siempre confirma lo que entendiste antes de procesar.",
    "cierre": "Siempre pregunta '¿Algo más?' o '¿Todo bien?' al final."
  },
  "manejo_herramientas": {
    "interpretar_orden": "USAR CUANDO: El cliente pide alimentos o bebidas. INCLUSO si es un item adicional ('y también una dona').",
    "cancelar_orden": "USAR CUANDO: El cliente explícitamente pide cancelar, borrar o dice que se equivocó en el pedido anterior."
  }
}

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

# --- ENDPOINT CHAT ---
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 1. Recuperar Memoria
        historial = await obtener_historial(request.telefono)

        # 2. Iniciar Chat con Memoria
        chat_session = model.start_chat(history=historial, enable_automatic_function_calling=False)
        
        # 3. Guardar mensaje usuario
        await guardar_mensaje(request.telefono, "user", request.mensaje)
        
        # 4. Enviar a Gemini
        response = await chat_session.send_message_async(request.mensaje)
        
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            
            # CASO A: ORDEN / AGREGAR ITEMS
            if part.function_call and part.function_call.name == 'interpretar_orden':
                args_native = recursive_to_native(part.function_call.args)
                raw_items = args_native.get('items', [])
                
                # Convertir input a objetos OrderItem (con cálculo de costos)
                new_order_items = []
                for item_data in raw_items:
                    precio = float(item_data.get('precio_unitario', 50.0))
                    costo_estimado = precio * 0.30
                    
                    obj_item = OrderItem(
                        nombre_producto=item_data.get('nombre_producto', 'Item'),
                        cantidad=int(item_data.get('cantidad', 1)),
                        precio_unitario=precio,
                        costo_unitario=costo_estimado,
                        modificadores_seleccionados=item_data.get('modificadores_seleccionados', []),
                        notas_especiales=item_data.get('notas_especiales')
                    )
                    new_order_items.append(obj_item)

                # LÓGICA DE COMANDA ABIERTA
                orden_existente_doc = None
                if db:
                    # Buscar orden pendiente
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
                    
                    # Recalcular total
                    nuevo_total = sum(i['cantidad'] * i['precio_unitario'] for i in lista_final_items)
                    
                    # Update en Firestore
                    orden_existente_doc.reference.update({
                        "items": lista_final_items,
                        "total": nuevo_total
                    })
                    
                    order_id = orden_existente_doc.id
                    mensaje_bot = f"¡Listo! Agregué eso a tu comanda ({order_id}). Total va en: ${nuevo_total}."
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
                    
                    nueva_orden = Order(
                        id=order_id,
                        id_cliente=request.telefono,
                        items=new_order_items,
                        total=total_calculado
                    )
                    
                    if db:
                        db.collection('pedidos').document(order_id).set(nueva_orden.to_firestore())
                    
                    mensaje_bot = f"¡Órale! Abriendo comanda nueva con costo de ${total_calculado}."
                    await guardar_mensaje(request.telefono, "model", mensaje_bot)
                    
                    return {
                        "tipo": "orden_creada",
                        "mensaje": mensaje_bot,
                        "orden": nueva_orden.to_firestore()
                    }

            # CASO B: CANCELAR ORDEN
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
                        doc.reference.update({"estado": OrderStatus.CANCELADO})
                        respuesta_texto = f"Va, cancelada la orden {doc.id}. Sin rencores."
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
