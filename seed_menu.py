"""
Script de Sembrado de Datos (Seed).
Utilidad para poblar la base de datos Firestore con el menú inicial de la cafetería.
Define el catálogo de productos (Cafe, Postres, Alimentos) con sus precios, descripciones
y tiempos de preparación, subiéndolos a la colección 'menu' para que el sistema tenga
información real con la que trabajar.
"""
import os
from dotenv import load_dotenv
from google.cloud import firestore

# 1. Cargar variables de entorno
load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

if not project_id:
    raise ValueError("Error: No se encontró GOOGLE_CLOUD_PROJECT en el archivo .env")

print(f"--- Iniciando proceso de poblado para: {project_id} ---")

# 2. Inicializar cliente de Firestore
# Al usar gcloud init previamente, no necesitamos pasar credenciales explícitas aquí,
# la librería las busca en el entorno local automáticamente.
db = firestore.Client(project=project_id)

# 3. Definir el Catálogo de Productos (Datos Maestros)
menu_items = [
    # --- BEBIDAS ---
    {
        "id": "beb_flatwhite",
        "nombre": "Flat White Artesanal",
        "descripcion": "Doble shot de espresso con una fina capa de leche texturizada.",
        "precio": 65.0,
        "categoria": "bebida",
        "tiempo_prep": 4,
        "disponible": True
    },
    {
        "id": "beb_coldbrew",
        "nombre": "Cold Brew 12hrs",
        "descripcion": "Infusión en frío por 12 horas, notas a chocolate y avellana.",
        "precio": 70.0,
        "categoria": "bebida",
        "tiempo_prep": 2,
        "disponible": True
    },
    {
        "id": "beb_matcha",
        "nombre": "Matcha Latte Ceremonial",
        "descripcion": "Té matcha grado ceremonial importado de Japón con leche de avena.",
        "precio": 85.0,
        "categoria": "bebida",
        "tiempo_prep": 6,
        "disponible": True
    },
    {
        "id": "beb_espresso",
        "nombre": "Espresso Doble",
        "descripcion": "Extracción precisa de 18g de café de especialidad (Veracruz).",
        "precio": 45.0,
        "categoria": "bebida",
        "tiempo_prep": 3,
        "disponible": True
    },
    {
        "id": "beb_chemex",
        "nombre": "Método Chemex (2 tazas)",
        "descripcion": "Filtrado manual, cuerpo ligero y alta claridad de sabores.",
        "precio": 90.0,
        "categoria": "bebida",
        "tiempo_prep": 10,
        "disponible": True
    },
    
    # --- ALIMENTOS ---
    {
        "id": "ali_bagel_salmon",
        "nombre": "Bagel de Salmón Curado",
        "descripcion": "Bagel de masa madre, queso crema, alcaparras y salmón ahumado.",
        "precio": 145.0,
        "categoria": "alimento",
        "tiempo_prep": 12,
        "disponible": True
    },
    {
        "id": "ali_avocado",
        "nombre": "Avocado Toast",
        "descripcion": "Pan campesino, aguacate machacado, huevo pochado y semillas de girasol.",
        "precio": 110.0,
        "categoria": "alimento",
        "tiempo_prep": 10,
        "disponible": True
    },
    {
        "id": "ali_croissant",
        "nombre": "Croissant de Almendra",
        "descripcion": "Relleno de frangipane y cubierto de almendras tostadas.",
        "precio": 60.0,
        "categoria": "alimento",
        "tiempo_prep": 2, # Solo calentar
        "disponible": True
    },
    {
        "id": "ali_panini",
        "nombre": "Panini Caprese",
        "descripcion": "Mozzarella fresca, jitomate, pesto de albahaca en ciabatta.",
        "precio": 125.0,
        "categoria": "alimento",
        "tiempo_prep": 15,
        "disponible": True
    },
    {
        "id": "ali_bowl",
        "nombre": "Açaí Bowl",
        "descripcion": "Base de açaí orgánico con granola de la casa, plátano y fresas.",
        "precio": 130.0,
        "categoria": "alimento",
        "tiempo_prep": 8,
        "disponible": True
    }
]

def seed_database():
    collection_ref = db.collection("menu")
    batch = db.batch() # Usamos batch para eficiencia en red
    
    print(f"Preparando {len(menu_items)} items para subir...")
    
    for item in menu_items:
        doc_id = item.pop("id") # Extraemos el ID para usarlo como llave del documento
        doc_ref = collection_ref.document(doc_id)
        
        # set(item, merge=True) actualiza campos si existe, crea si no.
        # En batch operations, set funciona igual.
        batch.set(doc_ref, item, merge=True)
        print(f" -> Encolado: {doc_id}")

    # Ejecutar todas las escrituras de una sola vez
    print("Enviando datos a Firestore...")
    batch.commit()
    print("✅ ¡Carga de menú completada exitosamente!")

if __name__ == "__main__":
    seed_database()