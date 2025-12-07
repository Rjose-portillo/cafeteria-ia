"""
Frontend Cliente - Premium Mobile Chat Experience (WhatsApp/Uber Style).
Features:
- Floating Action Button (FAB) for sidebar toggle
- Fixed mobile app header
- WhatsApp-style chat bubbles with tails
- Ticket-style order cards
- Native mobile UX
"""
import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Justicia y Café ☕",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM MOBILE CSS - WHATSAPP/UBER STYLE ---
st.markdown("""
<style>
    /* Hide Streamlit branding completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Full mobile app background */
    .stApp {
        background: #f0f2f5;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        overflow-x: hidden;
    }

    /* Main container - full mobile experience */
    .main .block-container {
        background: white;
        border-radius: 0;
        padding: 0;
        margin: 0;
        width: 100vw;
        max-width: 100vw;
        min-height: 100vh;
        box-shadow: none;
        border: none;
        position: relative;
    }

    /* FIXED MOBILE HEADER - WhatsApp Style */
    .mobile-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #075e54 0%, #128c7e 100%);
        color: white;
        padding: 12px 16px;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 56px;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-avatar {
        width: 40px;
        height: 40px;
        background: #25d366;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
    }

    .header-info h1 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.2;
    }

    .header-status {
        font-size: 12px;
        opacity: 0.8;
        margin: 0;
    }

    /* SUPER VISIBLE SIDEBAR TOGGLE - FLOATING ACTION BUTTON */
    .sidebar-toggle-fab {
        position: fixed !important;
        top: 16px !important;
        left: 16px !important;
        width: 48px !important;
        height: 48px !important;
        background: #ffffff !important;
        border: 3px solid #25d366 !important;
        border-radius: 50% !important;
        z-index: 9999 !important;
        box-shadow: 0 4px 16px rgba(37, 211, 102, 0.4) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 20px !important;
        color: #25d366 !important;
        font-weight: bold !important;
    }

    .sidebar-toggle-fab:hover {
        transform: scale(1.1) !important;
        background: #25d366 !important;
        color: #ffffff !important;
        box-shadow: 0 6px 24px rgba(37, 211, 102, 0.6) !important;
    }

    .sidebar-toggle-fab:active {
        transform: scale(0.95) !important;
    }

    /* Chat container with proper spacing for fixed header */
    .chat-container {
        padding: 76px 16px 100px 16px; /* Space for header + bottom input */
        min-height: calc(100vh - 176px);
        max-height: calc(100vh - 176px);
        overflow-y: auto;
        background: #f0f2f5;
    }

    /* WHATSAPP-STYLE CHAT BUBBLES */
    .message-wrapper {
        margin-bottom: 12px;
        display: flex;
        animation: messageSlideIn 0.3s ease-out;
    }

    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* User messages - RIGHT ALIGNED, GREEN WHATSAPP STYLE */
    .user-message-wrapper {
        justify-content: flex-end;
        margin-left: 20%;
    }

    .user-message {
        background: #dcf8c6;
        color: #303030;
        padding: 8px 12px;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin-right: 8px;
    }

    /* Bot messages - LEFT ALIGNED, WHITE WITH SHADOW */
    .bot-message-wrapper {
        justify-content: flex-start;
        margin-right: 20%;
    }

    .bot-message {
        background: #ffffff;
        color: #303030;
        padding: 8px 12px;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin-left: 8px;
    }

    /* Typing indicator - WhatsApp style */
    .typing-wrapper {
        justify-content: flex-start;
        margin-right: 20%;
        margin-bottom: 12px;
    }

    .typing-indicator {
        background: #ffffff;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin-left: 8px;
        display: flex;
        gap: 4px;
    }

    .typing-dot {
        width: 6px;
        height: 6px;
        background: #999;
        border-radius: 50%;
        animation: typingBounce 1.4s infinite ease-in-out;
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }

    /* TICKET-STYLE ORDER CARD */
    .order-card {
        background: linear-gradient(135deg, #fefefe 0%, #f9f9f9 100%);
        border: 2px dashed #e0e0e0;
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        position: relative;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        animation: ticketSlideIn 0.5s ease-out;
    }

    @keyframes ticketSlideIn {
        from {
            opacity: 0;
            transform: translateY(-10px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .order-card::before {
        content: "";
        position: absolute;
        top: -2px;
        left: 20px;
        width: 20px;
        height: 20px;
        background: #f0f2f5;
        border-radius: 50%;
        border: 2px dashed #e0e0e0;
    }

    .order-card::after {
        content: "";
        position: absolute;
        bottom: -2px;
        right: 20px;
        width: 20px;
        height: 20px;
        background: #f0f2f5;
        border-radius: 50%;
        border: 2px dashed #e0e0e0;
    }

    .order-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e0e0e0;
    }

    .order-title {
        font-size: 16px;
        font-weight: 700;
        color: #075e54;
        margin: 0;
    }

    .order-id {
        font-size: 12px;
        color: #666;
        font-family: monospace;
        background: #f0f0f0;
        padding: 4px 8px;
        border-radius: 12px;
        margin-top: 4px;
    }

    .order-status {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .order-status::before {
        content: "✓";
        font-size: 14px;
    }

    .order-items {
        margin-bottom: 16px;
    }

    .order-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }

    .order-item:last-child {
        border-bottom: none;
    }

    .item-info {
        flex: 1;
    }

    .item-name {
        font-weight: 600;
        color: #333;
        font-size: 14px;
        margin-bottom: 2px;
    }

    .item-details {
        font-size: 12px;
        color: #666;
        font-style: italic;
    }

    .item-price {
        font-weight: 700;
        color: #075e54;
        font-size: 14px;
        background: #e8f5e8;
        padding: 4px 8px;
        border-radius: 8px;
    }

    .order-total {
        background: #075e54;
        color: white;
        padding: 12px 16px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 16px;
        font-weight: 700;
        margin-top: 16px;
    }

    .order-time {
        text-align: center;
        margin-top: 12px;
        padding: 8px 12px;
        background: #fff3cd;
        border-radius: 8px;
        font-size: 12px;
        color: #856404;
        font-weight: 600;
        border: 1px solid #ffeaa7;
    }

    /* FIXED BOTTOM INPUT AREA */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #f0f2f5;
        padding: 12px 16px;
        border-top: 1px solid #e0e0e0;
        z-index: 1000;
    }

    .input-wrapper {
        max-width: 400px;
        margin: 0 auto;
        background: white;
        border-radius: 24px;
        padding: 8px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
        box-shadow: 2px 0 12px rgba(0,0,0,0.1);
        padding-top: 80px; /* Space for mobile header */
    }

    /* Button styling */
    .stButton > button {
        background: #25d366;
        color: white;
        border: none;
        border-radius: 24px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 2px 8px rgba(37, 211, 102, 0.2);
    }

    .stButton > button:hover {
        background: #20c157;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
    }

    /* Success messages */
    .stSuccess {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #2e7d32;
        font-weight: 500;
    }

    /* Error messages */
    .stError {
        background: #ffebee;
        border: 1px solid #f44336;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #c62828;
        font-weight: 500;
    }

    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 4px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: transparent;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 2px;
    }

    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #999;
    }

    /* Responsive adjustments */
    @media (min-width: 768px) {
        .mobile-header {
            padding: 16px 24px;
            height: 64px;
        }

        .chat-container {
            padding: 84px 24px 120px 24px;
        }

        .sidebar-toggle-fab {
            top: 20px !important;
            left: 20px !important;
            width: 52px !important;
            height: 52px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def render_typing_indicator():
    """Render WhatsApp-style typing indicator."""
    return st.markdown("""
        <div class="message-wrapper typing-wrapper">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_message(role: str, content: str):
    """Render WhatsApp-style message bubble."""
    wrapper_class = "user-message-wrapper" if role == "user" else "bot-message-wrapper"
    bubble_class = "user-message" if role == "user" else "bot-message"

    st.markdown(f"""
        <div class="message-wrapper {wrapper_class}">
            <div class="{bubble_class}">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def simulate_typing(text: str, placeholder):
    """Simulate typing effect with WhatsApp-style bubbles."""
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(f"""
            <div class="message-wrapper bot-message-wrapper">
                <div class="bot-message">{displayed_text}▌</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)  # Typing speed

    # Final render without cursor
    placeholder.markdown(f"""
        <div class="message-wrapper bot-message-wrapper">
            <div class="bot-message">{displayed_text}</div>
        </div>
    """, unsafe_allow_html=True)

def render_order_card(orden: dict):
    """Render ticket-style order confirmation card."""
    order_id = orden.get('id', 'N/A')
    total = orden.get('total', 0)
    items = orden.get('items', [])
    tiempo = orden.get('tiempo_preparacion_total', orden.get('tiempo_estimado', 15))

    items_html = ""
    for item in items:
        nombre = item.get('nombre_producto', 'Producto')
        cantidad = item.get('cantidad', 1)
        precio = item.get('precio_unitario', 0)
        mods = item.get('modificadores_seleccionados', [])

        mods_html = f'<div class="item-details">+ {", ".join(mods)}</div>' if mods else ''

        items_html += f"""
            <div class="order-item">
                <div class="item-info">
                    <div class="item-name">{cantidad}x {nombre}</div>
                    {mods_html}
                </div>
                <div class="item-price">${precio * cantidad:.2f}</div>
            </div>
        """

    st.markdown(f"""
        <div class="order-card">
            <div class="order-header">
                <div>
                    <div class="order-title">🍽️ Pedido Confirmado</div>
                    <div class="order-id">#{order_id[-8:]}</div>
                </div>
                <div class="order-status">Confirmado</div>
            </div>
            <div class="order-items">
                {items_html}
            </div>
            <div class="order-total">
                <span>Total</span>
                <span>${total:.2f}</span>
            </div>
            <div class="order-time">
                ⏱️ Tiempo estimado: ~{tiempo} minutos
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (CONFIGURACIÓN & MENÚ) ---
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #075e54 0%, #128c7e 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 8px;">☕</div>
        <h2 style="margin: 0; font-size: 18px; font-weight: 700;">Justicia y Café</h2>
        <div style="font-size: 14px; opacity: 0.9; margin-top: 4px;">Configuración</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📱 Configuración")
    telefono = st.text_input("Tu teléfono", value="+525599999999", label_visibility="collapsed")
    api_url = st.text_input("API URL", value="http://127.0.0.1:8000/chat", disabled=True, label_visibility="collapsed")

    st.markdown("---")

    if st.button("🗑️ Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("✅ Chat limpiado")
        st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Menú Rápido")

    # Menu items with WhatsApp-style cards
    st.markdown("""
    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
        <div style="color: #075e54; font-weight: 700; font-size: 14px; margin-bottom: 12px;">☕ BEBIDAS</div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e9ecef;">
            <span style="font-weight: 500;">• Latte</span>
            <span style="color: #25d366; font-weight: 700;">$45</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e9ecef;">
            <span style="font-weight: 500;">• Flat White</span>
            <span style="color: #25d366; font-weight: 700;">$65</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
            <span style="font-weight: 500;">• Cold Brew</span>
            <span style="color: #25d366; font-weight: 700;">$70</span>
        </div>
    </div>

    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
        <div style="color: #075e54; font-weight: 700; font-size: 14px; margin-bottom: 12px;">🥐 ALIMENTOS</div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e9ecef;">
            <span style="font-weight: 500;">• Croissant</span>
            <span style="color: #25d366; font-weight: 700;">$40</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e9ecef;">
            <span style="font-weight: 500;">• Bagel Salmón</span>
            <span style="color: #25d366; font-weight: 700;">$145</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
            <span style="font-weight: 500;">• Panini</span>
            <span style="color: #25d366; font-weight: 700;">$125</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN APP - PREMIUM MOBILE EXPERIENCE ---

# Fixed Mobile Header
st.markdown("""
    <div class="mobile-header">
        <div class="header-left">
            <div class="header-avatar">☕</div>
            <div class="header-info">
                <h1>Justicia y Café</h1>
                <div class="header-status">En línea</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! 👋 Soy Pepe, tu mesero virtual. ¿Qué te puedo servir hoy?",
        "tipo": "texto"
    }]

# Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Render chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    if role == "user":
        render_message("user", content)
    else:
        render_message("bot", content)

        # Render order card if present
        if message.get("orden"):
            render_order_card(message["orden"])

st.markdown('</div>', unsafe_allow_html=True)

# Fixed Bottom Input Area
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Escribe tu mensaje...", key="chat_input"):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    # Show typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
        <div class="message-wrapper typing-wrapper">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # API call
    try:
        payload = {"mensaje": prompt, "telefono": telefono}
        response = requests.post(api_url, json=payload, timeout=30)

        # Clear typing indicator
        typing_placeholder.empty()

        if response.status_code == 200:
            data = response.json()
            tipo = data.get("tipo", "texto")
            mensajes = data.get("mensajes", [data.get("mensaje", "...")])
            orden = data.get("orden")

            # Handle multi-message responses
            if mensajes and len(mensajes) > 1:
                for msg in mensajes:
                    response_placeholder = st.empty()
                    simulate_typing(msg, response_placeholder)
                    time.sleep(0.3)
                final_content = " ".join(mensajes)
            else:
                # Single message with typing effect
                response_placeholder = st.empty()
                single_msg = mensajes[0] if mensajes else "..."
                simulate_typing(single_msg, response_placeholder)
                final_content = single_msg

            # Store in history
            msg_data = {
                "role": "assistant",
                "content": final_content,
                "tipo": tipo
            }

            # Handle order responses
            if tipo in ["orden_creada", "orden_actualizada"] and orden:
                msg_data["orden"] = orden
                render_order_card(orden)
                st.balloons()

            st.session_state.messages.append(msg_data)

        else:
            error_msg = f"⚠️ Error del servidor: {response.status_code}"
            render_message("bot", error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "tipo": "error"
            })

    except requests.exceptions.ConnectionError:
        typing_placeholder.empty()
        error_msg = "🔌 No se pudo conectar con el servidor. ¿Está corriendo el backend?"
        render_message("bot", error_msg)
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg,
            "tipo": "error"
        })

    except Exception as e:
        typing_placeholder.empty()
        error_msg = f"❌ Error: {str(e)}"
        render_message("bot", error_msg)
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg,
            "tipo": "error"
        })

    # Rerun to update UI
    time.sleep(0.5)
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)