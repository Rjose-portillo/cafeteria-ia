
import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
from google.cloud import firestore
from datetime import datetime
import uuid
import asyncio # Importante para manejo de asincronía

# Importamos tus modelos
from models import Order, OrderItem, OrderStatus

# --- 1. CONFIGURACIÓN Y SEGURIDAD ---
load_dotenv()

# Carga segura de variables de entorno
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT") # Ya no está hardcoded
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash") # Default si falla .env

if not GEMINI_API_KEY:
    raise ValueError("FATAL: GEMINI_API_KEY no encontrada en .env")

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configurar Firestore
try:
    # Si PROJECT_ID es None, intentará inferirlo del entorno de GCP
    db = firestore.Client(project=PROJECT_ID)
    print(f"✅ Conectado a Firestore: {db.project}")
except Exception as e:
    print(f"⚠️ Error conectando a Firestore: {e}")
    db = None

# --- 2. UTILIDADES ---
def recursive_to_native(d):
    """Limpia las estructuras de Protobuf de Google a tipos nativos de Python."""
    if hasattr(d, 'items'):
        return {k: recursive_to_native(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)) or (hasattr(d, '__iter__') and not isinstance(d, (str, bytes))):
        return [recursive_to_native(x) for x in d]
    return d

# --- 3. DEFINICIÓN DE HERRAMIENTAS IA ---
def interpretar_orden(items: List[Dict[str, Any]]):
    """Dummy function for tool definition signature."""
    return items 

tools_list = [interpretar_orden]

instruccion_sistema = """
Eres el mesero digital experto de 'Justicia y Café'.
OBJETIVO: Estructurar pedidos usando `interpretar_orden`.

REGLAS DE FORMATO JSON (ESTRICTO):
Cuando llames a la función, cada item DEBE tener EXACTAMENTE estas claves:
- 'nombre_producto': (string) El nombre del ítem.
- 'cantidad': (int)
- 'precio_unitario': (float) Asume $50.0 si no se dice.
- 'modificadores_seleccionados': (list[str]) Ej: ['sin azúcar', 'leche light'].
- 'notas_especiales': (str o null)

REGLAS DE NEGOCIO:
1. SIEMPRE usa la tool `interpretar_orden` para pedidos de comida/bebida.
2. Si es saludo o duda, responde amable y brevemente.
"""

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=tools_list,
    system_instruction=instruccion_sistema
)

# --- 4. API (FASTAPI) ---
app = FastAPI(title="Cafetería IA Backend", version="1.0.0")

class ChatRequest(BaseModel):
    mensaje: str
    telefono: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Iniciamos chat (stateless por ahora)
        chat_session = model.start_chat(enable_automatic_function_calling=False)
        
        # --- MEJORA CRÍTICA: ASINCRONÍA ---
        # Usamos await para no bloquear el servidor mientras Gemini piensa
        response = await chat_session.send_message_async(request.mensaje)
        
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            
            # A. CASO: ORDEN DETECTADA (TOOL CALL)
            if part.function_call and part.function_call.name == 'interpretar_orden':
                # Limpieza de datos
                args_native = recursive_to_native(part.function_call.args)
                raw_items = args_native.get('items', [])
                
                # Validación y Creación de Modelos
                order_items = []
                total_calculado = 0.0
                
                for item_data in raw_items:
                    nuevo_item = OrderItem(
                        nombre_producto=item_data.get('nombre_producto', 'Desconocido'),
                        cantidad=int(item_data.get('cantidad', 1)),
                        precio_unitario=float(item_data.get('precio_unitario', 50.0)),
                        modificadores_seleccionados=item_data.get('modificadores_seleccionados', []),
                        notas_especiales=item_data.get('notas_especiales')
                    )
                    order_items.append(nuevo_item)
                    total_calculado += nuevo_item.subtotal

                # Persistencia
                order_id = f"ord_{uuid.uuid4().hex[:8]}"
                nueva_orden = Order(
                    id=order_id,
                    id_cliente=request.telefono,
                    fecha_creacion=datetime.now(),
                    items=order_items,
                    total=total_calculado,
                    estado=OrderStatus.PENDIENTE,
                    metodo_pago="pendiente"
                )

                if db:
                    # Operación de I/O bloqueante envuelta para no frenar el loop (opcional en Firestore pero buena práctica)
                    # Por simplicidad en MVP lo dejamos directo, Firestore client es rápido.
                    doc_ref = db.collection('pedidos').document(order_id)
                    doc_ref.set(nueva_orden.to_firestore())
                    print(f"💾 Orden guardada: {order_id}")

                return {
                    "tipo": "orden_creada",
                    "mensaje": f"¡Entendido! Total: ${total_calculado}. ID: {order_id}",
                    "orden": nueva_orden.to_firestore()
                }
            
            # B. CASO: TEXTO NORMAL
            return {"tipo": "texto", "mensaje": response.text}
        
        return {"tipo": "error", "mensaje": "Gemini no devolvió contenido válido."}

    except Exception as e:
        print(f"🔥 Error en endpoint: {e}")
        return {"tipo": "error", "mensaje": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Reload activado para desarrollo
    uvicorn.run(app, host="0.0.0.0", port=8000)
