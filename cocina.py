
"""
Dashboard de Cocina (KDS - Kitchen Display System).
Este módulo simula la pantalla que verían los cocineros.
Se conecta en tiempo real a Firestore para escuchar nuevos pedidos 'pendientes',
mostrándolos en tarjetas visuales. Permite al staff de cocina marcar órdenes 
como 'en preparación' o 'listas', actualizando el estado en la base de datos.
"""
import streamlit as st
from google.cloud import firestore
import os
from dotenv import load_dotenv
from datetime import datetime

# Setup inicial
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "cafeteria-ia-backend")

# Configurar página
st.set_page_config(
    page_title="Cocina - Justicia y Café",
    page_icon="👨‍🍳",
    layout="wide"
)

# Conexión a Firestore
@st.cache_resource
def get_db():
    try:
        return firestore.Client(project=PROJECT_ID)
    except Exception as e:
        st.error(f"Error conectando a Firestore: {e}")
        return None

db = get_db()

def marcar_listo(order_id):
    """Actualiza el estado del pedido a 'listo'"""
    if db:
        doc_ref = db.collection('pedidos').document(order_id)
        doc_ref.update({"estado": "listo"})
        st.success(f"Pedido {order_id} marcado como listo!")
        st.rerun()

# Header
st.title("👨‍🍳 Justicia y Café - Comandas")
st.markdown("---")

# Botón de actualización manual (Streamlit maneja el estado reactivo, pero esto ayuda)
if st.button("🔄 Actualizar Comandas"):
    st.rerun()

# Obtener pedidos pendientes
if db:
    # Query: Collection 'pedidos' where 'estado' == 'pendiente'
    # Nota: Firestore requiere índice para ordenar, así que traemos todo y filtramos/ordenamos en Python para MVP
    pedidos_ref = db.collection('pedidos').where(field_path='estado', op_string='==', value='pendiente')
    docs = pedidos_ref.stream()
    
    # Convertir a lista para manipular
    pedidos = []
    for doc in docs:
        p = doc.to_dict()
        p['id'] = doc.id
        pedidos.append(p)
    
    # Ordenar por fecha (más antiguos primero)
    # Manejo de timestamps: Firestore devuelve objetos datetime
    pedidos.sort(key=lambda x: x.get('fecha_creacion', datetime.now()))

    if not pedidos:
        st.info("👏 No hay pedidos pendientes. ¡La cocina está limpia!")
    else:
        # Layout Grid (3 columnas)
        cols = st.columns(3)
        
        for idx, pedido in enumerate(pedidos):
            col = cols[idx % 3] # Distribución cíclica
            
            with col:
                # Estilo tipo 'Card' usando contenedores
                with st.container(border=True):
                    # Cabecera de la tarjeta
                    st.subheader(f"🆔 {pedido.get('id', 'N/A')[:8]}")
                    
                    # Formatear hora
                    fecha = pedido.get('fecha_creacion')
                    if fecha:
                        hora = fecha.strftime("%H:%M")
                    else:
                        hora = "--:--"
                    
                    st.caption(f"🕒 Hora: {hora}")
                    st.markdown("### Productos:")
                    
                    # Lista de items
                    items = pedido.get('items', [])
                    for item in items:
                        nombre = item.get('nombre_producto', 'Item')
                        cant = item.get('cantidad', 1)
                        # Modificadores
                        mods = item.get('modificadores_seleccionados', [])
                        
                        st.markdown(f"**{cant}x {nombre}**")
                        if mods:
                            for mod in mods:
                                st.markdown(f"- *{mod}*")
                    
                    st.markdown("---")
                    
                    # Botón de Acción con key única
                    if st.button("✅ Listo", key=f"btn_{pedido['id']}"):
                        marcar_listo(pedido['id'])

else:
    st.warning("No hay conexión a la base de datos.")
