"""
Firestore Service - Database operations singleton.
Handles all CRUD operations for orders, chat history, and customer profiles.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from functools import lru_cache

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from app.core.config import settings
from app.models.schemas import Order, OrderItem, ChatMessage, OrderStatus, CustomerProfile, Insumo


class FirestoreService:
    """
    Singleton service for Firestore database operations.
    Provides CRUD methods for all collections.
    """
    
    _instance: Optional['FirestoreService'] = None
    _db: Optional[firestore.Client] = None
    
    def __new__(cls) -> 'FirestoreService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            try:
                self._db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT)
                print(f"✅ Firestore conectado: {self._db.project}")
            except Exception as e:
                print(f"❌ Error conectando Firestore: {e}")
                self._db = None
    
    @property
    def db(self) -> Optional[firestore.Client]:
        return self._db
    
    @property
    def is_connected(self) -> bool:
        return self._db is not None
    
    # --- Chat History Operations ---
    
    async def get_chat_history(self, telefono: str, limit: int = None) -> List[Dict[str, str]]:
        """
        Retrieve chat history for a customer.
        Returns list in Gemini-compatible format: [{"role": "user/model", "parts": [...]}]
        """
        if not self.is_connected:
            return []
        
        limit = limit or settings.CHAT_HISTORY_LIMIT
        
        try:
            mensajes_ref = self._db.collection('clientes').document(telefono).collection('chat_history')
            query = mensajes_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
            docs = query.stream()
            
            historial_gemini = []
            msgs = list(docs)[::-1]  # Reverse to chronological order
            
            for doc in msgs:
                datos = doc.to_dict()
                role = "user" if datos['role'] == "user" else "model"
                historial_gemini.append({"role": role, "parts": [datos['content']]})
            
            return historial_gemini
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    async def save_message(self, telefono: str, role: str, content: str) -> bool:
        """Save a chat message to history."""
        if not self.is_connected:
            return False
        
        try:
            mensajes_ref = self._db.collection('clientes').document(telefono).collection('chat_history')
            nuevo_msg = ChatMessage(role=role, content=content)
            mensajes_ref.add(nuevo_msg.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error guardando mensaje: {e}")
            return False
    
    # --- Order Operations ---
    
    async def get_pending_order(self, telefono: str) -> Optional[tuple]:
        """
        Get the pending order for a customer.
        Returns tuple of (document_snapshot, order_data) or None.
        """
        if not self.is_connected:
            return None
        
        try:
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("id_cliente", "==", telefono))\
                .where(filter=FieldFilter("estado", "==", "pendiente"))\
                .limit(1)
            
            docs = list(query.stream())
            if docs:
                return (docs[0], docs[0].to_dict())
            return None
        except Exception as e:
            print(f"❌ Error buscando orden pendiente: {e}")
            return None
    
    async def create_order(self, order: Order) -> bool:
        """Create a new order in Firestore."""
        if not self.is_connected:
            return False
        
        try:
            self._db.collection('pedidos').document(order.id).set(order.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error creando orden: {e}")
            return False
    
    async def update_order(self, order_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing order."""
        if not self.is_connected:
            return False
        
        try:
            self._db.collection('pedidos').document(order_id).update(updates)
            return True
        except Exception as e:
            print(f"❌ Error actualizando orden: {e}")
            return False
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order by updating its status."""
        return await self.update_order(order_id, {"estado": OrderStatus.CANCELADO})
    
    async def get_orders_by_status(self, status: OrderStatus) -> List[Dict[str, Any]]:
        """Get all orders with a specific status."""
        if not self.is_connected:
            return []
        
        try:
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("estado", "==", status.value))\
                .order_by('fecha_creacion', direction=firestore.Query.ASCENDING)
            
            orders = []
            for doc in query.stream():
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            
            return orders
        except Exception as e:
            print(f"❌ Error obteniendo órdenes: {e}")
            return []
    
    async def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get all active orders (pending or in preparation)."""
        if not self.is_connected:
            return []
        
        try:
            # Get pending orders
            pending = await self.get_orders_by_status(OrderStatus.PENDIENTE)
            # Get orders in preparation
            in_prep = await self.get_orders_by_status(OrderStatus.EN_PREPARACION)
            
            return pending + in_prep
        except Exception as e:
            print(f"❌ Error obteniendo órdenes activas: {e}")
            return []
    
    # --- Menu Operations ---
    
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Get all available menu items."""
        if not self.is_connected:
            return []
        
        try:
            docs = self._db.collection('menu')\
                .where(filter=FieldFilter("disponible", "==", True))\
                .stream()
            
            items = []
            for doc in docs:
                item_data = doc.to_dict()
                item_data['id'] = doc.id
                items.append(item_data)
            
            return items
        except Exception as e:
            print(f"❌ Error obteniendo menú: {e}")
            return []
    
    # --- Customer Profile Operations ---
    
    async def get_customer_profile(self, telefono: str) -> Optional[Dict[str, Any]]:
        """Get customer profile data."""
        if not self.is_connected:
            return None
        
        try:
            doc = self._db.collection('clientes').document(telefono).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error obteniendo perfil: {e}")
            return None
    
    async def update_customer_profile(self, telefono: str, profile_data: Dict[str, Any]) -> bool:
        """Update or create customer profile."""
        if not self.is_connected:
            return False

        try:
            self._db.collection('clientes').document(telefono).set(profile_data, merge=True)
            return True
        except Exception as e:
            print(f"❌ Error actualizando perfil: {e}")
            return False

    # --- Ingredient Operations ---

    async def get_all_insumos(self) -> List[Dict[str, Any]]:
        """Get all ingredients."""
        if not self.is_connected:
            return []

        try:
            docs = self._db.collection('insumos').stream()

            insumos = []
            for doc in docs:
                insumo_data = doc.to_dict()
                insumo_data['id'] = doc.id
                insumos.append(insumo_data)

            return insumos
        except Exception as e:
            print(f"❌ Error obteniendo insumos: {e}")
            return []

    async def create_insumo(self, insumo: Insumo) -> bool:
        """Create a new ingredient."""
        if not self.is_connected:
            return False

        try:
            doc_ref = self._db.collection('insumos').document()
            insumo.id = doc_ref.id
            doc_ref.set(insumo.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error creando insumo: {e}")
            return False

    async def update_insumo(self, insumo_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing ingredient."""
        if not self.is_connected:
            return False

        try:
            self._db.collection('insumos').document(insumo_id).update(data)
            return True
        except Exception as e:
            print(f"❌ Error actualizando insumo: {e}")
            return False

    # --- Daily Sales Metrics ---

    async def get_daily_sales_metrics(self, date: datetime) -> Dict[str, Any]:
        """
        Get daily sales metrics for a specific date.
        Returns total sales and number of orders for that day.
        """
        if not self.is_connected:
            return {"total_ventas": 0.0, "total_ordenes": 0}

        try:
            # Calculate start and end of the day in UTC
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Query orders for the day
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("fecha_creacion", ">=", start_of_day))\
                .where(filter=FieldFilter("fecha_creacion", "<=", end_of_day))\
                .where(filter=FieldFilter("estado", "in", ["entregado", "listo"]))

            docs = list(query.stream())

            total_ventas = 0.0
            total_ordenes = len(docs)

            for doc in docs:
                order_data = doc.to_dict()
                total_ventas += order_data.get('total', 0.0)

            return {
                "total_ventas": total_ventas,
                "total_ordenes": total_ordenes
            }
        except Exception as e:
            print(f"❌ Error obteniendo métricas diarias: {e}")
            return {"total_ventas": 0.0, "total_ordenes": 0}

    # --- Premium Personalization Features ---

    async def get_favorite_product(self, telefono: str) -> Optional[str]:
        """
        Get customer's favorite product based on order history.
        Returns the product name if ordered 3+ times, None otherwise.
        """
        if not self.is_connected:
            return None

        try:
            # Query all completed orders for this customer
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("id_cliente", "==", telefono))\
                .where(filter=FieldFilter("estado", "in", ["entregado", "listo"]))

            docs = list(query.stream())

            if not docs:
                return None

            # Count product occurrences
            product_counts = {}

            for doc in docs:
                order_data = doc.to_dict()
                items = order_data.get('items', [])

                for item in items:
                    product_name = item.get('nombre_producto', '')
                    if product_name:
                        product_counts[product_name] = product_counts.get(product_name, 0) + item.get('cantidad', 1)

            # Find product ordered 3+ times
            for product, count in product_counts.items():
                if count >= 3:
                    return product

            return None

        except Exception as e:
            print(f"❌ Error obteniendo producto favorito para {telefono}: {e}")
            return None


@lru_cache()
def get_firestore_service() -> FirestoreService:
    """Get singleton instance of FirestoreService."""
    return FirestoreService()