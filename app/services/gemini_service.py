"""
Gemini AI Service - AI chat processing with business logic.
Handles order interpretation, cancellation, and conversation management.
Implements "Comanda Abierta" (open tab) logic and time-based cancellation rules.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
from functools import lru_cache
import uuid
import json

import google.generativeai as genai

from app.core.config import settings
from app.models.schemas import Order, OrderItem, OrderStatus, ChatResponse
from app.services.firestore_service import get_firestore_service
from app.services.menu_service import get_menu_service


class GeminiService:
    """
    Service for Gemini AI interactions.
    Manages chat sessions, tool calls, and business logic processing.
    """
    
    _instance: Optional['GeminiService'] = None
    _model: Optional[genai.GenerativeModel] = None
    _configured: bool = False
    
    def __new__(cls) -> 'GeminiService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._configured:
            self._configure()
    
    def _configure(self):
        """Configure Gemini API and model."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                tools=self._get_tools(),
                system_instruction=self._build_system_instruction()
            )
            self._configured = True
            print(f"✅ Gemini configurado: {settings.GEMINI_MODEL}")
        except Exception as e:
            print(f"❌ Error configurando Gemini: {e}")
            self._configured = False
    
    def _get_tools(self) -> List:
        """Define AI tools for function calling."""
        
        def interpretar_orden(items: List[Dict[str, Any]]):
            """
            Agrega items a la orden del cliente.
            Usar cuando el cliente pide alimentos o bebidas.
            
            Args:
                items: Lista de items con nombre_producto, cantidad, modificadores, notas
            """
            return items
        
        def cancelar_orden(razon: str):
            """
            Cancela la orden pendiente actual.
            Usar cuando el cliente explícitamente pide cancelar su pedido.
            
            Args:
                razon: Motivo de la cancelación
            """
            return razon
        
        return [interpretar_orden, cancelar_orden]
    
    def _build_system_instruction(self) -> str:
        """Build dynamic system instruction with current menu."""
        menu_service = get_menu_service()
        menu_text = menu_service.get_menu_text_for_prompt()
        
        return f"""
### ROL
Eres 'Pepe', el mesero digital de la cafetería 'Justicia y Café'.
Tu tono es amable, coloquial (mexicano neutro) y eficiente.

### MENÚ DISPONIBLE (PRECIOS REALES)
{menu_text}

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
    
    @staticmethod
    def _recursive_to_native(d: Any) -> Any:
        """Convert protobuf/MapComposite objects to native Python types."""
        if hasattr(d, 'items'):
            return {k: GeminiService._recursive_to_native(v) for k, v in d.items()}
        if isinstance(d, (list, tuple)) or (hasattr(d, '__iter__') and not isinstance(d, (str, bytes))):
            return [GeminiService._recursive_to_native(x) for x in d]
        return d
    
    async def process_chat(self, telefono: str, mensaje: str) -> ChatResponse:
        """
        Process a chat message and return appropriate response.
        Handles tool calls, order management, and text responses.
        """
        firestore = get_firestore_service()
        menu_service = get_menu_service()
        
        try:
            # 1. Get chat history
            historial = await firestore.get_chat_history(telefono)
            
            # 2. Start chat session
            chat_session = self._model.start_chat(
                history=historial,
                enable_automatic_function_calling=False
            )
            
            # 3. Save user message
            await firestore.save_message(telefono, "user", mensaje)
            
            # 4. Send to Gemini
            response = await chat_session.send_message_async(mensaje)
            
            if not response.candidates or not response.candidates[0].content.parts:
                return ChatResponse(tipo="error", mensaje="Sin respuesta válida del AI")
            
            part = response.candidates[0].content.parts[0]
            
            # CASE A: Order interpretation
            if part.function_call and part.function_call.name == 'interpretar_orden':
                return await self._handle_order(telefono, part.function_call.args, menu_service, firestore)
            
            # CASE B: Order cancellation
            elif part.function_call and part.function_call.name == 'cancelar_orden':
                return await self._handle_cancellation(telefono, part.function_call.args, firestore)
            
            # CASE C: Text response
            else:
                return await self._handle_text_response(telefono, response.text, firestore)
                
        except Exception as e:
            print(f"❌ Error en process_chat: {e}")
            return ChatResponse(tipo="error", mensaje=str(e))
    
    async def _handle_order(
        self, 
        telefono: str, 
        args: Any, 
        menu_service: 'MenuService',
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle order creation or update (Comanda Abierta logic)."""
        
        args_native = self._recursive_to_native(args)
        raw_items = args_native.get('items', [])
        
        # Convert to OrderItem objects with real prices
        new_order_items = []
        total_prep_time = 0
        
        for item_data in raw_items:
            nombre = item_data.get('nombre_producto', 'Item')
            cantidad = int(item_data.get('cantidad', 1))
            
            # Search in real menu
            menu_item = menu_service.buscar_producto(nombre)
            
            if menu_item:
                precio = float(menu_item.get('precio', 50.0))
                tiempo_prep = int(menu_item.get('tiempo_prep', 5))
            else:
                precio = float(item_data.get('precio_unitario', 50.0))
                tiempo_prep = 5
            
            # Calculate cost (30% default)
            costo = precio * settings.DEFAULT_COST_PERCENTAGE
            total_prep_time += (tiempo_prep * cantidad)
            
            order_item = OrderItem(
                nombre_producto=nombre,
                cantidad=cantidad,
                precio_unitario=precio,
                costo_unitario=costo,
                tiempo_prep_unitario=tiempo_prep,
                modificadores_seleccionados=item_data.get('modificadores_seleccionados', []),
                notas_especiales=item_data.get('notas_especiales')
            )
            new_order_items.append(order_item)
        
        # Add buffer time
        tiempo_total = total_prep_time + settings.DEFAULT_PREP_BUFFER_MINUTES
        
        # Check for existing pending order (Comanda Abierta)
        existing = await firestore.get_pending_order(telefono)
        
        if existing:
            return await self._update_existing_order(
                telefono, existing, new_order_items, total_prep_time, firestore
            )
        else:
            return await self._create_new_order(
                telefono, new_order_items, tiempo_total, firestore
            )
    
    async def _update_existing_order(
        self,
        telefono: str,
        existing: tuple,
        new_items: List[OrderItem],
        new_prep_time: int,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Update an existing pending order with new items."""
        
        doc, data = existing
        current_items = data.get('items', [])
        
        # Add new items
        new_items_dicts = [item.to_firestore() for item in new_items]
        all_items = current_items + new_items_dicts
        
        # Recalculate totals
        nuevo_total = sum(i['cantidad'] * i['precio_unitario'] for i in all_items)
        
        # Update prep time
        tiempo_anterior = data.get('tiempo_preparacion_total', 0)
        nuevo_tiempo = tiempo_anterior + new_prep_time
        
        hora_entrega = datetime.now(timezone.utc) + timedelta(minutes=nuevo_tiempo)
        
        # Update in Firestore
        await firestore.update_order(doc.id, {
            "items": all_items,
            "total": nuevo_total,
            "tiempo_preparacion_total": nuevo_tiempo,
            "hora_entrega_estimada": hora_entrega
        })
        
        hora_str = hora_entrega.strftime("%H:%M")
        mensaje = f"¡Listo! Agregado a tu orden. Total: ${nuevo_total:.2f}. Tiempo estimado: {nuevo_tiempo} min (aprox {hora_str})."
        
        await firestore.save_message(telefono, "model", mensaje)
        
        return ChatResponse(
            tipo="orden_actualizada",
            mensaje=mensaje,
            orden={"id": doc.id, "total": nuevo_total, "items": all_items, "tiempo_estimado": nuevo_tiempo}
        )
    
    async def _create_new_order(
        self,
        telefono: str,
        items: List[OrderItem],
        tiempo_total: int,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Create a new order."""
        
        total = sum(item.subtotal for item in items)
        order_id = f"ord_{uuid.uuid4().hex[:8]}"
        hora_entrega = datetime.now(timezone.utc) + timedelta(minutes=tiempo_total)
        
        nueva_orden = Order(
            id=order_id,
            id_cliente=telefono,
            items=items,
            total=total,
            tiempo_preparacion_total=tiempo_total,
            hora_entrega_estimada=hora_entrega
        )
        
        await firestore.create_order(nueva_orden)
        
        hora_str = hora_entrega.strftime("%H:%M")
        mensaje = f"¡Órale! Confirmado. Son ${total:.2f}. Queda listo en ~{tiempo_total} min (a las {hora_str})."
        
        await firestore.save_message(telefono, "model", mensaje)
        
        return ChatResponse(
            tipo="orden_creada",
            mensaje=mensaje,
            orden=nueva_orden.to_firestore()
        )
    
    async def _handle_cancellation(
        self,
        telefono: str,
        args: Any,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle order cancellation with 5-minute rule."""
        
        razon = self._recursive_to_native(args).get('razon', 'Sin razón')
        
        existing = await firestore.get_pending_order(telefono)
        
        if not existing:
            mensaje = "No encontré ninguna orden pendiente pa' cancelar."
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
        
        doc, data = existing
        fecha_orden = data.get('fecha_creacion')
        ahora_utc = datetime.now(timezone.utc)
        
        minutos_pasados = 0
        if fecha_orden:
            # Ensure timezone awareness
            if fecha_orden.tzinfo is None:
                fecha_orden = fecha_orden.replace(tzinfo=timezone.utc)
            
            diferencia = ahora_utc - fecha_orden
            minutos_pasados = diferencia.total_seconds() / 60
            
            print(f"DEBUG: Orden {fecha_orden} vs Ahora {ahora_utc} -> Diff: {minutos_pasados:.2f} min")
        
        # Check 5-minute rule
        if minutos_pasados > settings.CANCEL_TIME_LIMIT_MINUTES:
            mensaje = f"Híjole, ya pasaron {int(minutos_pasados)} minutos y tu pedido ya está en preparación. No puedo cancelarlo. 🍳"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
        
        # Cancel the order
        await firestore.cancel_order(doc.id)
        mensaje = f"Estás a tiempo (pasaron sólo {int(minutos_pasados)} min). Cancelada la orden {doc.id}. Razón: {razon}"
        
        await firestore.save_message(telefono, "model", mensaje)
        return ChatResponse(tipo="orden_cancelada", mensaje=mensaje)
    
    async def _handle_text_response(
        self,
        telefono: str,
        texto: str,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle plain text response from AI."""
        
        # Try to parse as JSON array (multi-bubble format)
        try:
            mensajes = json.loads(texto)
            if isinstance(mensajes, list):
                full_text = " ".join(mensajes)
                await firestore.save_message(telefono, "model", full_text)
                return ChatResponse(
                    tipo="texto",
                    mensaje=full_text,
                    mensajes=mensajes
                )
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Plain text response
        await firestore.save_message(telefono, "model", texto)
        return ChatResponse(tipo="texto", mensaje=texto)
    
    def refresh_model(self):
        """Refresh the model with updated menu."""
        self._configured = False
        self._configure()


@lru_cache()
def get_gemini_service() -> GeminiService:
    """Get singleton instance of GeminiService."""
    return GeminiService()