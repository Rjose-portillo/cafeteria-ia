"""
Orders Router - Endpoints for order management.
Used by kitchen display and admin interfaces.
"""
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import OrderStatus
from app.services.firestore_service import get_firestore_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/active", response_model=List[Dict[str, Any]])
async def get_active_orders():
    """
    Get all active orders (pending and in preparation).
    Used by the kitchen display system.
    """
    firestore = get_firestore_service()
    orders = await firestore.get_active_orders()
    return orders


@router.get("/pending", response_model=List[Dict[str, Any]])
async def get_pending_orders():
    """Get all pending orders."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.PENDIENTE)
    return orders


@router.get("/in-preparation", response_model=List[Dict[str, Any]])
async def get_orders_in_preparation():
    """Get all orders currently being prepared."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.EN_PREPARACION)
    return orders


@router.get("/ready", response_model=List[Dict[str, Any]])
async def get_ready_orders():
    """Get all orders ready for pickup."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.LISTO)
    return orders


@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, new_status: OrderStatus):
    """
    Update the status of an order.
    Used by kitchen staff to move orders through the workflow.
    """
    firestore = get_firestore_service()
    
    success = await firestore.update_order(order_id, {"estado": new_status.value})
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden {order_id} no encontrada"
        )
    
    return {"message": f"Orden {order_id} actualizada a {new_status.value}"}


@router.patch("/{order_id}/start-preparation")
async def start_preparation(order_id: str):
    """Mark an order as being prepared."""
    return await update_order_status(order_id, OrderStatus.EN_PREPARACION)


@router.patch("/{order_id}/mark-ready")
async def mark_ready(order_id: str):
    """Mark an order as ready for pickup."""
    return await update_order_status(order_id, OrderStatus.LISTO)


@router.patch("/{order_id}/mark-delivered")
async def mark_delivered(order_id: str):
    """Mark an order as delivered."""
@router.get("/status/{telefono}")
async def get_customer_order_status(telefono: str):
    """
    Get the current order status for a customer.
    Returns the most recent order and its status.
    """
    firestore = get_firestore_service()

    # Get pending order first
    pending = await firestore.get_pending_order(telefono)
    if pending:
        doc, data = pending
        return {
            "order_id": doc.id,
            "status": data.get('estado', 'desconocido'),
            "items": data.get('items', []),
            "total": data.get('total', 0),
            "tiempo_estimado": data.get('tiempo_preparacion_total', 0),
            "hora_entrega_estimada": data.get('hora_entrega_estimada')
        }

    # If no pending order, check recent completed orders
    if firestore.is_connected:
        try:
            query = firestore._db.collection('pedidos')\
                .where(filter=firestore._db.field_filter("id_cliente", "==", telefono))\
                .where(filter=firestore._db.field_filter("estado", "in", ["entregado", "listo"]))\
                .order_by('fecha_creacion', direction=firestore._db.Query.DESCENDING)\
                .limit(1)

            docs = list(query.stream())
            if docs:
                data = docs[0].to_dict()
                return {
                    "order_id": docs[0].id,
                    "status": data.get('estado', 'desconocido'),
                    "items": data.get('items', []),
                    "total": data.get('total', 0),
                    "message": "Tu pedido anterior ya fue entregado. ¿Quieres ordenar algo más?"
                }
        except Exception as e:
            print(f"Error checking recent orders: {e}")

    return {"status": "no_orders", "message": "No tienes pedidos activos. ¿Qué te gustaría ordenar?"}
    return await update_order_status(order_id, OrderStatus.ENTREGADO)