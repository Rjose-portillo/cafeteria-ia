# 📋 Informe de Estado y Contexto Técnico - Justicia y Café

## 📝 RESUMEN DEL PROYECTO

**Nombre:** Justicia y Café  
**Misión:** Sistema de pedidos ultra-rápido para abogados/jueces usando IA  
**Core:** Automatización total (Chatbot "Pepe" → Cocina KDS → Dashboard Admin)  
**Versión Actual:** 2.0.0  
**Estado:** Demo funcional completa con todas las interfaces operativas  

### Propósito del Sistema
"Justicia y Café" es un ecosistema completo de automatización para cafeterías que combina inteligencia artificial conversacional con sistemas de gestión operativa en tiempo real. Dirigido específicamente al mercado legal (abogados/jueces), ofrece una experiencia de pedidos conversacional tipo WhatsApp con automatización backend completa.

### Flujo Principal
```
Cliente (WhatsApp-style UI) → Chatbot "Pepe" (Gemini AI) → FastAPI Backend → 
Firestore Database → KDS (Cocina) → Dashboard (Analytics)
```

---

## 🛠️ STACK TECNOLÓGICO Y ENTORNO

### Entorno de Desarrollo Específico
- **OS:** Windows con WSL 2 (Arch Linux)
- **Shell:** Fish Shell (source venv/bin/activate.fish)
- **Lenguaje:** Python 3.10+
- **Entorno Virtual:** venv con dependencias gestionadas por requirements.txt

### Backend Framework
- **FastAPI 0.115.6:** Framework async/await para alta concurrencia
- **Uvicorn:** Servidor ASGI para producción
- **Pydantic 2.10.3:** Validación de datos y serialización automática
- **Pydantic-Settings 2.6.1:** Configuración type-safe desde variables de entorno

### Frontend Technologies
- **Streamlit 1.41.0:** Desarrollo rápido de apps web
- **CSS Custom:** Estilos avanzados para UX nativa estilo WhatsApp
- **Responsive Design:** Media queries para múltiples dispositivos
- **Plotly 5.24.1:** Gráficos interactivos para Dashboard

### Inteligencia Artificial
- **Google Gemini 2.5 Flash:** Modelo multimodal rápido y preciso
- **Google AI GenerativeAI 0.8.3:** SDK oficial para integración
- **Function Calling:** Tools para interpretación de pedidos

### Base de Datos y Cloud
- **Google Firestore:** NoSQL en tiempo real, escalable globalmente
- **Google Cloud Platform:** Proyecto: cafeteria-ia-backend
- **Firebase Admin SDK:** Autenticación y acceso a servicios

### Dependencias Críticas
```txt
fastapi==0.115.6
streamlit==1.41.0
pydantic==2.10.3
google-cloud-firestore==2.19.0
google-generativeai==0.8.3
pandas==2.2.3
numpy==2.2.0
requests==2.32.3
uvicorn==0.32.1
APScheduler==3.10.4
```

### Autenticación y Configuración
- **Service Account:** credentials.json configurado en .env
- **Variables de Entorno:** GOOGLE_APPLICATION_CREDENTIALS, GEMINI_API_KEY
- **Proyecto Cloud:** cafeteria-ia-backend (GCP)

---

## 🏗️ ARQUITECTURA ACTUAL

### Backend Modular (app/)
```
app/
├── main.py              # Entry point FastAPI con lifespan management
├── core/
│   └── config.py        # Configuración pydantic-settings
├── models/
│   └── schemas.py       # Modelos Pydantic para toda la app
├── api/routers/
│   ├── chat.py          # Endpoint principal de chat con debouncing
│   ├── orders.py        # Gestión de órdenes (CRUD)
│   └── menu.py          # Catálogo de productos
└── services/
    ├── gemini_service.py    # IA conversacional con personalidad "Pepe"
    ├── firestore_service.py # CRUD Firestore con singleton pattern
    ├── menu_service.py      # Cache de menú con fuzzy search
    └── scheduler_service.py # APScheduler para feedback post-venta
```

### Servicios Críticos

