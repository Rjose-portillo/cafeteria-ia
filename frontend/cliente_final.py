"""
Frontend Cliente - WhatsApp Business Style Chat Interface.
Complete mobile app experience with floating action button, fixed header, and native UX.
"""
import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Justicia y Café ☕",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- WHATSAPP BUSINESS STYLE CSS - COMPLETE OVERRIDE ---
st.markdown("""
<style>
    /* Hide all Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Full mobile app background - WhatsApp style */
    .stApp {
        background: #e5ddd5;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Mobile container - centered like a phone screen */
    .main .block-container {
        background: white;
        border-radius: 0;
        padding: 0;
        margin: 0 auto;
        width: 100%;
        max-width: 400px;
        min-height: 100vh;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        border: none;
        position: relative;
    }

    /* SUPER VISIBLE SIDEBAR TOGGLE - FLOATING ACTION BUTTON */
    [data-testid="stSidebarCollapsedControl"] {
        background: #2E7D32 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 10000 !important;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4) !important;
        border: 3px solid white !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }

    /* Custom hamburger icon */
    [data-testid="stSidebarCollapsedControl"]::before {
        content: "☰" !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* Hide default arrow */
    [data-testid="stSidebarCollapsedControl"] svg {
        display: none !important;
    }

    /* Hover effect */
    [data-testid="stSidebarCollapsedControl"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.6) !important;
        background: #1B5E20 !important;
    }

    /* Pulse animation to draw attention */
    @keyframes fabPulse {
        0%, 100% {
            box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
        }
        50% {
            box-shadow: 0 6px 30px rgba(46, 125, 50, 0.8), 0 0 20px rgba(46, 125, 50, 0.4);
        }
    }

    [data-testid="stSidebarCollapsedControl"] {
        animation: fabPulse 2s ease-in-out infinite !important;
    }

    /* FIXED HEADER - WhatsApp Business Style */
    .whatsapp-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #075e54 0%, #128c7e 100%);
        color: white;
        padding: 16px 20px;
        z-index: 999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 60px;
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
        border: 2px solid white;
    }

    .header-info {
        display: flex;
        flex-direction: column;
    }

    .header-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 12px;
        opacity: 0.8;
        margin: 2px 0 0 0;
    }

    /* Chat container with proper spacing */
    .chat-messages {
        padding: 80px 16px 100px 16px;
        min-height: calc(100vh - 180px);
        max-height: calc(100vh - 180px);
        overflow-y: auto;
        background: #e5ddd5;
    }

    /* WHATSAPP-STYLE CHAT BUBBLES */
    .message-bubble {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 75%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        animation: bubbleSlideIn 0.3s ease-out;
    }

    @keyframes bubbleSlideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* User messages - RIGHT ALIGNED, GREEN */
    .user-message {
        background: #dcf8c6;
        color: #303030;
        float: right;
        clear: both;
        margin-left: 25%;
        margin-right: 8px;
        border-radius: 15px 15px 0 15px;
        text-align: right;
    }

    /* Bot messages - LEFT ALIGNED, WHITE */
    .bot-message {
        background: #ffffff;
        color: #303030;
        float: left;
        clear: both;
        margin-right: 25%;
        margin-left: 8px;
        border-radius: 15px 15px 15px 0;
        text-align: left;
    }

    /* Typing indicator */
    .typing-indicator {
        background: #ffffff;
        border-radius: 15px 15px 15px 0;
        padding: 12px 16px;
        float: left;
        clear: both;
        margin-right: 25%;
        margin-left: 8px;
        margin-bottom: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
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
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px dashed #dee2e6;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        position: relative;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
        animation: ticketAppear 0.5s ease-out;
        clear: both;
    }

    @keyframes ticketAppear {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Ticket perforation effect */
    .order-card::before,
    .order-card::after {
        content: "";
        position: absolute;
        width: 12px;
        height: 12px;
        background: #e5ddd5;
        border-radius: 50%;
        border: 2px dashed #dee2e6;
    }

    .order-card::before {
        top: -6px;
        left: 20px;
    }

    .order-card::after {
        bottom: -6px;
        right: 20px;
    }

    .order-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e9ecef;
    }

    .order-title {
        font-size: 14px;
        font-weight: 700;
        color: #075e54;
        margin: 0;
    }

    .order-id {
        font-size: 11px;
        color: #666;
        font-family: 'Courier New', monospace;
        background: #f8f9fa;
        padding: 2px 6px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }

    .order-status {
        background: #4caf50;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 11px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .order-status::before {
        content: "✓";
        font-size: 12px;
    }

    .order-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px dashed #e9ecef;
        font-size: 13px;
    }

    .order-item:last-child {
        border-bottom: none;
    }

    .item-name {
        font-weight: 500;
        color: #333;
    }

    .item-price {
        font-weight: 600;
        color: #2E7D32;
        font-family: 'Courier New', monospace;
        background: #e8f5e8;
        padding: 2px 6px;
        border-radius: 6px;
    }

    .order-total {
        background: #075e54;
        color: white;
        padding: 10px 12px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 15px;
        font-weight: 700;
        margin-top: 12px;
        font-family: 'Courier New', monospace;
    }

    .order-time {
        text-align: center;
        margin-top: 10px;
        padding: 6px 10px;
        background: #fff3cd;
        border-radius: 6px;
        font-size: 11px;
        color: #856404;
        font-weight: 500;
        border: 1px solid #ffeaa7;
    }

    /* Fixed bottom input area */
    .input-area {
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
        border-radius: 20px;
        padding: 8px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 2px solid #e9ecef;
        box-shadow: 2px 0 12px rgba(0,0,0,0.1);
        padding-top: 80px;
    }

    /* Button styling */
    .stButton > button {
        background: #25d366;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 2px 6px rgba(37, 211, 102, 0.2);
    }

    .stButton > button:hover {
        background: #20c157;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
    }

    /* Success messages */
    .stSuccess {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #2e7d32;
        font-weight: 500;
    }

    /* Error messages */
    .stError {
        background: #ffebee;
        border: 1px solid #f44336;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #c62828;
        font-weight: 500;
    }

    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 4px;
    }

    .chat-messages::-webkit-scrollbar-track {
        background: transparent;
    }

    .chat-messages::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 2px;
    }

    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #999;
    }

    /* Responsive design */
    @media (min-width: 768px) {
        .main .block-container {
            max-width: 450px;
        }

        .whatsapp-header {
            padding: 18px 24px;
            height: 64px;
        }

        .chat-messages {
            padding: 84px 20px 120px 20px;
        }

        [data-testid="stSidebarCollapsedControl"] {
            width: 64px !important;
            height: 64px !important;
            top: 24px !important;
            left: 24px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def render_typing_indicator():
    """Render WhatsApp-style typing indicator."""
    st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    """, unsafe_allow_html=True)

