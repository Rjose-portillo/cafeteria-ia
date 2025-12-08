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
from app.services.scheduler_service import get_scheduler_service


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
        """Configure Gemini API (model created per request for personalization)."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._configured = True
            print(f"✅ Gemini API configurado: {settings.GEMINI_MODEL}")
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

        def registrar_nombre(nombre: str):
            """
            Registra el nombre del cliente en su perfil.
            Usar cuando el usuario proporciona su nombre espontáneamente o después de preguntarle.
            Esto permite personalizar futuras interacciones.

            Args:
                nombre: Nombre del cliente (ej: "Ricardo", "María", etc.)
            """
            return nombre

        # Include code execution for future mathematical calculations
        tools = [interpretar_orden, cancelar_orden, registrar_nombre]

        # Add code execution capability for precise calculations
        try:
            # Enable code execution for mathematical operations
            code_execution_tool = genai.protos.Tool(
                code_execution=genai.protos.CodeExecution()
            )
            tools.append(code_execution_tool)
        except Exception as e:
            print(f"Warning: Could not enable code execution: {e}")

        return tools
    
    def _build_system_instruction(self, customer_profile: Dict[str, Any] = None, favorite_product: str = None) -> str:
        """Build dynamic system instruction with current menu and customer context."""
        menu_service = get_menu_service()
        menu_text = menu_service.get_menu_text_for_prompt()

        # Enhanced customer context
        customer_context = ""
        customer_name = None
        if customer_profile:
            customer_name = customer_profile.get('nombre')
            if customer_name:
                customer_context = f"El usuario se llama {customer_name}."
            else:
                customer_context = "Usuario Nuevo/Desconocido - NO SABEMOS SU NOMBRE."
        else:
            customer_context = "Usuario Nuevo/Desconocido - NO SABEMOS SU NOMBRE."

        # Favorite product context for "El Habitual" feature
        favorite_context = ""
        if favorite_product:
            favorite_context = f"DATO CLAVE: El plato favorito de este usuario es '{favorite_product}'. Si saluda sin pedir nada específico, sugiere: '¿Lo de siempre ({favorite_product})?'."

        return f"""
### CONTEXTO DEL CLIENTE
{customer_context}

{favorite_context}

### ROL
Eres 'Pepe', el mesero digital de la cafetería 'Justicia y Café'.
Tu tono es amable, coloquial (mexicano neutro) y eficiente.

### MENÚ DISPONIBLE (PRECIOS REALES)
{menu_text}

### ⛔ REGLAS DE INVENTARIO
Solo puedes vender items que estén explícitamente listados en el MENÚ DISPONIBLE.
Si el usuario pide algo que no está (ej. Pizza, Sushi, Hamburguesa), responde amablemente que en 'Justicia y Café' no manejamos eso, y sugiere una alternativa del menú existente.

### OBJETIVO
Gestionar el CICLO COMPLETO del cliente: Identificación → Venta → Cierre → Post-Venta.

### 🚀 FASES DEL CICLO DE VIDA DEL CLIENTE

#### 🎯 FASE 0 - IDENTIFICACIÓN (CRÍTICA):
SI el usuario es NUEVO/DESCONOCIDO (no sabemos su nombre):
- PRIMERA acción: Saludar y preguntar nombre casualmente
- NO tomes pedidos hasta saber con quién hablas
- Ejemplos: "¿Con quién tengo el gusto hoy?", "¿A nombre de quién abro la comanda?"
- Una vez que te dé su nombre → USA 'registrar_nombre' INMEDIATAMENTE

#### 🍽️ FASE 1 - TOMA DE PEDIDOS + UPSELLING:
**UPSELLING INTELIGENTE:**
- Si piden Café → Sugiere Postre específico (ej. Brownie).
- Si piden Alimento → Sugiere Bebida fría.
- Si es TARDE (después de 6 PM) → Sugiere DESCAFEINADO: "Si quieres algo más suave, tenemos descafeinado"

#### ❌ FASE 2 - CANCELACIONES (EMPATÍA):
Si usuario pide cancelar:
1. USA herramienta 'cancelar_orden' SIN EXCEPTUAR
2. Si devuelve ERROR por tiempo (>5 min) → Responde con empatía usando nombre:
   "Híjole{customer_name and f' {customer_name}' or ''}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
3. NUNCA prometas cancelar sin usar herramienta primero

