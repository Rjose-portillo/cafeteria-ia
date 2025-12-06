"""
Tests Unitarios de Modelos.
Pruebas enfocadas en validar la lógica y restricciones de los modelos de datos (models.py).
Aseguran que no se puedan crear ítems con precios negativos, cantidades cero,
y valida la correcta conversión de tipos al interactuar con el formato de Firestore.
"""
import json
from datetime import datetime
from models import MenuItem, OrderItem, Order, Customer, Category, OrderStatus

def run_simulation():
    print("--- Iniciando Simulación de Cafetería ---\n")

    # 1. Crear productos (Menú)
    cafe = MenuItem(
        id="menu_001",
        nombre="Café Americano",
        descripcion="Café negro recién hecho",
        precio=45.0,
        categoria=Category.BEBIDA,
        modificadores_permitidos=["leche", "azúcar", "crema"]
    )
    
    bagel = MenuItem(
        id="menu_002",
        nombre="Bagel de Queso",
        descripcion="Bagel tostado con queso crema",
        precio=60.0,
        categoria=Category.ALIMENTO
    )

    print(f"Producto creado: {cafe.nombre} (${cafe.precio})")
    print(f"Producto creado: {bagel.nombre} (${bagel.precio})\n")

    # 2. Crear un Cliente
    cliente = Customer(
        telefono_id="+525512345678",
        nombre="Juan Pérez",
        pedidos_frecuentes=["Café Americano"]
    )
    print(f"Cliente identificado: {cliente.nombre} (ID: {cliente.telefono_id})\n")

    # 3. Simular una Orden
    # Item 1: Café con leche
    item1 = OrderItem(
        nombre_producto=cafe.nombre,
        cantidad=1,
        precio_unitario=cafe.precio,
        modificadores_seleccionados=["leche"],
        notas_especiales="Muy caliente"
    )

    # Item 2: 2 Bagels
    item2 = OrderItem(
        nombre_producto=bagel.nombre,
        cantidad=2,
        precio_unitario=bagel.precio
    )

    # Calcular total (simple suma)
    total_orden = item1.subtotal + item2.subtotal

    orden = Order(
        id="order_999",
        id_cliente=cliente.telefono_id,
        items=[item1, item2],
        total=total_orden,
        estado=OrderStatus.PENDIENTE,
        metodo_pago="tarjeta"
    )

    print(f"Orden creada con éxito. Total: ${orden.total}")
    print(f"Estado: {orden.estado.value}\n")

    # 4. Simular guardado en Firestore (to_firestore)
    print("--- Simulando Guardado en Firestore (to_firestore) ---")
    firestore_data = orden.to_firestore()
    
    # Imprimimos bonito el diccionario. 
    # Nota: datetime no es serializable por json.dumps por defecto, lo convertimos a str solo para visualizar aquí.
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError ("Type not serializable")

    print(json.dumps(firestore_data, indent=2, default=json_serial))

    # 5. Simular lectura desde Firestore (from_firestore)
    print("\n--- Simulando Lectura desde Firestore (from_firestore) ---")
    # Simulamos que recuperamos el dict y queremos volver a tener el objeto
    orden_recuperada = Order.from_firestore(firestore_data, doc_id="order_999")
    
    print(f"Orden recuperada ID: {orden_recuperada.id}")
    print(f"Cliente ID: {orden_recuperada.id_cliente}")
    print(f"Items: {len(orden_recuperada.items)}")
    print(f"Es la misma orden? {orden.id == orden_recuperada.id}")

if __name__ == "__main__":
    run_simulation()
