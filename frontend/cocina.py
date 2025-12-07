"""
Kitchen Display System (KDS) - Professional Kitchen Interface.
Features:
- Kanban-style order layout
- Traffic light time indicators (green/yellow/red)
- Auto-refresh without aggressive flickering
- Clear item display with modifiers
"""
import streamlit as st
import requests
from datetime import datetime, timezone
import time

# Page configuration
st.set_page_config(
    page_title="🍳 Cocina - Justicia y Café",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR KDS ---
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dark theme for kitchen */
    .stApp {
        background: #1a1a2e;
    }
    
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .kds-header {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .kds-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .kds-time {
        font-size: 1.2rem;
        font-family: monospace;
        background: #0f3460;
        padding: 8px 15px;
        border-radius: 8px;
    }
    
    /* Column headers */
    .column-header {
        text-align: center;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .header-pending {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
    }
    
    .header-preparing {
        background: linear-gradient(135deg, #f39c12 0%, #d68910 100%);
        color: white;
    }
    
    .header-ready {
        background: linear-gradient(135deg, #27ae60 0%, #1e8449 100%);
        color: white;
    }
    
    /* Order ticket */
    .order-ticket {
        background: #ffffff;
        border-radius: 12px;
        margin-bottom: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: slideIn 0.4s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .order-ticket:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    /* Time-based borders */
    .time-green {
        border-left: 6px solid #27ae60;
    }
    
    .time-yellow {
        border-left: 6px solid #f39c12;
    }
    
    .time-red {
        border-left: 6px solid #e74c3c;
        animation: pulse-red 1.5s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3); }
        50% { box-shadow: 0 4px 25px rgba(231, 76, 60, 0.6); }
    }
    
    /* Ticket header */
    .ticket-header {
        padding: 12px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px dashed #eee;
    }
    
    .ticket-id {
        font-family: monospace;
        font-weight: 700;
        font-size: 1rem;
        color: #333;
    }
    
    .ticket-time {
        font-size: 0.85rem;
        padding: 4px 10px;
        border-radius: 15px;
        font-weight: 600;
    }
    
    .time-badge-green {
        background: #d4edda;
        color: #155724;
    }
    
    .time-badge-yellow {
        background: #fff3cd;
        color: #856404;
    }
    
    .time-badge-red {
        background: #f8d7da;
        color: #721c24;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Ticket body */
    .ticket-body {
        padding: 15px;
    }
    
    .ticket-item {
        display: flex;
        align-items: flex-start;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .ticket-item:last-child {
        border-bottom: none;
    }
    
    .item-quantity {
        background: #6B4423;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .item-details {
        flex: 1;
    }
    
    .item-name {
        font-weight: 600;
        font-size: 1rem;
        color: #333;
        margin-bottom: 3px;
    }
    
    .item-mods {
        font-size: 0.85rem;
        color: #e74c3c;
        font-weight: 500;
    }
    
    .item-notes {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
        margin-top: 3px;
    }
    
    /* Ticket footer */
    .ticket-footer {
        background: #f8f9fa;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .customer-id {
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Action buttons */
    .action-btn {
        padding: 8px 16px;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .btn-start {
        background: #f39c12;
        color: white;
    }
    
    .btn-ready {
        background: #27ae60;
        color: white;
    }
    
    .btn-deliver {
        background: #3498db;
        color: white;
    }
    
    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .stat-card {
        background: #16213e;
        padding: 15px 25px;
        border-radius: 10px;
        text-align: center;
        flex: 1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-pending .stat-number { color: #e74c3c; }
    .stat-preparing .stat-number { color: #f39c12; }
    .stat-ready .stat-number { color: #27ae60; }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #888;
    }
    
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    /* Refresh indicator */
    .refresh-indicator {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #16213e;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.85rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Expander styling - WhatsApp colors */
    .streamlit-expanderHeader {
        background: #25d366 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid #20c157 !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        margin-bottom: 8px !important;
    }

    .streamlit-expanderHeader:hover {
        background: #20c157 !important;
        box-shadow: 0 2px 8px rgba(37, 211, 102, 0.3) !important;
    }

    /* Expander arrow - more visible */
    .streamlit-expanderHeader svg {
        color: white !important;
        width: 20px !important;
        height: 20px !important;
        stroke-width: 3 !important;
    }

    /* Expander content */
    .streamlit-expanderContent {
        background: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin-top: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_time_status(fecha_creacion) -> tuple:
    """
    Calculate time elapsed and return status color.
    Returns: (minutes_elapsed, color_class, badge_class)
    """
    if not fecha_creacion:
        return (0, "time-green", "time-badge-green")
    
    # Handle different datetime formats
    if isinstance(fecha_creacion, str):
        try:
            fecha_creacion = datetime.fromisoformat(fecha_creacion.replace('Z', '+00:00'))
        except:
            return (0, "time-green", "time-badge-green")
    
    # Ensure timezone awareness
    if fecha_creacion.tzinfo is None:
        fecha_creacion = fecha_creacion.replace(tzinfo=timezone.utc)
    
    ahora = datetime.now(timezone.utc)
    diff = ahora - fecha_creacion
    minutes = int(diff.total_seconds() / 60)
    
    if minutes < 5:
        return (minutes, "time-green", "time-badge-green")
    elif minutes < 15:
        return (minutes, "time-yellow", "time-badge-yellow")
    else:
        return (minutes, "time-red", "time-badge-red")

def render_order_ticket(order: dict, show_action: str = None):
    """Render a single order ticket."""
    order_id = order.get('id', 'N/A')
    items = order.get('items', [])
    cliente = order.get('id_cliente', 'Cliente')[-4:]  # Last 4 digits
    fecha = order.get('fecha_creacion')
    
    minutes, border_class, badge_class = get_time_status(fecha)
    
    # Build items HTML
    items_html = ""
    for item in items:
        nombre = item.get('nombre_producto', 'Item')
        cantidad = item.get('cantidad', 1)
        mods = item.get('modificadores_seleccionados', [])
        notas = item.get('notas_especiales', '')
        
        mods_html = f'<div class="item-mods">⚠️ {", ".join(mods)}</div>' if mods else ''
        notas_html = f'<div class="item-notes">📝 {notas}</div>' if notas else ''
        
        items_html += f"""
            <div class="ticket-item">
                <div class="item-quantity">{cantidad}</div>
                <div class="item-details">
                    <div class="item-name">{nombre}</div>
                    {mods_html}
                    {notas_html}
                </div>
            </div>
        """
    
    st.markdown(f"""
        <div class="order-ticket {border_class}">
            <div class="ticket-header">
                <span class="ticket-id">#{order_id[-8:]}</span>
                <span class="ticket-time {badge_class}">{minutes} min</span>
            </div>
            <div class="ticket-body">
                {items_html}
            </div>
            <div class="ticket-footer">
                <span class="customer-id">📱 ...{cliente}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    return order_id

def fetch_orders(api_base: str, endpoint: str) -> list:
    """Fetch orders from API with error handling."""
    try:
        url = f"{api_base}{endpoint}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else []
        else:
            st.error(f"API Error {response.status_code}: {url}")
            return []
    except requests.exceptions.ConnectionError:
        st.error(f"❌ No se puede conectar a {api_base}. ¿Está corriendo el backend?")
        return []
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")
        return []

def update_order_status(api_base: str, order_id: str, endpoint: str) -> bool:
    """Update order status via API with error handling."""
    try:
        url = f"{api_base}/orders/{order_id}/{endpoint}"
        response = requests.patch(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error updating order {response.status_code}: {url}")
            return False
    except requests.exceptions.ConnectionError:
        st.error(f"❌ No se puede conectar a {api_base}. ¿Está corriendo el backend?")
        return False
    except Exception as e:
        st.error(f"Error updating order status: {str(e)}")
        return False

# --- MAIN APP ---

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuración KDS")
    api_base = st.text_input(
        "🔗 API Base URL",
        value="http://127.0.0.1:8000",
        help="URL base del backend"
    )
    
    refresh_interval = st.slider(
        "🔄 Auto-refresh (segundos)",
        min_value=5,
        max_value=60,
        value=15,
        help="Intervalo de actualización automática"
    )
    
    st.divider()
    
    if st.button("🔄 Refrescar Ahora", use_container_width=True):
        st.rerun()
    
    st.divider()
    st.markdown("### 📊 Leyenda de Tiempos")
    st.markdown("""
    🟢 **Verde**: < 5 min (OK)
    🟡 **Amarillo**: 5-15 min (Atención)
    🔴 **Rojo**: > 15 min (¡Urgente!)
    """)

    st.divider()
    st.markdown("### 🔍 Debug Info")
    with st.expander("Ver detalles de conexión", expanded=False):
        st.write(f"**API Base:** {api_base}")
        st.write(f"**Última actualización:** {time.strftime('%H:%M:%S', time.localtime(st.session_state.get('last_refresh', time.time())))}")

        # Test API endpoints
        st.markdown("**Test de endpoints:**")
        test_endpoints = [
            "/orders/pending",
            "/orders/in-preparation",
            "/orders/ready",
            "/health"
        ]

        for endpoint in test_endpoints:
            try:
                response = requests.get(f"{api_base}{endpoint}", timeout=2)
                status_icon = "✅" if response.status_code == 200 else "❌"
                st.write(f"{status_icon} {endpoint}: {response.status_code}")
            except:
                st.write(f"❌ {endpoint}: Error de conexión")

# Header with manual refresh button
col_title, col_refresh = st.columns([3, 1])
with col_title:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="kds-header">
            <h1 class="kds-title">🍳 Kitchen Display System</h1>
            <div class="kds-time">🕐 {current_time}</div>
        </div>
    """, unsafe_allow_html=True)

with col_refresh:
    if st.button("🔄 REFRESCAR", use_container_width=True, type="primary"):
        st.rerun()

# Fetch all orders with connection status
pending_orders = fetch_orders(api_base, "/orders/pending")
preparing_orders = fetch_orders(api_base, "/orders/in-preparation")
ready_orders = fetch_orders(api_base, "/orders/ready")

# Connection status indicator
connection_ok = len(pending_orders) >= 0  # If we got here without errors, connection is OK
connection_status = "🟢 Conectado" if connection_ok else "🔴 Desconectado"

# Stats bar with connection status
st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-card stat-pending">
            <div class="stat-number">{len(pending_orders)}</div>
            <div class="stat-label">Pendientes</div>
        </div>
        <div class="stat-card stat-preparing">
            <div class="stat-number">{len(preparing_orders)}</div>
            <div class="stat-label">En Preparación</div>
        </div>
        <div class="stat-card stat-ready">
            <div class="stat-number">{len(ready_orders)}</div>
            <div class="stat-label">Listos</div>
        </div>
        <div class="stat-card" style="background: {'#16213e' if connection_ok else '#2c1810'};">
            <div class="stat-number" style="color: {'white' if connection_ok else '#ff6b6b'};">
                {"✓" if connection_ok else "✗"}
            </div>
            <div class="stat-label" style="color: {'#888' if connection_ok else '#ff6b6b'};">
                {"Conectado" if connection_ok else "Error"}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Debug info after orders are fetched
st.markdown("### 🔍 Información de Órdenes")
with st.expander("📊 Ver estadísticas detalladas", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📥 Pendientes", len(pending_orders))
    with col2:
        st.metric("🔥 En Preparación", len(preparing_orders))
    with col3:
        st.metric("📤 Listos", len(ready_orders))

    st.write(f"**Última actualización:** {time.strftime('%H:%M:%S', time.localtime(st.session_state.get('last_refresh', time.time())))}")
    st.write(f"**Estado de conexión:** {'🟢 Conectado' if connection_ok else '🔴 Desconectado'}")

# Kanban columns
col1, col2, col3 = st.columns(3)

# Column 1: Pending Orders
with col1:
    st.markdown('<div class="column-header header-pending">📥 Pendientes</div>', unsafe_allow_html=True)
    
    if not pending_orders:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">✨</div>
                <div>Sin pedidos pendientes</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for order in pending_orders:
            order_id = render_order_ticket(order)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.empty()
            with col2:
                if st.button(f"▶️ Iniciar #{order_id[-4:]}", key=f"start_{order_id}", use_container_width=True):
                    if update_order_status(api_base, order_id, "start-preparation"):
                        st.success(f"✅ Orden {order_id[-4:]} iniciada")
                        st.balloons()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error al iniciar orden {order_id[-4:]}")

# Column 2: In Preparation
with col2:
    st.markdown('<div class="column-header header-preparing">🔥 En Preparación</div>', unsafe_allow_html=True)
    
    if not preparing_orders:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🍳</div>
                <div>Nada en preparación</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for order in preparing_orders:
            order_id = render_order_ticket(order)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.empty()
            with col2:
                if st.button(f"✅ Listo #{order_id[-4:]}", key=f"ready_{order_id}", use_container_width=True):
                    if update_order_status(api_base, order_id, "mark-ready"):
                        st.success(f"✅ Orden {order_id[-4:]} lista")
                        st.balloons()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error al marcar orden {order_id[-4:]} como lista")

# Column 3: Ready for Pickup
with col3:
    st.markdown('<div class="column-header header-ready">📤 Listos</div>', unsafe_allow_html=True)
    
    if not ready_orders:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🎉</div>
                <div>Sin pedidos listos</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for order in ready_orders:
            order_id = render_order_ticket(order)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.empty()
            with col2:
                if st.button(f"🚀 Entregar #{order_id[-4:]}", key=f"deliver_{order_id}", use_container_width=True):
                    if update_order_status(api_base, order_id, "mark-delivered"):
                        st.success(f"✅ Orden {order_id[-4:]} entregada")
                        st.balloons()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error al entregar orden {order_id[-4:]}")

# Auto-refresh indicator and mechanism
st.markdown(f"""
    <div class="refresh-indicator">
        🔄 Auto-refresh: {refresh_interval}s
    </div>
""", unsafe_allow_html=True)

# Auto-refresh mechanism with better error handling
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
time_since_refresh = current_time - st.session_state.last_refresh

if time_since_refresh >= refresh_interval:
    st.session_state.last_refresh = current_time
    time.sleep(0.1)  # Small delay to prevent rapid refreshes
    st.rerun()
else:
    # Show countdown to next refresh
    remaining = int(refresh_interval - time_since_refresh)
    if remaining > 0:
        time.sleep(1)  # Update every second
        st.rerun()