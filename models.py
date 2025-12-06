from enum import Enum
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class Category(str, Enum):
    """Categorías disponibles para los productos del menú."""
    BEBIDA = "bebida"
    ALIMENTO = "alimento"

class OrderStatus(str, Enum):
    """Estados posibles de un pedido."""
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"

class FirestoreModelMixin:
    """
    Mixin para agregar capacidades de conversión a diccionarios compatibles con Firestore.
    """
    
    def to_firestore(self) -> Dict[str, Any]:
        """
        Convierte la instancia del modelo a un diccionario para Firestore.
        Maneja la conversión de Enums y Datetimes si es necesario.
        Pydantic v2 model_dump suele manejar esto bien, pero Firestore acepta datetime nativo.
        """
        # model_dump (v2) o dict (v1). Usaremos model_dump si está disponible, sino dict.
        # Asumimos Pydantic v2 por ser el estándar actual, pero mantenemos compatibilidad simple.
        if hasattr(self, 'model_dump'):
            data = self.model_dump()
        else:
            data = self.dict()
            
        # Firestore maneja datetime nativo, así que no necesitamos convertirlo a string
        # a menos que sea un requerimiento específico. Pydantic por defecto mantiene los objetos
        # si no se especifica mode='json'.
        return data

    @classmethod
    def from_firestore(cls, data: Dict[str, Any], doc_id: Optional[str] = None) -> 'FirestoreModelMixin':
        """
        Crea una instancia del modelo desde un diccionario de Firestore.
        Si el modelo tiene un campo 'id' y se pasa doc_id, se inyecta.
        """
        if doc_id and 'id' in cls.__fields__:
            data['id'] = doc_id
        return cls(**data)

class MenuItem(BaseModel, FirestoreModelMixin):
    """
    Representa un artículo en el menú de la cafetería.
    """
    id: Optional[str] = Field(default=None, description="ID único del producto (generalmente el ID del documento en Firestore)")
    nombre: str
    descripcion: str
    precio: float
    categoria: Category
    modificadores_permitidos: List[str] = Field(default_factory=list, description="Lista de modificadores como 'leche deslactosada', 'sin azúcar'")

class OrderItem(BaseModel, FirestoreModelMixin):
    """
    Representa un ítem dentro de una orden.
    """
    nombre_producto: str
    cantidad: int = Field(gt=0, description="Cantidad del producto")
    precio_unitario: float
    modificadores_seleccionados: List[str] = Field(default_factory=list)
    notas_especiales: Optional[str] = None

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal de este ítem."""
        return self.cantidad * self.precio_unitario

class Order(BaseModel, FirestoreModelMixin):
    """
    Representa un pedido realizado por un cliente.
    """
    id: Optional[str] = Field(default=None, description="ID único de la orden")
    id_cliente: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    items: List[OrderItem]
    total: float
    estado: OrderStatus = OrderStatus.PENDIENTE
    metodo_pago: str

class Customer(BaseModel, FirestoreModelMixin):
    """
    Representa a un cliente de la cafetería.
    """
    telefono_id: str = Field(..., description="ID del cliente basado en su teléfono, usado como clave")
    nombre: str
    fecha_registro: datetime = Field(default_factory=datetime.now)
    ultima_visita: Optional[datetime] = None
    pedidos_frecuentes: List[str] = Field(default_factory=list, description="Lista de IDs o nombres de productos frecuentes")
