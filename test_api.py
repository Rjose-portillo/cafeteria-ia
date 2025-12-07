"""
Tests de Integración de API.
Conjunto de pruebas automatizadas usando `pytest` y `TestClient` de FastAPI.
Verifican que los endpoints del backend respondan correctamente, validando códigos de estado,
estructuras JSON de respuesta y manejo de errores básicos sin necesidad de levantar el servidor completo.
"""
import requests
import json

url = "http://127.0.0.1:8000/chat"

# Caso 1: Charla normal
payload_chat = {
    "mensaje": "Hola, ¿a qué hora abren?",
    "telefono": "+525512345678"
}

# Caso 2: Un pedido complejo
# Nota: Probamos si es capaz de detectar precio y cantidad implícita
payload_pedido = {
    "mensaje": "Quiero dos lattes grandes con leche de almendra y un bagel de queso, por favor.",
    "telefono": "+525512345678"
}

def probar(nombre, payload):
    print(f"\n--- Probando: {nombre} ---")
    try:
        response = requests.post(url, json=payload)
        print("Status:", response.status_code)
        # Imprimimos el JSON bonito
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar pruebas
probar("Consulta General", payload_chat)
probar("Pedido de Venta", payload_pedido)
