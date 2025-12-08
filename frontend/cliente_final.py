"""
Frontend Cliente - WhatsApp Style + Super Botón de Menú.
Combina la estética limpia de chat con la navegación intuitiva del botón flotante.
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

# --- CSS HACKING: WHATSAPP STYLE + SUPER BOTÓN ---
st.markdown("""
<style>
    /* 1. Ocultar elementos nativos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. SUPER BOTÓN DE MENÚ (EL QUE TE GUSTABA) */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #25d366 !important; /* Verde WhatsApp */
        color: white !important;
        border-radius: 0 50px 50px 0 !important; /* Semicírculo */
        padding: 10px !important;
        width: 60px !important;
        height: 60px !important;
        top: 80px !important; /* Bajamos un poco para no tapar el header */
        left: 0 !important;
        z-index: 100000 !important;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border: 2px solid white !important;
    }

    /* Icono de la flecha */
    [data-testid="stSidebarCollapsedControl"] svg {
        height: 30px !important;
        width: 30px !important;
        fill: white !important;
        stroke: white !important;
    }

    /* Efecto Hover */
    [data-testid="stSidebarCollapsedControl"]:hover {
        width: 75px !important;
        background-color: #128c7e !important;
        transform: scale(1.05) !important;
    }

    /* Animación de Pulso */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(37, 211, 102, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
    }
    
    [data-testid="stSidebarCollapsedControl"] {
        animation: pulse-green 2s infinite;
    }

    /* 3. ESTILOS GENERALES (WhatsApp) */
    .stApp {
        background: #e5ddd5;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Contenedor del Chat */
    .main .block-container {
        padding-top: 60px; /* Espacio para el header */
        padding-bottom: 80px; /* Espacio para el input */
        max-width: 600px;
    }

    /* HEADER FIJO */
    .whatsapp-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #075e54;
        color: white;
        padding: 10px 20px;
        z-index: 9999; /* Mayor que el botón */
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        height: 60px;
    }

    .header-avatar {
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-size: 20px;
    }

    .header-info h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: white;
    }
    .header-info p {
        margin: 0;
        font-size: 12px;
        opacity: 0.8;
    }

    /* BURBUJAS DE CHAT */
    .message-bubble {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 75%;
        font-size: 15px;
        line-height: 1.4;
        position: relative;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }

    .user-message {
        background: #dcf8c6;
        float: right;
        clear: both;
        border-top-right-radius: 0;
    }

    .bot-message {
        background: #ffffff;
        float: left;
        clear: both;
        border-top-left-radius: 0;
    }

    /* INPUT FIJO */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px;
        background: #f0f0f0;
        z-index: 1000;
    }
    
    /* Order Card */
    .order-card {
        background: white;
        border: 1px dashed #ccc;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        clear: both;
        float: left;
        width: 100%;
        max-width: 85%;
    }

    /* SIDEBAR STYLING - DARK THEME */
    [data-testid="stSidebar"] {
        background: #262730 !important; /* Gunmetal - Streamlit dark */
        border-right: 1px solid #404040 !important;
        box-shadow: 2px 0 8px rgba(0,0,0,0.3) !important;
    }

    /* Sidebar content text */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* Pure white for main text */
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Sidebar subheaders and labels */
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        color: #E0E0E0 !important; /* Light gray for secondary text */
    }

    /* Input fields - dark background */
    [data-testid="stSidebar"] input {
        background: #0E1117 !important; /* Almost black for depth */
        border: 1px solid #404040 !important;
        border-radius: 6px !important;
        color: #FFFFFF !important;
        padding: 8px 12px !important;
    }

    /* Input placeholders */
    [data-testid="stSidebar"] input::placeholder {
        color: #A0A0A0 !important;
    }

    /* Buttons in sidebar */
    [data-testid="stSidebar"] button {
        background: #25d366 !important; /* WhatsApp green */
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: #128c7e !important;
        transform: translateY(-1px) !important;
    }

    /* Menu items styling */
    [data-testid="stSidebar"] .menu-item {
        color: #FFFFFF !important;
        margin-bottom: 6px !important;
        font-size: 14px !important;
    }

    /* Menu prices - bright green */
    [data-testid="stSidebar"] .menu-price {
        color: #25d366 !important; /* Bright green */
        font-weight: 700 !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Menu categories */
    [data-testid="stSidebar"] .menu-cat {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        margin: 15px 0 8px 0 !important;
        border-bottom: 2px solid #25d366 !important;
        padding-bottom: 4px !important;
    }

    /* Custom menu cards in sidebar */
    [data-testid="stSidebar"] .menu-card {
        background: #1a1a2e !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 12px !important;
    }

    /* Success messages in sidebar */
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(76, 175, 80, 0.2) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 6px !important;
        color: #81c784 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def render_typing_indicator():
    placeholder = st.empty()
    placeholder.markdown('<div class="message-bubble bot-message" style="color:#888;">Escribiendo... ✍️</div>', unsafe_allow_html=True)
    return placeholder

def simulate_typing(text: str, placeholder):
    full_text = ""
    html_tpl = '<div class="message-bubble bot-message">{}</div><div style="clear:both;"></div>'
    for chunk in text.split(" "):
        full_text += chunk + " "
        placeholder.markdown(html_tpl.format(full_text + "▌"), unsafe_allow_html=True)
        time.sleep(0.04)
    placeholder.markdown(html_tpl.format(full_text), unsafe_allow_html=True)

def render_order_card(orden: dict):
    total = orden.get('total', 0)
    order_id = orden.get('id', '???')
    items = orden.get('items', [])
    tiempo = orden.get('tiempo_preparacion_total', 15)
    
    items_html = ""
    for item in items:
        mods = f"<br><small style='color:#666'>+ {', '.join(item['modificadores_seleccionados'])}</small>" if item.get('modificadores_seleccionados') else ""
        items_html += f"""
        <div style="display:flex; justify-content:space-between; border-bottom:1px dashed #eee; padding:5px 0;">
            <span><b>{item['cantidad']}x</b> {item['nombre_producto']} {mods}</span>
            <span>${item['precio_unitario'] * item['cantidad']:.0f}</span>
        </div>"""

    card = f"""
    <div class="order-card">
        <div style="color:#075e54; margin-bottom:10px; font-weight:bold;">✅ Pedido Confirmado <span style="float:right; font-weight:normal; font-size:0.8em; background:#eee; padding:2px 5px; border-radius:4px;">#{order_id[:6]}</span></div>
        {items_html}
        <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:1.2em; font-weight:bold;">
            <span>Total:</span><span>${total:.0f}</span>
        </div>
        <div style="background:#e8f5e8; color:#2e7d32; padding:5px; border-radius:5px; text-align:center; margin-top:10px; font-size:0.9em;">
            ⏱️ Tiempo estimado: {tiempo} min
        </div>
    </div>
    """
    st.markdown(card, unsafe_allow_html=True)

# --- SIDEBAR - DARK THEME ---
with st.sidebar:
    # Header with logo and title
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #25d366;">
        <div style="font-size: 48px; margin-bottom: 10px;">☕</div>
        <h1 style="color: #FFFFFF; margin: 0; font-size: 20px; font-weight: 700;">Justicia y Café</h1>
        <div style="color: #E0E0E0; font-size: 12px; margin-top: 4px;">Sistema de Pedidos</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Configuration Section
    st.markdown('<div style="color: #FFFFFF; font-size: 16px; font-weight: 600; margin-bottom: 12px;">⚙️ Configuración</div>', unsafe_allow_html=True)

    telefono = st.text_input(
        "📞 Tu Teléfono:",
        value="+525599999999",
        help="Número para identificarte en el sistema"
    )

    api_url = st.text_input(
        "🌐 API URL:",
        value="http://127.0.0.1:8000/chat",
        disabled=True,
        help="URL del servidor backend"
    )

    # Clear chat button
    if st.button("🧹 Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("✅ Historial limpiado")
        st.rerun()

    st.markdown("---")

    # Menu Section
    st.markdown('<div style="color: #FFFFFF; font-size: 16px; font-weight: 600; margin-bottom: 12px;">📜 Menú del Día</div>', unsafe_allow_html=True)

    # Menu with improved styling
    menu_html = """
    <div class="menu-card">
        <div class="menu-cat">☕ BEBIDAS</div>
        <div class="menu-item">• Latte <span class="menu-price">$45</span></div>
        <div class="menu-item">• Flat White <span class="menu-price">$65</span></div>
        <div class="menu-item">• Cold Brew <span class="menu-price">$70</span></div>

        <div class="menu-cat">🥐 ALIMENTOS</div>
        <div class="menu-item">• Croissant <span class="menu-price">$40</span></div>
        <div class="menu-item">• Bagel Salmón <span class="menu-price">$145</span></div>
        <div class="menu-item">• Panini <span class="menu-price">$125</span></div>
    </div>

    <div style="margin-top: 20px; padding: 12px; background: #1a1a2e; border-radius: 8px; border: 1px solid #404040;">
        <div style="color: #E0E0E0; font-size: 12px; text-align: center;">
            💡 <strong>Tip:</strong> Escribe tu pedido en lenguaje natural.<br>
            Ej: "Quiero un latte y un croissant"
        </div>
    </div>
    """

    st.markdown(menu_html, unsafe_allow_html=True)

# --- MAIN APP ---

# Header Fijo
st.markdown("""
    <div class="whatsapp-header">
        <div class="header-avatar">🤖</div>
        <div class="header-info">
            <h1>Justicia y Café</h1>
            <p>En línea • Pepe</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Inicializar estado
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "¡Hola! 👋 Soy Pepe. ¿Qué se te antoja hoy?", 
        "tipo": "texto"
    }]

# Renderizar Historial
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_message("user", msg["content"])
    else:
        render_message("bot", msg["content"])
        if msg.get("orden"):
            render_order_card(msg["orden"])

# Input de Chat
if prompt := st.chat_input("Escribe tu pedido..."):
    # 1. Mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    # 2. Indicador
    typing = render_typing_indicator()

    # 3. Backend Call
    try:
        payload = {"mensaje": prompt, "telefono": telefono}
        response = requests.post(api_url, json=payload, timeout=30)
        typing.empty()

        if response.status_code == 200:
            data = response.json()
            tipo = data.get("tipo", "texto")
            mensajes = data.get("mensajes", [data.get("mensaje", "...")])
            orden = data.get("orden")

            # Procesar mensajes
            full_txt = ""
            for txt in mensajes:
                ph = st.empty()
                simulate_typing(txt, ph)
                full_txt += txt + " "
                st.markdown('<div style="clear:both;"></div>', unsafe_allow_html=True)
            
            # Mostrar Orden
            if tipo in ["orden_creada", "orden_actualizada"] and orden:
                render_order_card(orden)
                st.balloons()
            
            st.session_state.messages.append({
                "role": "assistant", "content": full_txt, "orden": orden, "tipo": tipo
            })
        else:
            st.error(f"Error {response.status_code}")

    except Exception as e:
        typing.empty()
        st.error(f"Error: {e}")
    
    st.rerun() # Para limpiar input y hacer scroll