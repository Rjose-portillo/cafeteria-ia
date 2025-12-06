from enum import Enum
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class Category(str, Enum):
    BEBIDA = "bebida"
    ALIMENTO = "alimento"
    POSTRE = "postre"

class OrderStatus(str, Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class FirestoreModelMixin:
    def to_firestore(self) -> Dict[str, Any]:
        if hasattr(self, 'model_dump'):
            data = self.model_dump()
        else:
            data = self.dict()
        return data

    @classmethod
    def from_firestore(cls, data: Dict[str, Any], doc_id: Optional[str] = None) -> 'FirestoreModelMixin':
        if doc_id and 'id' in cls.__fields__:
            data['id'] = doc_id
        return cls(**data)

class OrderItem(BaseModel, FirestoreModelMixin):
    nombre_producto: str
    cantidad: int = Field(gt=0)
    precio_unitario: float
    costo_unitario: float = 0.0 # [NUEVO] Para contabilidad
    modificadores_seleccionados: List[str] = []
    notas_especiales: Optional[str] = None

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

class Order(BaseModel, FirestoreModelMixin):
    id: Optional[str] = None
    id_cliente: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    items: List[OrderItem]
    total: float
    estado: OrderStatus = OrderStatus.PENDIENTE
    metodo_pago: str = "pendiente"
    requiere_factura: bool = False # [NUEVO]

class ChatMessage(BaseModel, FirestoreModelMixin): 
    """[NUEVO] Modelo para la memoria del chat"""
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
