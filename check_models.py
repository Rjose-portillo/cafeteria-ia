"""
Herramienta de Diagnóstico de Modelos.
Este pequeño script utilitario sirve para validar la integridad de la estructura de datos.
Permite instanciar y probar los modelos Pydantic (Order, Customer, etc.) de forma aislada 
para asegurar que las reglas de tipo y validación estén funcionando antes de integrarlos al backend.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Buscando modelos disponibles para tu API Key ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nombre: {m.name}")
except Exception as e:
    print(f"Error al listar modelos: {e}")