#### GeminiService (`app/services/gemini_service.py`)
- **Personalidad:** "Pepe" - mesero digital mexicano amable y eficiente
- **Tools disponibles:** 
  - `interpretar_orden()`: Procesa pedidos con precios reales del menú
  - `cancelar_orden()`: Maneja cancelaciones con regla de 5 minutos
  - `registrar_nombre()`: Onboarding de clientes
- **Comanda Abierta:** Permite agregar items a pedidos existentes
- **Context Aware:** Personalización por cliente y producto favorito

#### FirestoreService (`app/services/firestore_service.py`)
- **Colecciones:** clientes, pedidos, menu, chat_history, insumos
- **Operaciones:** CRUD completo con manejo de errores
- **Funciones Premium:** get_favorite_product(), get_daily_sales_metrics()
- **Patrón Singleton:** Una instancia por aplicación

#### MenuService (`app/services/menu_service.py`)
- **Cache en memoria:** Carga menu desde Firestore al startup
- **Fuzzy Search:** Búsqueda con SequenceMatcher y normalización de texto
- **Búsqueda Avanzada:** Exact, partial, y similarity-based matching

#### SchedulerService (`app/services/scheduler_service.py`)
- **APScheduler:** Tareas en background
- **Feedback Automático:** Mensajes post-venta programados
- **Timezone UTC:** Consistencia en todas las operaciones temporales

### Frontend Components (frontend/)

#### Cliente (`frontend/cliente.py`)
- **UX:** WhatsApp Business clone pixel-perfect
- **Características:**
  - Header fijo con avatar de Pepe
  - Chat bubbles verde (usuario) y blanco (bot)
  - Sidebar dinámico con menú visual
  - Indicador de escritura animado
  - Tickets físicos visuales (CSS receipt-style)
  - Session state para persistencia de chat
- **API Integration:** POST /chat con manejo de errores robusto
- **Visual Features:** Balloons animation, typing indicator, menu cards

#### Cocina KDS (`frontend/cocina.py`)
- **Layout:** Kanban con 3 columnas (Pendiente/Preparando/Listo)
- **Time Indicators:** Semáforo de tiempos (verde <5min, amarillo 5-15min, rojo >15min)
- **Auto-refresh:** Cada 15 segundos sin flicker agresivo
- **Action Buttons:** Iniciar preparación, marcar listo, entregar
- **Professional UI:** Dark theme optimizado para cocina

#### Dashboard (`frontend/dashboard.py`)
- **Async Handling:** Fix para asyncio event loop en Streamlit
- **Analytics:** Gráficos Plotly con métricas de negocio
- **Mock Data:** Simulador con botón "Datos Semilla" para demo
- **Filters:** Por fecha, estado, cliente
- **Export:** CSV download functionality

---

## ✅ FUNCIONALIDADES IMPLEMENTADAS (Estado "Done")

### Chatbot "Pepe" - IA Conversacional
- ✅ **Onboarding automático:** Pregunta nombre a usuarios nuevos
- ✅ **Personalización:** Recuerda nombre y producto favorito del cliente
- ✅ **Herramientas IA:** Interpretación de pedidos, cancelaciones, registro de nombres
- ✅ **Comanda Abierta:** Agregar items a pedidos existentes
- ✅ **Upselling inteligente:** Sugerencias automáticas (bebida+comida)
- ✅ **Regla de Cancelación:** 5 minutos de gracia con empatía personalizada
- ✅ **Modo Juez Hambriento:** Detecta urgencia y responde express
- ✅ **Plan Justicia para Todos:** Programa de puntos automatizado

### Sistema de Menú
- ✅ **Menú Visual:** Renderizado en chat y sidebar dinámico
- ✅ **Categorías:** Bebidas, Alimentos, Postres
- ✅ **Precios Reales:** Integración con Firestore para precios actualizados
- ✅ **Tiempo de Preparación:** Cálculo automático por item
- ✅ **Búsqueda Fuzzy:** Normalización de texto y matching inteligente

### Gestión de Órdenes
- ✅ **Creación de Órdenes:** Con ID único y timestamp UTC
- ✅ **Estados:** Pendiente → Preparando → Listo → Entregado
- ✅ **Cálculo Automático:** Total, tiempo de preparación, hora estimada
- ✅ **Tickets Físicos:** CSS receipt-style con información completa
- ✅ **Comanda Abierta:** Agregar items sin crear nueva orden

