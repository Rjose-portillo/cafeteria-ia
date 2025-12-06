"""
Módulo de Auditoría de Costos.
Este script permite inspeccionar "las tripas" de las órdenes recientes en Firestore.
Su función principal es verificar que los campos ocultos de contabilidad (costo_unitario, margen) 
se estén calculando y guardando correctamente en la base de datos, 
permitiendo al desarrollador validar la rentabilidad invisible del sistema.
"""
import firestore
import os
from dotenv import load_dotenv

# Configuración
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# Conexión
try:
    db = firestore.Client(project=PROJECT_ID)
    print(f"🕵️‍♂️ Auditando costos en proyecto: {PROJECT_ID}...\n")
except Exception as e:
    print(f"❌ Error conectando a Firestore: {e}")
    exit()

# Obtener último pedido
pedidos_ref = db.collection('pedidos')
query = pedidos_ref.order_by('fecha_creacion', direction=firestore.Query.DESCENDING).limit(1)
docs = query.stream()

found = False
for doc in docs:
    found = True
    data = doc.to_dict()
    print(f"🧾 ID Pedido: {doc.id}")
    print(f"💰 Total Venta: ${data.get('total')}")
    
    print("\n--- DETALLE DE ITEMS (CON COSTOS INTERNOS) ---")
    items = data.get('items', [])
    for i in items:
        nombre = i.get('nombre_producto')
        precio = i.get('precio_unitario')
        costo = i.get('costo_unitario', 0) # Aquí buscamos el dato clave
        
        # Validación segura de tipos para evitar errores si alguno es None
        precio = float(precio) if precio is not None else 0.0
        costo = float(costo) if costo is not None else 0.0
        
        margen = precio - costo
        print(f"📦 Producto: {nombre}")
        print(f"   - Precio Venta: ${precio}")
        print(f"   - Costo Interno: ${costo} (Calculado al 30%)")
        print(f"   - Ganancia Neta: ${margen}")
        print("-" * 30)

if not found:
    print("❌ No se encontraron pedidos recientes.")