#### 💰 FASE 3 - PLAN DE AFILIADOS "JUSTICIA PARA TODOS":
Si preguntan por descuentos o puntos:
- Explica: "Tenemos el plan 'Justicia para Todos' donde acumulas 5% en puntos por cada compra"
- Los puntos se pueden canjear por descuentos en futuras compras
- Es nuestra forma de agradecer tu preferencia

### REGLAS DE ORO (CRÍTICAS)

#### 🎯 REGLA DE ORO (ONBOARDING):
SI el usuario es DESCONOCIDO/Nuevo, tu PRIMERA acción es saludar amablemente y preguntar su nombre.
NO tomes NINGÚN pedido hasta saber con quién hablas.
Ejemplo: ["¡Hola! 👋 Soy Pepe, tu mesero digital", "¿Cómo te llamas para atenderte mejor?"]
Una vez que te dé su nombre, usa la herramienta 'registrar_nombre' INMEDIATAMENTE.

#### ❌ REGLA DE CANCELACIÓN:
Si el usuario pide cancelar, usa la herramienta 'cancelar_orden' SIN EXCEPTUAR.
Si la herramienta devuelve error (por tiempo límite), explícaselo con empatía:
"Híjole{customer_name and f' {customer_name}' or ''}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
NUNCA prometas cancelar sin usar la herramienta primero.

#### 💰 REGLA DE UPSELLING (VENTA CRUZADA):
Si piden SOLO café/bebida → Sugiere sutilmente un pan/postre.
Si piden SOLO comida → Sugiere sutilmente una bebida.
Si es TARDE (después de 6 PM) → Sugiere descafeinado.
Hazlo CORTO y NATURAL: "Va perfecto con un croissant de acompañante"

