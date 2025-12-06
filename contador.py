import os
import pandas as pd
import google.generativeai as genai
from google.cloud import firestore
from dotenv import load_dotenv
from datetime import datetime, time
import logging

# --- CONFIGURACIÓN ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not GEMINI_API_KEY:
    raise ValueError("FATAL: Falta GEMINI_API_KEY en .env")

if not PROJECT_ID:
    raise ValueError("FATAL: Falta GOOGLE_CLOUD_PROJECT en .env")

# Configurar APIs
genai.configure(api_key=GEMINI_API_KEY)

try:
    db = firestore.Client(project=PROJECT_ID)
    logging.info(f"✅ Conectado a Firestore: {db.project}")
except Exception as e:
    logging.error(f"⚠️ Error conectando a Firestore: {e}")
    exit(1)

def main():
    logging.info("🚀 Iniciando proceso batch: Contador Auditor (Diario)")

    # 1. Definir rango de tiempo (Hoy)
    now = datetime.now()
    start_of_day = datetime.combine(now.date(), time.min)
    end_of_day = datetime.combine(now.date(), time.max)
    
    logging.info(f"📅 Analizando periodo: {start_of_day} - {end_of_day}")

    # 2. Extracción (ETL)
    try:
        pedidos_ref = db.collection('pedidos')
        # Filtramos por fecha de creación
        query = pedidos_ref.where(filter=firestore.FieldFilter('fecha_creacion', '>=', start_of_day))\
                           .where(filter=firestore.FieldFilter('fecha_creacion', '<=', end_of_day))
        
        docs = query.stream()
        
        flat_records = []
        count_orders = 0
        
        for doc in docs:
            count_orders += 1
            data = doc.to_dict()
            order_id = doc.id
            
            # Hora de creación
            timestamp = data.get('fecha_creacion')
            # Firestore devuelve datetime con zona horaria, simplificamos a string HH:MM
            hora_str = timestamp.strftime('%H:%M') if timestamp else "00:00"
            
            items = data.get('items', [])
            for item in items:
                nombre = item.get('nombre_producto', 'Desconocido')
                precio = float(item.get('precio_unitario', 0))
                # Costo unitario (si no existe, asumimos 0 para la auditoría y reportamos fallo en ganancia)
                costo = float(item.get('costo_unitario', 0))
                
                flat_records.append({
                    "ID_Pedido": order_id,
                    "Hora": hora_str,
                    "Producto": nombre,
                    "Precio_Venta": precio,
                    "Costo_Unitario": costo
                })
        
        if count_orders == 0:
            logging.warning("📭 No hay ventas registradas en el día de hoy.")
            return

        logging.info(f"📦 Procesados {count_orders} pedidos con {len(flat_records)} items.")

        # 3. Transformación (Pandas)
        df = pd.DataFrame(flat_records)
        csv_data = df.to_csv(index=False)
        
        # 4. Análisis con IA (Code Execution)
        logging.info("🤖 Enviando datos al Contador Auditor (Gemini)...")
        
        # Configuración del modelo con Code Execution
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            tools='code_execution'
        )

        prompt = f"""
        Actúa como un Contador Auditor experto. Tienes acceso a los datos de ventas de hoy en formato CSV.
        
        DATOS CSV:
        ```csv
        {csv_data}
        ```
        
        TAREA:
        Usa código Python para calcular con EXACTITUD:
        1. Total de Ventas ($).
        2. Utilidad Bruta Real ($) (Calculada como Suma de [Precio_Venta - Costo_Unitario]).
        3. Identificar la Hora Pico (la hora con más items vendidos).
        4. Calcular IVA estimado (16% del ingreso total).
        
        OUTPUT:
        Genera un REPORTE EJECUTIVO de texto resumiendo los hallazgos.
        Sé formal y preciso.
        """
        
        response = model.generate_content(prompt)
        
        print("\n" + "="*60)
        print("📑 REPORTE NOCTURNO DE VENTAS")
        print("="*60)
        
        # Si hay partes con código ejecutado, Gemini suele mostrar el texto final en .text
        # A veces el output está estructurado, pero .text suele contener la respuesta sintetizada.
        if response.text:
            print(response.text)
        else:
            print("⚠️ El modelo no generó respuesta de texto.")
            
        print("="*60 + "\n")

    except Exception as e:
        logging.error(f"❌ Error crítico en el proceso batch: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
