import asyncio
import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page configuration
st.set_page_config(
    page_title="Dashboard - Justicia y Café",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ASYNC HELPER FUNCTION - OBLIGATORIA ---
def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

# --- CSS STYLING ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .status-pending { color: #ff9800; font-weight: bold; }
    .status-preparing { color: #2196f3; font-weight: bold; }
    .status-ready { color: #4caf50; font-weight: bold; }
    .status-delivered { color: #9e9e9e; font-weight: bold; }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 Dashboard")
    st.markdown("---")
    
    # Filters
    st.subheader("Filtros")
    
    # Date range
    fecha_inicio = st.date_input("Fecha inicio", value=pd.Timestamp.now().date())
    fecha_fin = st.date_input("Fecha fin", value=pd.Timestamp.now().date())
    
    # Status filter
    status_filter = st.multiselect(
        "Estado del pedido",
        ["Pendiente", "Preparando", "Listo", "Entregado"],
        default=["Pendiente", "Preparando", "Listo", "Entregado"]
    )
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        st.rerun()

# --- MAIN DASHBOARD ---
st.title("📊 Panel de Control - Justicia y Café")

# Mock data for demo - Replace with real Firestore data
def get_mock_orders():
    """Mock data for demonstration - Replace with Firestore calls"""
    import random
    from datetime import datetime, timedelta
    
    mock_orders = []
    statuses = ["Pendiente", "Preparando", "Listo", "Entregado"]
    
    for i in range(50):
        order = {
            "id": f"ORD-{1000 + i}",
            "fecha": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d %H:%M"),
            "estado": random.choice(statuses),
            "total": random.randint(50, 300),
            "items_count": random.randint(1, 5),
            "telefono": f"+52{random.randint(550000000, 559999999)}"
        }
        mock_orders.append(order)
    
    return pd.DataFrame(mock_orders)

# Try to get real data, fallback to mock
try:
    df = get_mock_orders()
    
    # Apply filters
    df["fecha_date"] = pd.to_datetime(df["fecha"]).dt.date
    
    if fecha_inicio and fecha_fin:
        df = df[(df["fecha_date"] >= fecha_inicio) & (df["fecha_date"] <= fecha_fin)]
    
    if status_filter:
        df = df[df["estado"].isin(status_filter)]
    
except Exception as e:
    st.error(f"Error al cargar datos: {str(e)}")
    df = pd.DataFrame()

# --- METRICS ROW ---
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pedidos = len(df)
        st.metric("Total Pedidos", total_pedidos)
    
    with col2:
        ingresos_totales = df["total"].sum()
        st.metric("Ingresos Totales", f"${ingresos_totales:,.0f}")
    
    with col3:
        promedio_pedido = df["total"].mean()
        st.metric("Promedio por Pedido", f"${promedio_pedido:.0f}")
    
    with col4:
        pedidos_hoy = len(df[pd.to_datetime(df["fecha"]).dt.date == pd.Timestamp.now().date()])
        st.metric("Pedidos Hoy", pedidos_hoy)

# --- CHARTS ROW ---
if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Orders by status
        status_counts = df["estado"].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Distribución por Estado",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Daily orders
        df["fecha_dia"] = pd.to_datetime(df["fecha"]).dt.date
        daily_orders = df.groupby("fecha_dia").size().reset_index(name="pedidos")
        daily_orders.columns = ["fecha", "pedidos"]
        
        fig_daily = px.bar(
            daily_orders,
            x="fecha",
            y="pedidos",
            title="Pedidos por Día",
            labels={"fecha": "Fecha", "pedidos": "Número de Pedidos"}
        )
        st.plotly_chart(fig_daily, use_container_width=True)

# --- ORDERS TABLE ---
st.markdown("---")
st.subheader("📋 Pedidos Recientes")

if not df.empty:
    # Sort by fecha
    df_display = df.sort_values("fecha", ascending=False)
    
    # Format dataframe for display
    df_display["estado"] = df_display["estado"].apply(
        lambda x: f'<span class="status-{x.lower()}">{x}</span>'
    )
    
    # Show table
    st.dataframe(
        df_display[["id", "fecha", "estado", "total", "items_count", "telefono"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay datos para mostrar con los filtros seleccionados")

# --- REAL-TIME UPDATES ---
st.markdown("---")
st.subheader("🔄 Actualizaciones en Tiempo Real")

# Auto-refresh every 30 seconds
st.empty()
if st.button("🔄 Auto-actualizar (30s)"):
    import time
    time.sleep(30)
    st.rerun()

# Add some demo functionality
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📈 Ver Tendencias"):
        st.info("Función de tendencias - En desarrollo")

with col2:
    if st.button("📊 Exportar Datos"):
        if not df.empty:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"pedidos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

with col3:
    if st.button("🔔 Configurar Alertas"):
        st.info("Sistema de alertas - En desarrollo")