
"""
Frontend para Cliente Final (Streamlit).
Esta aplicación simula la interfaz móvil del usuario (tipo WhatsApp/Messenger).
Gestiona la interacción del cliente con el mesero virtual, enviando mensajes al backend,
recibiendo respuestas, y mostrando feedback visual (globos, tickets) cuando se confirman órdenes.
Manitene el historial de chat en sesión local.
"""
import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Justicia y Café",
    page_icon="☕",
    layout="centered"
)

# Estilos personalizados (opcional)
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título y Descripción
st.title("☕ Justicia y Café")
st.caption("Ordena tu café favorito con nuestro asistente virtual.")

# Sidebar: Configuración del Usuario
with st.sidebar:
    st.header("👤 Datos del Cliente")
    # Teléfono simulado (clave para el ID del cliente en backend)
    telefono = st.text_input("Tu número de teléfono", value="+525599999999")
    
    st.divider()
    
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()

# Inicializar estado de la sesión para el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Si hubo un mensaje de éxito especial guardado (opcional, por simplicidad guardamos solo texto,
        # pero podríamos renderizar bloques especiales si reconstruimos el historial complejo)

# Capturar entrada del usuario
if prompt := st.chat_input("Hola, quiero un café..."):
    # 1. Agregar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Preparar llamada al Backend
    api_url = "http://127.0.0.1:8000/chat"
    payload = {
        "mensaje": prompt,
        "telefono": telefono
    }

    # 3. Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("💭 Consultando con el barista..."):
                response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                tipo = data.get("tipo", "texto")
                texto_respuesta = data.get("mensaje", "No recibí respuesta.")
                orden = data.get("orden", {})
                
                # Mostrar el mensaje principal
                message_placeholder.markdown(texto_respuesta)
                
                # Guardar respuesta en historial
                st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
                
                # --- Lógica Especial: Orden Creada ---
                if tipo == "orden_creada":
                    # Efecto visual
                    st.balloons()
                    
                    # Detalles de la orden
                    order_id = orden.get("id", "N/A")
                    total = orden.get("total", 0.0)
                    items = orden.get("items", [])
                    
                    # Mensaje de éxito destacado
                    st.success(f"✅ **Pedido Confirmado** | ID: `{order_id}`")
                    st.metric(label="Total a Pagar", value=f"${total:,.2f}")
                    
                    # Mostrar resumen de items
                    with st.expander("🧾 Ver detalles del ticket", expanded=True):
                        for item in items:
                            nombre = item.get("nombre_producto", "Producto")
                            cant = item.get("cantidad", 1)
                            precio = item.get("precio_unitario", 0)
                            mods = item.get("modificadores_seleccionados", [])
                            
                            st.markdown(f"**{cant}x {nombre}** - ${precio*cant:,.2f}")
                            if mods:
                                st.caption(f"   *Mods: {', '.join(mods)}*")
                    
            else:
                error_msg = f"⚠️ Error del servider: {response.status_code}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except requests.exceptions.ConnectionError:
            error_msg = "🔌 No se pudo conectar con el backend. ¿Está corriendo en el puerto 8000?"
            message_placeholder.error(error_msg)
            # No guardamos errores de conexión en historial permanente a menos que se desee
        except Exception as e:
            error_msg = f"❌ Ocurrió un error inesperado: {str(e)}"
            message_placeholder.error(error_msg)
