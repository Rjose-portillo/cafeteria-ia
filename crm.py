import os
import pandas as pd
from google.cloud import firestore
from dotenv import load_dotenv
from collections import Counter

# --- 1. CONFIGURACIÓN ---
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    # Intento de fallback o advertencia
    print("⚠️ ADVERTENCIA: GOOGLE_CLOUD_PROJECT no está definido en .env.")

try:
    db = firestore.Client(project=PROJECT_ID)
    print(f"✅ Conectado a Firestore: {db.project}")
except Exception as e:
    print(f"❌ Error conectando a Firestore: {e}")
    exit()

def get_product_mode(products_list):
    """Calcula el producto más frecuente (moda) de una lista."""
    if not products_list:
        return "Ninguno"
    c = Counter(products_list)
    # most_common(1) devuelve [(elemento, conteo)]
    return c.most_common(1)[0][0]

def main():
    print("🔄 Descargando pedidos desde Firestore...")
    
    # --- 2. EXTRACCIÓN ---
    orders_ref = db.collection('pedidos')
    docs = orders_ref.stream()
    
    # Listas para construir DataFrames
    orders_data = [] # Para datos a nivel orden (Total, ID orden)
    items_data = []  # Para datos a nivel producto (aplanado)

    count = 0
    for doc in docs:
        count += 1
        order = doc.to_dict()
        
        # Datos clave de la orden
        o_id = order.get('id', doc.id)
        c_id = order.get('id_cliente', 'Desconocido')
        total = order.get('total', 0.0)
        
        # Guardamos nivel orden
        orders_data.append({
            'order_id': o_id,
            'id_cliente': c_id,
            'total': total
        })
        
        # Procesamos items para "aplanar" y saber qué pidió
        # En Firestore 'items' es una lista de diccionarios
        items = order.get('items', [])
        for item in items:
            p_name = item.get('nombre_producto', 'Desconocido')
            items_data.append({
                'id_cliente': c_id,
                'producto': p_name
            })

    print(f"📊 Procesados {count} documentos.")

    if not orders_data:
        print("⚠️ No hay datos de pedidos para analizar.")
        return

    # --- 3. PROCESAMIENTO CON PANDAS ---
    
    # DF de Órdenes (para montos y frecuencia)
    df_orders = pd.DataFrame(orders_data)
    
    # DF de Items (para encontrar favorito)
    df_items = pd.DataFrame(items_data)

    # 3.1 Agrupación de métricas financieras
    # Agrupamos por cliente y calculamos suma de ventas y cuenta de órdenes únicas
    client_metrics = df_orders.groupby('id_cliente').agg(
        TotalGastado=('total', 'sum'),
        Frecuencia=('order_id', 'nunique') # nunique por si hubiera duplicados de datos, aunque stream es único docs
    ).reset_index()

    # 3.2 Cálculo del ticket promedio
    client_metrics['TicketPromedio'] = client_metrics['TotalGastado'] / client_metrics['Frecuencia']

    # 3.3 Cálculo del producto favorito
    # Para cada cliente, calculamos la moda de sus productos
    # GroupBy id_cliente -> apply funcion custom
    favorite_products = df_items.groupby('id_cliente')['producto'].apply(list).reset_index()
    favorite_products['ProductoFavorito'] = favorite_products['producto'].apply(get_product_mode)
    
    # 3.4 Merge de métricas y productos favoritos
    final_df = pd.merge(client_metrics, favorite_products[['id_cliente', 'ProductoFavorito']], on='id_cliente')

    # --- 4. SEGMENTACIÓN (LÓGICA DE NEGOCIO) ---
    def segmentar_cliente(row):
        f = row['Frecuencia']
        if f > 5:
            return 'Magistrado'
        elif f >= 3:
            return 'Asociado'
        else:
            return 'Pasante'

    final_df['Nivel'] = final_df.apply(segmentar_cliente, axis=1)

    # Ordenar por Total Gastado
    final_df = final_df.sort_values(by='TotalGastado', ascending=False)

    # Limpieza de formato (opcional, redondeo)
    final_df['TicketPromedio'] = final_df['TicketPromedio'].round(2)

    # --- 5. OUTPUT ---
    print("\n" + "="*50)
    print("📈 REPORTE DE FIDELIZACIÓN DE CLIENTES")
    print("="*50)
    print(final_df.to_string(index=False))
    
    
    # Exportar CSV
    output_file = "clientes_vip.csv"
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 Archivo exportado exitosamente: {output_file}")

    print("\n🔄 Sincronizando perfiles con Firestore (Colección 'clientes')...")
    
    # Iteramos sobre el DataFrame para guardar en Firestore
    # Convertimos a diccionario orientado a records
    records = final_df.to_dict(orient='records')
    
    for record in records:
        cliente_id = record['id_cliente']
        
        # Preparamos datos para guardar
        perfil = {
            "nivel": record['Nivel'],
            "total_gastado": float(record['TotalGastado']),
            "producto_favorito": record['ProductoFavorito'],
            "ultima_actualizacion": firestore.SERVER_TIMESTAMP
        }
        
        # Guardar/Actualizar en colección 'clientes'
        db.collection('clientes').document(cliente_id).set(perfil, merge=True)
        print(f"✅ Perfil actualizado: {cliente_id} -> {record['Nivel']}")

    print("✨ Sincronización CRM completada.")

if __name__ == "__main__":
    main()
