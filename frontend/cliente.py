import sys
import os
import streamlit as st
import requests
import time
import uuid
from datetime import datetime

# Agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page configuration - MOBILE FIRST
st.set_page_config(
    page_title="Justicia y Café ☕",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- WHATSAPP BUSINESS CLONE CSS - PIXEL PERFECT ---
st.markdown("""
<style>
    /* Hide all Streamlit branding completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* WhatsApp beige background - EXACT MATCH */
    .stApp {
        background: #e5ddd5 !important;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Mobile container - FULL SCREEN APP EXPERIENCE */
    .main .block-container {
        background: #e5ddd5;
        border-radius: 0;
        padding: 0;
        padding-top: 120px !important;
        margin: 0;
        width: 100vw;
        max-width: 100vw;
        min-height: 100vh;
        box-shadow: none;
        border: none;
        position: relative;
    }

    /* WHATSAPP GREEN FAB - VISIBLE AND PULSING */
    [data-testid="stSidebarCollapsedControl"] {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 56px !important;
        height: 56px !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 10000 !important;
        box-shadow: 0 4px 16px rgba(37, 211, 102, 0.4) !important;
        border: 3px solid white !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        font-size: 20px !important;
        font-weight: bold !important;
        animation: fabPulse 2s ease-in-out infinite !important;
    }

    @keyframes fabPulse {
        0%, 100% {
            box-shadow: 0 4px 16px rgba(37, 211, 102, 0.4);
        }
        50% {
            box-shadow: 0 6px 24px rgba(37, 211, 102, 0.8), 0 0 16px rgba(37, 211, 102, 0.4);
        }
    }

    [data-testid="stSidebarCollapsedControl"]::before {
        content: "☰" !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.6) !important;
    }

    /* WHATSAPP HEADER - FIXED AND BEAUTIFUL */
    .whatsapp-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #075e54;
        color: white;
        padding: 12px 16px;
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
        color: white;
    }

    .header-subtitle {
        font-size: 12px;
        opacity: 0.8;
        margin: 2px 0 0 0;
        color: white;
    }

    /* CHAT CONTAINER - SCROLLABLE AREA */
    .chat-messages {
        padding: 20px 16px 120px 16px;
        min-height: calc(100vh - 180px);
        overflow-y: auto;
        background: #e5ddd5;
    }

    /* WHATSAPP-STYLE CHAT BUBBLES - PIXEL PERFECT */
    .message-bubble {
        padding: 8px 12px;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 75%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
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

    /* USER MESSAGES - GREEN BUBBLES, RIGHT ALIGNED */
    .user-message {
        background: #dcf8c6;
        color: #303030;
        float: right;
        clear: both;
        margin-left: 25%;
        margin-right: 8px;
        border-radius: 18px 18px 4px 18px;
        text-align: right;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* BOT MESSAGES - WHITE BUBBLES, LEFT ALIGNED */
    .bot-message {
        background: #ffffff;
        color: #303030;
        float: left;
        clear: both;
        margin-right: 25%;
        margin-left: 8px;
        border-radius: 18px 18px 18px 4px;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* TYPING INDICATOR - WHATSAPP STYLE */
    .typing-indicator {
        background: #ffffff;
        border-radius: 18px 18px 18px 4px;
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

    /* MENU CARD - BEAUTIFUL CHAT DISPLAY */
    .menu-chat-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        position: relative;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: menuSlideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        clear: both;
        float: left;
        max-width: 85%;
        border: 1px solid #25d366;
    }

    @keyframes menuSlideUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .menu-chat-header {
        text-align: center;
        border-bottom: 2px solid #25d366;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .menu-chat-title {
        font-size: 18px;
        font-weight: bold;
        color: #25d366;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .menu-chat-subtitle {
        font-size: 12px;
        color: #a0a0a0;
        margin: 4px 0 0 0;
    }

    .menu-chat-category {
        color: #e94560;
        font-size: 16px;
        font-weight: 700;
        margin: 16px 0 8px 0;
        border-bottom: 2px solid #e94560;
        padding-bottom: 4px;
    }

    .menu-chat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #404040;
        font-size: 14px;
    }

    .menu-chat-item:last-child {
        border-bottom: none;
    }

    .menu-chat-item-name {
        color: #ffffff;
        font-weight: 500;
        flex: 1;
    }

    .menu-chat-item-price {
        color: #25d366;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        font-size: 16px;
    }

    /* PHYSICAL TICKET RECEIPT - AUTHENTIC */
    .order-card {
        background: #ffffff;
        border: 2px solid #333;
        border-radius: 0 0 8px 8px;
        padding: 20px;
        margin: 16px 0;
        position: relative;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        animation: ticketSlideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        clear: both;
        font-family: 'Courier New', monospace;
        float: left;
        max-width: 85%;
    }

    @keyframes ticketSlideUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
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
        left: 0;
        right: 0;
        height: 10px;
        background: #e5ddd5;
        clip-path: polygon(0% 100%, 5% 0%, 10% 100%, 15% 0%, 20% 100%, 25% 0%, 30% 100%, 35% 0%, 40% 100%, 45% 0%, 50% 100%, 55% 0%, 60% 100%, 65% 0%, 70% 100%, 75% 0%, 80% 100%, 85% 0%, 90% 100%, 95% 0%, 100% 100%);
    }

    .order-header {
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .order-title {
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .order-id {
        font-size: 12px;
        color: #666;
        margin: 5px 0 0 0;
    }

    .order-date {
        font-size: 10px;
        color: #999;
        margin: 2px 0 0 0;
    }

    .order-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px dashed #ccc;
        font-size: 12px;
    }

    .order-item:last-child {
        border-bottom: none;
    }

    .item-name {
        font-weight: bold;
        color: #333;
    }

    .item-price {
        color: #333;
        font-weight: bold;
    }

    .order-total {
        background: #333;
        color: white;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        margin-top: 15px;
        border-radius: 4px;
    }

    .order-time {
        text-align: center;
        margin-top: 12px;
        padding: 8px;
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        font-size: 11px;
        color: #856404;
        font-weight: bold;
    }

    .order-footer {
        text-align: center;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px dashed #ccc;
        font-size: 10px;
        color: #666;
    }

    /* BOTTOM INPUT AREA - WHATSAPP STYLE */
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
        border-radius: 24px;
        padding: 8px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* SIDEBAR - DARK THEME */
    [data-testid="stSidebar"] {
        background: #262730 !important;
        border-right: 1px solid #404040 !important;
        box-shadow: 2px 0 8px rgba(0,0,0,0.3) !important;
        padding-top: 80px !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        color: #E0E0E0 !important;
    }

    [data-testid="stSidebar"] input {
        background: #0E1117 !important;
        border: 1px solid #404040 !important;
        border-radius: 6px !important;
        color: #FFFFFF !important;
        padding: 8px 12px !important;
    }

    [data-testid="stSidebar"] input::placeholder {
        color: #A0A0A0 !important;
    }

    [data-testid="stSidebar"] button {
        background: #25d366 !important;
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

    /* MENU ITEMS - VISUAL ATTRACTION */
    .menu-item {
        color: #FFFFFF !important;
        margin-bottom: 6px !important;
        font-size: 14px !important;
    }

    .menu-price {
        color: #25d366 !important;
        font-weight: 700 !important;
        font-family: 'Courier New', monospace !important;
    }

    .menu-cat {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        margin: 15px 0 8px 0 !important;
        border-bottom: 2px solid #25d366 !important;
        padding-bottom: 4px !important;
    }

    .menu-card {
        background: #1a1a2e !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 12px !important;
    }

    /* SUCCESS/ERROR MESSAGES */
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(76, 175, 80, 0.2) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 6px !important;
        color: #81c784 !important;
    }

    [data-testid="stSidebar"] .stError {
        background: rgba(244, 67, 54, 0.2) !important;
        border: 1px solid #f44336 !important;
        border-radius: 6px !important;
        color: #ef5350 !important;
    }

    /* SCROLLBAR */
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

    /* RESPONSIVE DESIGN */
    @media (min-width: 768px) {
        .main .block-container {
            max-width: 450px;
            margin: 20px auto;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }

        .whatsapp-header {
            padding: 16px 20px;
            height: 64px;
            border-radius: 20px 20px 0 0;
        }

        .chat-messages {
            padding: 84px 20px 120px 20px;
        }

        [data-testid="stSidebarCollapsedControl"] {
            top: 40px !important;
            left: 40px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- API CONFIGURATION ---
API_BASE_URL = "http://localhost:8000"

# --- MENU DATA ---
MENU_DATA = {
    "bebidas": [
        {"nombre": "Latte", "precio": 45, "descripcion": "Café espresso con leche vaporizada"},
        {"nombre": "Flat White", "precio": 65, "descripcion": "Doble espresso con microfoam"},
        {"nombre": "Cold Brew", "precio": 70, "descripcion": "Café frío infusionado 12 horas"},
        {"nombre": "Cappuccino", "precio": 50, "descripcion": "Espresso, leche y espuma perfecta"},
        {"nombre": "Americano", "precio": 35, "descripcion": "Espresso diluido con agua caliente"}
    ],
    "alimentos": [
        {"nombre": "Croissant", "precio": 40, "descripcion": "Hojaldre francés recién horneado"},
        {"nombre": "Bagel Salmón", "precio": 145, "descripcion": "Bagel con salmón ahumado y cream cheese"},
        {"nombre": "Panini", "precio": 125, "descripcion": "Panini tostado con jamón y queso"},
        {"nombre": "Muffin Arándanos", "precio": 55, "descripcion": "Muffin casero con arándanos frescos"},
        {"nombre": "Tostada Aguacate", "precio": 85, "descripcion": "Pan artesanal con aguacate y tomate"}
    ],
    "postres": [
        {"nombre": "Cheesecake", "precio": 95, "descripcion": "Cheesecake cremoso con frutos rojos"},
        {"nombre": "Brownie", "precio": 65, "descripcion": "Brownie de chocolate con helado de vainilla"},
        {"nombre": "Tiramisú", "precio": 85, "descripcion": "Clásico italiano con café y mascarpone"},
        {"nombre": "Macaron Mix", "precio": 120, "descripcion": "Selección de macarons artesanales"}
    ]
}

# --- HELPER FUNCTIONS ---

@st.cache_data(ttl=300)
def fetch_menu_from_api(api_url):
    """Fetch menu from backend API with fallback."""
    try:
        response = requests.get(f"{api_url}/menu", timeout=5)
        if response.status_code == 200:
            items = response.json()
            # Organize by category
            menu = {"bebidas": [], "alimentos": [], "postres": []}
            for item in items:
                cat = item.get('categoria', 'otros').lower()
                # Map backend categories to frontend keys if needed
                if cat in ['bebidas', 'bebida']:
                    menu["bebidas"].append(item)
                elif cat in ['alimentos', 'alimento', 'comida']:
                    menu["alimentos"].append(item)
                elif cat in ['postres', 'postre']:
                    menu["postres"].append(item)
            return menu
    except Exception as e:
        print(f"Error fetching menu: {e}")

    return MENU_DATA

def render_menu_card():
    """Generate beautiful menu card HTML for chat display"""
    menu_data = fetch_menu_from_api(API_BASE_URL)

    menu_html = """
    <div class="menu-chat-card">
        <div class="menu-chat-header">
            <div class="menu-chat-title">📜 MENÚ DEL DÍA</div>
            <div class="menu-chat-subtitle">Justicia y Café</div>
        </div>
    """
    
    # Bebidas
    if menu_data.get("bebidas"):
        menu_html += '<div class="menu-chat-category">☕ BEBIDAS</div>'
        for item in menu_data["bebidas"]:
            menu_html += f"""
        <div class="menu-chat-item">
            <span class="menu-chat-item-name">{item['nombre']}</span>
            <span class="menu-chat-item-price">${item['precio']}</span>
        </div>
        """
    
    # Alimentos
    if menu_data.get("alimentos"):
        menu_html += '<div class="menu-chat-category">🥐 ALIMENTOS</div>'
        for item in menu_data["alimentos"]:
            menu_html += f"""
        <div class="menu-chat-item">
            <span class="menu-chat-item-name">{item['nombre']}</span>
            <span class="menu-chat-item-price">${item['precio']}</span>
        </div>
        """
    
    # Postres
    if menu_data.get("postres"):
        menu_html += '<div class="menu-chat-category">🍰 POSTRES</div>'
        for item in menu_data["postres"]:
            menu_html += f"""
        <div class="menu-chat-item">
            <span class="menu-chat-item-name">{item['nombre']}</span>
            <span class="menu-chat-item-price">${item['precio']}</span>
        </div>
        """
    
    menu_html += """
        <div style="text-align: center; margin-top: 16px; padding-top: 12px; border-top: 1px solid #404040;">
            <div style="color: #a0a0a0; font-size: 12px;">
                💡 Escribe tu pedido en lenguaje natural<br>
                Ej: "Quiero un latte y un croissant"
            </div>
        </div>
    </div>
    """
    
    return menu_html

def render_order_ticket(orden):
    """Generate beautiful order ticket HTML"""
    order_id = orden.get('id', 'N/A')
    total = orden.get('total', 0)
    items = orden.get('items', [])
    tiempo = orden.get('tiempo_preparacion_total', orden.get('tiempo_estimado', 15))

    # Build ticket items
    items_html = ""
    for item in items:
        nombre = item.get('nombre_producto', 'Producto')
        cant = item.get('cantidad', 1)
        precio = item.get('precio_unitario', 0)

        # Modifiers
        mods = ""
        if item.get('modificadores_seleccionados'):
            mods_list = ", ".join(item['modificadores_seleccionados'])
            mods = f'<div style="font-size:10px; color:#666; margin-top:2px;">+ {mods_list}</div>'

        items_html += f"""
        <div class="order-item">
            <span class="item-name">{cant}x {nombre}{mods}</span>
            <span class="item-price">${precio * cant:.0f}</span>
        </div>
        """

    # Physical ticket
    ticket_html = f"""
    <div class="order-card">
        <div class="order-header">
            <div class="order-title">JUSTICIA Y CAFÉ</div>
            <div class="order-id">#{order_id[-6:]}</div>
            <div class="order-date">{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
        </div>

        {items_html}

        <div class="order-total">
            TOTAL: ${total:.0f}
        </div>

        <div class="order-time">
            ⏱️ TIEMPO ESTIMADO: {tiempo} MINUTOS
        </div>

        <div class="order-footer">
            ¡Gracias por tu preferencia!<br>
            Recibo generado automáticamente
        </div>
    </div>
    """
    return ticket_html

def generate_dynamic_sidebar():
    """SIDEBAR DINÁMICO: Itera sobre MENU_DATA para generar HTML"""
    menu_data = fetch_menu_from_api(API_BASE_URL)
    sidebar_html = '<div class="menu-card">'
    
    # ITERACIÓN DINÁMICA SOBRE MENU_DATA
    for categoria, items in menu_data.items():
        if items:  # Solo si la categoría tiene items
            # Título dinámico basado en la categoría
            categoria_titulos = {
                "bebidas": "☕ BEBIDAS",
                "alimentos": "🥐 ALIMENTOS", 
                "postres": "🍰 POSTRES"
            }
            categoria_titulo = categoria_titulos.get(categoria, categoria.upper())
            
            sidebar_html += f'<div class="menu-cat">{categoria_titulo}</div>'
            
            # Iteración sobre items de la categoría
            for item in items:
                sidebar_html += f'''
                <div class="menu-item">
                    • {item['nombre']} <span class="menu-price">${item['precio']}</span>
                </div>'''
    
    sidebar_html += '</div>'
    
    # Tip visual
    sidebar_html += """
    <div style="margin-top: 20px; padding: 12px; background: #1a1a2e; border-radius: 8px; border: 1px solid #404040;">
        <div style="color: #E0E0E0; font-size: 12px; text-align: center;">
            💡 <strong>Tip:</strong> Escribe tu pedido en lenguaje natural.<br>
            Ej: "Quiero un latte y un croissant"
        </div>
    </div>
    """
    
    return sidebar_html

# --- SIDEBAR - MENU DINÁMICO ---
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
        value=API_BASE_URL,
        disabled=True,
        help="URL del servidor backend"
    )

    # Clear chat button
    if st.button("🧹 Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("✅ Historial limpiado")
        st.rerun()

    st.markdown("---")

    # Menu Section - GENERACIÓN DINÁMICA
    st.markdown('<div style="color: #FFFFFF; font-size: 16px; font-weight: 600; margin-bottom: 12px;">📜 Menú del Día</div>', unsafe_allow_html=True)

    # SIDEBAR DINÁMICO BASADO EN MENU_DATA
    dynamic_menu_html = generate_dynamic_sidebar()
    st.markdown(dynamic_menu_html, unsafe_allow_html=True)

# --- MAIN APP - WHATSAPP EXPERIENCE ---

# Fixed WhatsApp Header
st.markdown("""
<div class="whatsapp-header">
    <div class="header-left">
        <div class="header-avatar">🤖</div>
        <div class="header-info">
            <h1>Justicia y Café</h1>
            <p>En línea • Pepe</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state - CRITICAL FIX
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if chat is empty and show welcome message
chat_is_empty = len(st.session_state.messages) == 0

if chat_is_empty:
    # Show welcome message (visual only, not saved to DB)
    st.markdown("""
    <div class="message-bubble bot-message">
        ¡Bienvenido a Justicia y Café! ☕👨‍⚖️<br><br>
        Soy Pepe, tu asistente legal-cafetero.<br><br>
        ¿Qué te sirvo para ganar el caso de hoy?<br><br>
        (Pide por voz o texto)
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

    # Quick menu button removed - used via chips
    pass
else:
    # Show existing chat history
    pass

# Chat messages container
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Only render chat history if there are messages
if not chat_is_empty:
    # Render chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # User message - GREEN BUBBLE
            st.markdown(f'<div class="message-bubble user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
        else:
            # Bot message - WHITE BUBBLE(S)
            if msg.get("mensajes"):
                # Multiple bubbles from JSON array
                for bubble_text in msg["mensajes"]:
                    st.markdown(f'<div class="message-bubble bot-message">{bubble_text}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
                    time.sleep(0.3)  # Small delay between bubbles
            else:
                # Single message
                st.markdown(f'<div class="message-bubble bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
                st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

            # Render order card if present
            if msg.get("orden"):
                ticket_html = render_order_ticket(msg["orden"])
                st.markdown(ticket_html, unsafe_allow_html=True)
                st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

# Handle menu display in chat
if not chat_is_empty:
    last_user_msg = st.session_state.messages[-1]["content"] if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" else ""
    
    # Check if user requested menu
    if "menú" in last_user_msg.lower() or "menu" in last_user_msg.lower() or last_user_msg.lower() in ["ver menú", "mostrar menú", "muéstrame el menú"]:
        menu_card_html = render_menu_card()
        st.markdown(menu_card_html, unsafe_allow_html=True)
        st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fixed bottom input area - WHATSAPP STYLE
st.markdown('<div class="input-area">', unsafe_allow_html=True)

# Quick Action Chips
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("📜 Ver Menú", key="btn_menu", use_container_width=True):
        st.session_state.messages.append({'role': 'user', 'content': '📜 Ver Menú'})
        st.rerun()
with c2:
    if st.button("☕ Lo de siempre", key="btn_habitual", use_container_width=True):
        st.session_state.messages.append({'role': 'user', 'content': '☕ Lo de siempre'})
        st.rerun()
with c3:
    if st.button("⚖️ Mis Puntos", key="btn_puntos", use_container_width=True):
        st.session_state.messages.append({'role': 'user', 'content': '⚖️ Mis Puntos'})
        st.rerun()
with c4:
    if st.button("🎲 Sorpréndeme", key="btn_sorpresa", use_container_width=True):
        st.session_state.messages.append({'role': 'user', 'content': '🎲 Sorpréndeme'})
        st.rerun()

st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# Chat input - VISIBLE SEND BUTTON
if prompt := st.chat_input("Escribe tu pedido...", key="chat_input"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show typing indicator
    typing_placeholder = st.empty()
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)

    # Process request with FIXED API HANDLING
    try:
        payload = {"mensaje": prompt, "telefono": telefono}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        typing_placeholder.empty()

        if response.status_code == 200:
            data = response.json()
            
            # CRITICAL FIX: Validar que data no sea None
            if data:
                tipo = data.get("tipo", "texto")
                mensajes = data.get("mensajes", [data.get("mensaje", "...")])
                orden = data.get("orden")

                # Store message
                msg_data = {
                    "role": "assistant",
                    "content": " ".join(mensajes) if mensajes else "...",
                    "orden": orden,
                    "tipo": tipo,
                    "mensajes": mensajes if len(mensajes) > 1 else None
                }

                # Handle order responses
                if tipo in ["orden_creada", "orden_actualizada"] and orden:
                    st.balloons()

                st.session_state.messages.append(msg_data)
            else:
                # Handle empty response
                st.error("Error de comunicación con el cerebro")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Error de comunicación con el cerebro",
                    "tipo": "error"
                })
        else:
            st.error("Error de comunicación con el cerebro")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Error de comunicación con el cerebro",
                "tipo": "error"
            })

    except requests.exceptions.ConnectionError:
        typing_placeholder.empty()
        error_msg = "🔌 No se pudo conectar con el servidor. ¿Está corriendo el backend?"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg,
            "tipo": "error"
        })

    except Exception as e:
        typing_placeholder.empty()
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg,
            "tipo": "error"
        })

    # Rerun to update UI without losing chat
    time.sleep(0.5)
    st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# Remove duplicate file if exists
if os.path.exists("frontend/cliente_final.py"):
    os.remove("frontend/cliente_final.py")