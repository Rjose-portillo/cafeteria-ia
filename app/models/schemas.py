"""
Pydantic Schemas and Data Models.
Defines the core data structures for the application with Firestore compatibility.
All datetime fields use UTC timezone for consistency.
"""
from enum import Enum
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field, computed_field


class Category(str, Enum):
    """Product categories in the menu."""
    BEBIDA = "bebida"
    ALIMENTO = "alimento"
    POSTRE = "postre"


class OrderStatus(str, Enum):
    """Order lifecycle states."""
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class FirestoreModelMixin:
    """
    Mixin providing Firestore serialization/deserialization methods.
    Ensures consistent data format between Python objects and Firestore documents.
    """
    
    def to_firestore(self) -> Dict[str, Any]:
        """Convert model to Firestore-compatible dictionary."""
        if hasattr(self, 'model_dump'):
            data = self.model_dump()
        else:
            data = self.dict()
        return data

    @classmethod
    def from_firestore(cls, data: Dict[str, Any], doc_id: Optional[str] = None) -> 'FirestoreModelMixin':
        """Create model instance from Firestore document."""
        if doc_id and hasattr(cls, '__fields__') and 'id' in cls.__fields__:
            data['id'] = doc_id
        return cls(**data)


class MenuItem(BaseModel, FirestoreModelMixin):
    """Menu item representation."""
    id: Optional[str] = None
    nombre: str
    precio: float
    categoria: Category = Category.BEBIDA
    descripcion: Optional[str] = None
    tiempo_prep: int = 5  # Minutes
    disponible: bool = True
    modificadores: List[str] = []
    imagen_url: Optional[str] = None


class OrderItem(BaseModel, FirestoreModelMixin):
    """
    Individual item within an order.
    Includes pricing and cost tracking for accounting.
    """
    nombre_producto: str
    cantidad: int = Field(gt=0, description="Quantity must be positive")
    precio_unitario: float = Field(ge=0, description="Unit price")
    costo_unitario: float = Field(default=0.0, description="Unit cost for accounting (30% default)")
    modificadores_seleccionados: List[str] = Field(default_factory=list)
    notas_especiales: Optional[str] = None
    tiempo_prep_unitario: int = Field(default=5, description="Prep time per unit in minutes")

    @computed_field
    @property
    def subtotal(self) -> float:
        """Calculate item subtotal (quantity * unit price)."""
        return self.cantidad * self.precio_unitario
    
    @computed_field
    @property
    def costo_total(self) -> float:
        """Calculate total cost for accounting."""
        return self.cantidad * self.costo_unitario


class Order(BaseModel, FirestoreModelMixin):
    """
    Complete order model with all business logic fields.
    Uses UTC timezone for all datetime fields.
    """
    id: Optional[str] = None
    id_cliente: str = Field(description="Customer phone number or ID")
    
    # Timestamps - CRITICAL: Always use UTC
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Order creation time in UTC"
    )
    
    # Order contents
    items: List[OrderItem] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0)
    
    # Status tracking
    estado: OrderStatus = OrderStatus.PENDIENTE
    
    # Payment
    metodo_pago: str = "pendiente"
    requiere_factura: bool = False
    
    # Time management
    hora_entrega_estimada: Optional[datetime] = None
    hora_entrega_programada: Optional[datetime] = None
    tiempo_preparacion_total: int = Field(default=0, description="Total prep time in minutes")
    
    # Metadata
    notas_orden: Optional[str] = None
    
    def calcular_total(self) -> float:
        """Recalculate order total from items."""
        return sum(item.subtotal for item in self.items)
    
    def calcular_tiempo_prep(self) -> int:
        """Calculate total preparation time from items."""
        return sum(item.tiempo_prep_unitario * item.cantidad for item in self.items)


class ChatMessage(BaseModel, FirestoreModelMixin):
    """
    Chat message for conversation history.
    Stored in Firestore for memory persistence.
    """
    role: str = Field(description="'user' or 'model'")
    content: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Message timestamp in UTC"
    )
    metadata: Optional[Dict[str, Any]] = None


class CustomerProfile(BaseModel, FirestoreModelMixin):
    """
    Customer profile with CRM data.
    Updated by the CRM analysis system.
    """
    id: Optional[str] = None  # Phone number
    nombre: Optional[str] = None
    nivel: str = "Pasante"  # Pasante, Asociado, Magistrado
    total_gastado: float = 0.0
    producto_favorito: Optional[str] = None
    frecuencia_visitas: int = 0
    ultima_visita: Optional[datetime] = None
    preferencias: List[str] = Field(default_factory=list)


# --- API Request/Response Models ---

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    mensaje: str = Field(min_length=1, description="User message")
    telefono: str = Field(min_length=10, description="Customer phone number")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    tipo: str = Field(description="Response type: texto, orden_creada, orden_actualizada, orden_cancelada, error, ignorar")
    mensaje: str
    mensajes: Optional[List[str]] = None  # For multi-bubble responses
    orden: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None