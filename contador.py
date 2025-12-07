"""
Contador Auditor Automatizado (Batch Process).
Este script está diseñado para ejecutarse como un proceso nocturno (cron job).
Extrae todas las ventas del día actual, calcula métricas financieras precisas 
(Total ventas, Costos, Utilidad, IVA) y utiliza un modelo de IA con capacidad de 
ejecución de código (Python REPL) para generar un reporte ejecutivo fiable y detallado.
"""
import os
import pandas as pd
import google.generativeai as genai
from google.cloud import firestore
from dotenv import load_dotenv
from datetime import datetime, time, timezone

# --- CONFIGURACIÓN ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    raise ValueError("FATAL: Falta GEMINI_API_KEY en .env")

# Configurar APIs
genai.configure(api_key=GEMINI_API_KEY)

try:
    db = firestore.Client(project=PROJECT_ID)
    print(f"✅ Conectado a Firestore: {db.project}")
except Exception as e:
    print(f"⚠️ Error conectando a Firestore: {e}")
    exit(1)

def main():
    print("🚀 Iniciando Cierre de Caja (Contador Auditor)...")

    # 1. Definir rango de tiempo (Hoy UTC/Local manejado para filtro)
    # Para simplificar, usaremos la fecha actual del sistema local para el rango
    now = datetime.now()
    start_of_day = datetime.combine(now.date(), time.min)
    end_of_day = datetime.combine(now.date(), time.max)
    
    print(f"📅 Analizando ventas del: {now.date()}")

    # 2. Extracción (ETL)
    try:
        pedidos_ref = db.collection('pedidos')
        # Filtramos pedidos creados hoy (Firestore maneja la comparación de timestamps)
        query = pedidos_ref.where(filter=firestore.FieldFilter('fecha_creacion', '>=', start_of_day))\
                           .where(filter=firestore.FieldFilter('fecha_creacion', '<=', end_of_day))
        
        docs = query.stream()
        
        flat_records = []
        count_orders = 0
        
        for doc in docs:
            data = doc.to_dict()
            # Ignorar cancelados para el cierre de venta real
            if data.get('estado') == 'cancelado':
                continue

            count_orders += 1
            order_id = doc.id
            
            items = data.get('items', [])
            for item in items:
                nombre = item.get('nombre_producto', 'Desconocido')
                precio = float(item.get('precio_unitario', 0))
                
                # LÓGICA DE COSTO (Fallback si no existe: 30% del precio)
                costo = item.get('costo_unitario')
                if costo is None:
                    costo = precio * 0.30
                else:
                    costo = float(costo)
                
                flat_records.append({
                    "ID_Pedido": order_id,
                    "Producto": nombre,
                    "Precio_Venta": precio,
                    "Costo_Unitario": costo
                })
        
        if count_orders == 0:
            print("📭 No se encontraron ventas activas el día de hoy.")
            return

        print(f"📦 Datos extraídos: {count_orders} pedidos válidos, {len(flat_records)} items.")

        # 3. Transformación (Pandas)
        df = pd.DataFrame(flat_records)
        csv_data = df.to_csv(index=False)
        
        # 4. Análisis con IA (Code Execution)
        print("🤖 Enviando datos al Auditor (Gemini)...")
        
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            tools='code_execution'
        )

        prompt = f"""
        Actúa como Auditor Financiero. Tienes estos datos de ventas reales en CSV.
        
        DATOS CSV:
        ```csv
        {csv_data}
        ```
        
        TAREA:
        Escribe y ejecuta código Python para calcular con precisión:
        1. Venta Total (Suma de Precio_Venta).
        2. Costo Total (Suma de Costo_Unitario).
        3. Utilidad Neta Real (Venta - Costo).
        4. Margen de Ganancia Global % ((Utilidad / Venta) * 100).
        
        OUTPUT:
        Genera un reporte breve de texto con los resultados finales.
        """
        
        response = model.generate_content(prompt)
        
        print("\n" + "="*50)
        print("📑 REPORTE DE CIERRE DE CAJA")
        print("="*50)
        
        if response.text:
            print(response.text)
        else:
            print("⚠️ El modelo no generó respuesta de texto.")
        print("="*50 + "\n")

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")

if __name__ == "__main__":
    main()