### Backend API
- ✅ **FastAPI Asíncrono:** Todos los endpoints con async/await
- ✅ **CORS Configurado:** Permite conexiones desde Streamlit
- ✅ **Debouncing:** Agrupación de mensajes rápidos (2 segundos)
- ✅ **Error Handling:** Try/catch robusto con logging
- ✅ **Health Checks:** Endpoints de monitoreo

### Frontend Interfaces
- ✅ **Cliente WhatsApp-Style:** UX pixel-perfect con CSS custom
- ✅ **KDS Cocina:** Sistema Kanban con indicadores de tiempo
- ✅ **Dashboard Analytics:** Métricas en tiempo real con gráficos
- ✅ **Responsive Design:** Funciona en desktop y móvil
- ✅ **Session State:** Persistencia de datos entre refreshes

### Base de Datos
- ✅ **Firestore Integration:** CRUD completo con singleton pattern
- ✅ **Colecciones:** clientes, pedidos, menu, chat_history, insumos
- ✅ **Timezone UTC:** Consistencia temporal en toda la app
- ✅ **Métricas Diarias:** Agregación automática de ventas
- ✅ **Perfiles Cliente:** CRM básico con preferencias

### Automatización
- ✅ **Scheduler Service:** APScheduler para tareas background
- ✅ **Feedback Post-Venta:** Mensajes automáticos 35 min después
- ✅ **Estrategias Múltiples:** 6 mensajes aleatorios para feedback
- ✅ **Job Management:** Cancelación y monitoreo de tareas

### Script de Arranque
- ✅ **start_all.sh:** Orquestación completa de servicios
- ✅ **Fish Shell Support:** Activación automática de entorno virtual
- ✅ **Port Validation:** Verificación de puertos antes de iniciar
- ✅ **Health Checks:** Validación de servicios en startup
- ✅ **Error Handling:** Cleanup automático en caso de error

---

## 🚀 ROADMAP Y SIGUIENTES PASOS

### Integraciones Pendientes
- 🔄 **WhatsApp Business API:** Integración real con Meta para notificaciones
- 🔄 **Pasarela de Pagos:** Stripe o MercadoPago para procesamiento automático
- 🔄 **Facturación 4.0:** Generación automática de CFDI
- 🔄 **Impresoras Térmicas:** API para tickets físicos en cocina

### Funcionalidades Avanzadas
- 🔄 **Machine Learning:** Predicción de demanda y optimización de inventario
- 🔄 **CRM Avanzado:** Segmentación automática de clientes
- 🔄 **Multi-sucursal:** Soporte para múltiples ubicaciones
- 🔄 **App Móvil:** PWA o aplicación nativa

### Mejoras Técnicas
- 🔄 **Cache Redis:** Para performance de búsquedas frecuentes
- 🔄 **CDN:** Optimización de assets estáticos
- 🔄 **Monitoring:** Logs estructurados y métricas de performance
- 🔄 **Testing:** Suite de tests unitarios y de integración

---

## 🧪 GUÍA DE EJECUCIÓN RÁPIDA

### Requisitos Previos
```bash
# Verificar que estás en el directorio correcto
cd /home/ricardo/Cafeteria

# Verificar que existe el entorno virtual
ls -la venv/
```

### Comando de Arranque Universal
```bash
# PASO 1: Activar entorno virtual (Fish Shell)
source venv/bin/activate.fish

# PASO 2: Ejecutar orquestación completa
./start_all.sh
```

### Salida Esperada
```
🚀 Iniciando Justicia y Café...
🐍 Python version: 3.10.x
📦 Verificando dependencias...
✅ fastapi
✅ streamlit
✅ google.generativeai
✅ google.cloud.firestore
✅ pydantic_settings
🔍 Verificando puertos...
Puerto 8000 está libre
Puerto 8501 está libre
Puerto 8502 está libre
Puerto 8503 está libre
🎯 Iniciando servicios...
🔧 Iniciando Backend (FastAPI) en puerto 8000...
✅ Backend API está listo
💬 Iniciando Cliente (Streamlit) en puerto 8501...
🍳 Iniciando Cocina (KDS) en puerto 8502...
📊 Iniciando Dashboard (Panel de Control) en puerto 8503...
🔍 Verificando servicios...
✅ Backend API: http://localhost:8000
   📖 Docs: http://localhost:8000/docs
✅ Cliente: http://localhost:8501
✅ Cocina (KDS): http://localhost:8502
✅ Dashboard: http://localhost:8503
🎉 ¡Todos los servicios iniciados exitosamente!
📊 Estado: 4/4 servicios activos
🌐 URLs de acceso:
   🔧 Backend API: http://localhost:8000/docs
   💬 Cliente:     http://localhost:8501
   🍳 Cocina:      http://localhost:8502
   📊 Dashboard:   http://localhost:8503
```