def render_message(role: str, content: str):
    """Render WhatsApp-style message bubble."""
    bubble_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f'<div class="message-bubble {bubble_class}">{content}</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

def simulate_typing(text: str, placeholder):
    """Simulate typing effect with WhatsApp-style bubbles."""
    displayed_text = ""
    html_template = '<div class="message-bubble bot-message">{}</div><div style="clear: both;"></div>'

    for char in text:
        displayed_text += char
        placeholder.markdown(html_template.format(displayed_text + "▌"), unsafe_allow_html=True)
        time.sleep(0.03)  # Typing speed

    # Final render without cursor
    placeholder.markdown(html_template.format(displayed_text), unsafe_allow_html=True)

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

        mods_text = f" + {', '.join(mods)}" if mods else ""
        items_html += f"""
            <div class="order-item">
                <span class="item-name">{cantidad}x {nombre}{mods_text}</span>
                <span class="item-price">${precio:.0f}</span>
            </div>
        """

    card_html = f"""
        <div class="order-card">
            <div class="order-header">
                <div class="order-title">🍽️ Pedido Confirmado</div>
                <div class="order-id">#{order_id[-6:]}</div>
                <div class="order-status">Confirmado</div>
            </div>
            {items_html}
            <div class="order-total">
                <span>Total</span>
                <span>${total:.0f}</span>
            </div>
            <div class="order-time">
                ⏱️ Tiempo estimado: {tiempo} min
            </div>
        </div>
        <div style="clear: both;"></div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

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

# --- MAIN APP - WHATSAPP BUSINESS STYLE ---

# Fixed WhatsApp-style Header
st.markdown("""
    <div class="whatsapp-header">
        <div class="header-left">
            <div class="header-avatar">☕</div>
            <div class="header-info">
                <div class="header-title">Justicia y Café</div>
                <div class="header-subtitle">En línea</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! 👋 Soy Pepe, tu mesero virtual. ¿Qué se te antoja hoy?",
        "tipo": "texto"
    }]

# Chat Messages Container
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

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
st.markdown('<div class="input-area">', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Escribe tu mensaje...", key="chat_input"):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", content=prompt)

    # Show typing indicator
    typing_placeholder = st.empty()
    render_typing_indicator()

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