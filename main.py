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
    return items

tools_list = [interpretar_orden]

# --- SYSTEM INSTRUCTION ---
instruccion_sistema = """
Eres el mesero digital de 'Justicia y Café'.

REGLAS DE RESPUESTA:
- Si tu respuesta es texto, PUEDES devolver una lista JSON de strings para simular mensajes separados. Ejemplo: ["¡Hola!", "¿En qué te ayudo?"]
- Asume precio $50.0 por item si no se especifica.
- Tienes memoria del chat anterior. No repitas preguntas obvias.
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
        # Firestore devuelve en orden desc (más nuevo primero), invertimos para Gemini (antiguo a nuevo)
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
            
            # CASO A: ORDEN
            if part.function_call and part.function_call.name == 'interpretar_orden':
                args = recursive_to_native(part.function_call.args)
                raw_items = args.get('items', [])
                
                order_items = []
                total = 0.0
                for item in raw_items:
                    precio = float(item.get('precio_unitario', 50.0))
                    costo_estimado = precio * 0.30 # [CONTABILIDAD]
                    
                    obj_item = OrderItem(
                        nombre_producto=item.get('nombre_producto', 'Item'),
                        cantidad=int(item.get('cantidad', 1)),
                        precio_unitario=precio,
                        costo_unitario=costo_estimado,
                        modificadores_seleccionados=item.get('modificadores_seleccionados', []),
                        notas_especiales=item.get('notas_especiales')
                    )
                    order_items.append(obj_item)
                    total += obj_item.subtotal
                
                order_id = f"ord_{uuid.uuid4().hex[:8]}"
                nueva_orden = Order(
                    id=order_id,
                    id_cliente=request.telefono,
                    items=order_items,
                    total=total
                )
                
                if db:
                    db.collection('pedidos').document(order_id).set(nueva_orden.to_firestore())
                    await guardar_mensaje(request.telefono, "model", f"Orden creada ID: {order_id}")
                return {
                    "tipo": "orden_creada",
                    "mensaje": f"¡Pedido listo! Total: ${total}. ID: {order_id}",
                    "orden": nueva_orden.to_firestore()
                }
            
            # CASO B: TEXTO
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