### URLs de Acceso Directo
- **Cliente (WhatsApp-Style):** http://localhost:8501
- **Cocina (KDS):** http://localhost:8502  
- **Dashboard (Analytics):** http://localhost:8503
- **Backend API Docs:** http://localhost:8000/docs

### Configuración de Credenciales
```bash
# Verificar .env
cat .env | grep -E "(GEMINI_API_KEY|GOOGLE_CLOUD_PROJECT)"

# Verificar credentials.json
ls -la credentials.json
```

---

## 🔧 CORRECCIONES RECIENTES IMPLEMENTADAS

### Fix Asyncio en Dashboard
**Archivo:** `frontend/dashboard.py`  
**Problema:** RuntimeError al usar asyncio.run() en Streamlit  
**Solución:** 
```python
def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
```

### Fix Visual unsafe_allow_html en Cliente
**Archivo:** `frontend/cliente.py`  
**Problema:** Rendering de CSS personalizado bloqueado  
**Solución:** Wrapping completo en `unsafe_allow_html=True` para todos los componentes CSS

### Sidebar Dinámico
**Archivo:** `frontend/cliente.py`  
**Funcionalidad:** Menú generado dinámicamente desde MENU_DATA con iteración automática sobre categorías

---


## 🎯 CASOS DE USO DEMO VALIDADOS

### Flujo Completo Cliente
1. **Inicio:** Cliente accede a http://localhost:8501
2. **Onboarding:** Pepe pregunta nombre automáticamente
3. **Pedido:** Cliente escribe "Quiero un latte y un croissant"
4. **IA Procesa:** Gemini interpreta orden con precios reales
5. **Confirmación:** Ticket físico visual con tiempo estimado
6. **KDS Actualiza:** Cocina ve orden en estado "Pendiente"

### Flujo Completo Cocina
1. **Visualización:** KDS muestra órdenes en Kanban
2. **Indicadores:** Semáforo de tiempo por orden
3. **Actions:** Botones para cambiar estados
4. **Actualización:** Auto-refresh cada 15 segundos

### Flujo Dashboard
1. **Métricas:** KPIs en tiempo real
2. **Simulación:** Botón "Datos Semilla" para demo
3. **Análisis:** Gráficos Plotly interactivos
4. **Export:** Descarga CSV de datos

---

## 🔍 DEBUGGING Y TROUBLESHOOTING

### Verificación de Servicios
```bash
# Verificar backend
curl http://localhost:8000/health

# Verificar clientes
curl http://localhost:8501/_stcore/health
curl http://localhost:8502/_stcore/health  
curl http://localhost:8503/_stcore/health
```

### Logs Comunes
```bash
# Ver logs del backend
tail -f nohup.out | grep "FastAPI"

# Ver logs de Streamlit
streamlit run frontend/cliente.py --logger.level=debug
```

### Errores Frecuentes
- **Puerto en uso:** `lsof -ti:8000 | xargs kill -9`
- **Credentials error:** Verificar GOOGLE_APPLICATION_CREDENTIALS
- **API Key:** Validar GEMINI_API_KEY en .env

---

*Informe técnico generado el 2025-12-08 para sesión de IA - Justicia y Café v2.0.0*

**CONTEXTO COMPLETO PARA PRÓXIMA SESIÓN DE IA:** Este documento contiene absolutamente todo el contexto técnico, operativo y de entorno necesario para que la siguiente IA pueda retomar el trabajo sin hacer preguntas básicas. El sistema está completamente funcional con demo operativa en los 4 puertos especificados.