### DIRECTRICES DE COMPORTAMIENTO (JSON)
{{
  "personalidad": {{
    "tono": "Amigable, servicial, proactivo. Usa emojis de justicia (⚖️, 👨‍⚖️) y café (☕) en frases de cierre.",
    "estilo": "Breve y directo. Evita bloques de texto largos."
  }},
  "reglas_negocio": {{
    "precios": "Usa los precios del menú. Si no está en menú, di que no tenemos eso.",
    "confirmacion": "Siempre confirma lo que entendiste antes de procesar.",
    "cierre": "Siempre pregunta '¿Algo más?' o '¿Todo bien?' al final."
  }},
  "manejo_herramientas": {{
    "interpretar_orden": "USAR CUANDO: El cliente pide alimentos o bebidas. INCLUSO si es un item adicional.",
    "cancelar_orden": "USAR CUANDO: El cliente pide cancelar, borrar o se equivocó.",
    "registrar_nombre": "USAR CUANDO: El cliente se presenta o da su nombre."
  }},
  "correcciones_inmediatas": {{
    "regla_principal": "SI el mensaje contiene corrección inmediata, IGNORA la primera parte y obedece SÓLO la última instrucción válida.",
    "ejemplos": [
      "'Quiero café... no, mejor té' → Interpreta SOLO 'té'",
      "'Dos croissants... mejor solo uno' → Interpreta SOLO 'uno'"
    ]
  }},
  "modo_juez_hambriento": {{
    "regla_urgencia": "Analiza el tono del usuario. SI escribe en MAYÚSCULAS o usa palabras como ['URGE', 'RÁPIDO', 'PRISA', 'AUDIENCIA', 'CORRIENDO'], ACTIVA EL 'MODO EXPRESS'.",
    "modo_express_acciones": [
      "1. ELIMINA todos los saludos y cortesías.",
      "2. Confirma la orden en una sola frase corta.",
      "3. No hagas upselling.",
      "4. Tu prioridad es la velocidad."
    ],
    "ejemplos_urgencia": [
      "Mensaje: 'URGENTE necesito un latte YA' → Modo Express: 'Listo, latte confirmado.'",
      "Mensaje: 'CORRIENDO a una reunión, café negro' → Modo Express: 'Café negro confirmado.'"
    ]
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
            # 1. Get customer profile for personalization
            customer_profile = await firestore.get_customer_profile(telefono)

            # 2. Get customer's favorite product for "El Habitual" feature
            favorite_product = await firestore.get_favorite_product(telefono) if firestore.is_connected else None

            # 3. Get chat history
            historial = await firestore.get_chat_history(telefono)

            # 4. Create model with customer context
            personalized_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                tools=self._get_tools(),
                system_instruction=self._build_system_instruction(customer_profile, favorite_product),
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )

            # 4. Start chat session
            chat_session = personalized_model.start_chat(
                history=historial,
                enable_automatic_function_calling=False
            )

            # 5. Save user message
            await firestore.save_message(telefono, "user", mensaje)

            # 6. Send to Gemini
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

            # CASE C: Name registration
            elif part.function_call and part.function_call.name == 'registrar_nombre':
                return await self._handle_name_registration(telefono, part.function_call.args, firestore)

            # CASE D: Text response
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

        # Schedule automated feedback message (30-40 minutes after delivery)
        try:
            scheduler = get_scheduler_service()
            # Schedule feedback for 35 minutes from now (average delivery + some buffer)
            scheduler.schedule_feedback(telefono, customer_name or "Cliente", delay_minutes=35)
        except Exception as e:
            print(f"⚠️ Error programando feedback para {telefono}: {e}")

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

        # Get customer name for personalized response
        customer_profile = await firestore.get_customer_profile(telefono)
        customer_name = customer_profile.get('nombre') if customer_profile else None

        existing = await firestore.get_pending_order(telefono)

        if not existing:
            mensaje = "No encontré ninguna orden pendiente pa' cancelar."
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        doc, data = existing
        fecha_orden_raw = data.get('fecha_creacion')

        # CRITICAL: Ensure UTC timezone consistency
        ahora_utc = datetime.now(timezone.utc)

        minutos_pasados = 0
        if fecha_orden_raw:
            # Handle Firestore timestamp conversion - ensure UTC timezone
            if hasattr(fecha_orden_raw, 'timestamp'):  # Firestore Timestamp
                # Convert Firestore timestamp to UTC datetime
                timestamp_seconds = fecha_orden_raw.timestamp()
                fecha_orden = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            elif isinstance(fecha_orden_raw, datetime):
                # Regular datetime - ensure UTC
                if fecha_orden_raw.tzinfo is None:
                    # Assume UTC if no timezone info (Firestore default)
                    fecha_orden = fecha_orden_raw.replace(tzinfo=timezone.utc)
                else:
                    # Convert to UTC if different timezone
                    fecha_orden = fecha_orden_raw.astimezone(timezone.utc)
            else:
                # Fallback - treat as UTC timestamp
                try:
                    fecha_orden = datetime.fromtimestamp(float(fecha_orden_raw), tz=timezone.utc)
                except (ValueError, TypeError):
                    print(f"ERROR: Could not parse fecha_orden: {fecha_orden_raw}")
                    fecha_orden = ahora_utc  # Fallback to allow cancellation

            # Both datetimes are now guaranteed to be timezone-aware UTC
            diferencia = ahora_utc - fecha_orden
            minutos_pasados = diferencia.total_seconds() / 60

            print(f"DEBUG: Orden {fecha_orden} vs Ahora {ahora_utc} -> Diff: {minutos_pasados:.2f} min")

        # Check 5-minute rule
        if minutos_pasados > settings.CANCEL_TIME_LIMIT_MINUTES:
            # Personalized empathetic response using customer name
            name_part = f" {customer_name}" if customer_name else ""
            mensaje = f"Híjole{name_part}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        # Cancel the order
        await firestore.cancel_order(doc.id)
        mensaje = f"Estás a tiempo (pasaron sólo {int(minutos_pasados)} min). Cancelada la orden {doc.id}. Razón: {razon}"

        await firestore.save_message(telefono, "model", mensaje)
        return ChatResponse(tipo="orden_cancelada", mensaje=mensaje)

    async def _handle_name_registration(
        self,
        telefono: str,
        args: Any,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle customer name registration."""

        nombre = self._recursive_to_native(args).get('nombre', '').strip()

        if not nombre:
            mensaje = "No pude entender tu nombre. ¿Me lo puedes repetir?"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        # Update customer profile with name
        success = await firestore.update_customer_profile(telefono, {"nombre": nombre})

        if success:
            mensaje = f"¡Perfecto, {nombre}! Ya te tengo registrado. ¿Qué se te antoja hoy? ☕"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
        else:
            mensaje = "Híjole, tuve un problema guardando tu nombre. ¿Me lo puedes decir otra vez?"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
    
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
        """Refresh the API configuration."""
        self._configured = False
        self._configure()


@lru_cache()
def get_gemini_service() -> GeminiService:
    """Get singleton instance of GeminiService."""
    return GeminiService()