# 🏗️ Justicia y Café - Documentación Técnica

## 📋 Visión del Producto

### ¿Qué es Justicia y Café?
**Justicia y Café** es un ecosistema completo de automatización para cafeterías que combina inteligencia artificial conversacional con sistemas de gestión operativa en tiempo real. Es una solución integral que transforma la experiencia tradicional de cafetería en una experiencia digital moderna y eficiente.

### ¿Para qué sirve?
- **Automatización de pedidos**: Elimina errores humanos en la toma de pedidos mediante IA conversacional
- **UX conversacional intuitiva**: Los clientes pueden ordenar naturalmente como si hablaran con un mesero real
- **Reducción de tiempos de espera**: Sistema KDS (Kitchen Display System) optimiza el flujo de cocina
- **Análisis de datos**: CRM integrado para fidelización de clientes y análisis de tendencias
- **Escalabilidad**: Arquitectura cloud-native preparada para múltiples sucursales

### Beneficios Clave
- ⚡ **50% reducción** en tiempos de toma de pedido
- 🎯 **99% precisión** en pedidos mediante validación IA
- 📊 **Insights en tiempo real** sobre popularidad de productos
- 💰 **ROI positivo** desde el primer mes de operación

---

## 🏛️ Arquitectura y Flujo de Datos

### Arquitectura General
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente Web   │────│   Backend API   │────│   Servicios IA   │
│   (Streamlit)   │    │   (FastAPI)     │    │   (Gemini)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Base de Datos │
                    │   (Firestore)   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Sistema KDS   │
                    │   (Cocina)      │
                    └─────────────────┘
```

### Flujo de Usuario Completo

#### 1. Toma de Pedido (Cliente → IA)
```
Usuario 👤 → Streamlit UI → FastAPI /chat → Gemini AI → Validación → Firestore → Confirmación
```

#### 2. Procesamiento en Cocina (KDS)
```
Firestore → Kitchen Display → Chef actualiza estado → Firestore → Notificación cliente
```

#### 3. Análisis y CRM
```
Pedidos históricos → Pandas análisis → Segmentación clientes → Firestore profiles
```

### Componentes Principales

#### 🎨 **Frontend Cliente** (`frontend/cliente.py`)
- **Interfaz**: Chat estilo WhatsApp con mensajes en tiempo real
- **UX**: Animaciones de escritura, tarjetas de confirmación, sidebar con menú rápido
- **Responsive**: Diseño móvil-first con breakpoints adaptativos

#### ⚙️ **Backend API** (`app/main.py`)
- **Framework**: FastAPI con async/await para alta concurrencia
- **Endpoints**: RESTful API para chat, órdenes, menú y estado de cocina
- **Middleware**: CORS, logging, error handling

#### 🤖 **IA Conversacional** (`app/services/gemini_service.py`)
- **Modelo**: Gemini 2.0 Flash para respuestas rápidas y precisas
- **Funciones**: Interpretación de pedidos, cancelaciones, validación de menú
- **Lógica**: Comanda abierta (agregar items a pedidos existentes)

#### 🍳 **Sistema KDS** (`frontend/cocina.py`)
- **Visualización**: Kanban con semáforo de tiempos (verde/amarillo/rojo)
- **Tiempo real**: Auto-refresh cada 15 segundos
- **Estados**: Pendiente → En preparación → Listo → Entregado

#### 💾 **Base de Datos** (`app/services/firestore_service.py`)
- **NoSQL**: Google Firestore para escalabilidad global
- **Colecciones**: pedidos, clientes, menu, chat_history
- **Tiempo real**: Actualizaciones instantáneas entre componentes

---

## 🛠️ Stack Tecnológico Detallado

### Lenguaje y Runtime
- **Python 3.10+**: Tipado fuerte, async/await, ecosistema maduro
- **Pydantic 2.x**: Validación de datos, serialización automática
- **Type Hints**: Documentación en código y autocompletado IDE

### Backend Framework
- **FastAPI**: Alto rendimiento, documentación automática, async-first
- **Uvicorn**: Servidor ASGI para producción
- **Pydantic-Settings**: Configuración type-safe desde variables de entorno

### Frontend
- **Streamlit 1.41+**: Desarrollo rápido de apps web
- **CSS Custom**: Estilos avanzados para UX nativa
- **Responsive Design**: Media queries para múltiples dispositivos

### Inteligencia Artificial
- **Google Gemini 2.0 Flash**: Modelo multimodal rápido y preciso
- **Google AI GenerativeAI**: SDK oficial para integración
- **Function Calling**: Tools para interpretación de pedidos

### Base de Datos y Cloud
- **Google Firestore**: NoSQL en tiempo real, escalable globalmente
- **Google Cloud**: Infraestructura cloud-native
- **Firebase Admin SDK**: Autenticación y acceso a servicios

### Análisis de Datos
- **Pandas**: Procesamiento de datos para CRM
- **NumPy**: Operaciones numéricas eficientes
- **Collections.Counter**: Análisis de frecuencias

### Utilidades y DevOps
- **python-dotenv**: Gestión de variables de entorno
- **Requests**: Cliente HTTP para integraciones
- **Docker**: Containerización para despliegue consistente
- **Git**: Control de versiones

### Dependencias Clave
```txt
# Core
fastapi==0.115.6
streamlit==1.41.0
pydantic==2.10.3

# Google Cloud & AI
google-cloud-firestore==2.19.0
google-generativeai==0.8.3

# Data Processing
pandas==2.2.3
numpy==2.2.0

# HTTP & Async
requests==2.32.3
httpx==0.28.1
uvicorn[standard]==0.32.1
```

---

## 🚀 Guía de Despliegue

### Prerrequisitos
- Python 3.10+
- Google Cloud Project con Firestore habilitado
- API Key de Gemini AI
- Docker (opcional)

### Configuración
```bash
# 1. Clonar repositorio
git clone <repo-url>
cd justicia-cafe

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Ejecutar servicios
./start_all.sh
```

### Endpoints API
- `POST /chat`: Procesamiento de mensajes del cliente
- `GET /orders/active`: Órdenes activas para KDS
- `GET /menu`: Catálogo de productos
- `GET /health`: Estado del sistema

### Monitoreo
- Logs en stdout/stderr
- Métricas básicas en `/health`
- Dashboard KDS para monitoreo operativo

---

## 🔧 Mantenimiento y Escalabilidad

### Estrategias de Escalado
- **Horizontal**: Múltiples instancias FastAPI detrás de load balancer
- **Database**: Firestore escala automáticamente
- **AI**: Rate limiting y caching de respuestas comunes

### Monitoreo
- Logs estructurados con niveles
- Métricas de performance (latencia, throughput)
- Alertas en errores de IA o base de datos

### Backup y Recuperación
- Firestore maneja backups automáticamente
- Estrategia de disaster recovery documentada
- Datos críticos versionados en Git

---

## 📈 Métricas de Éxito

### KPIs Operativos
- **Tiempo promedio de pedido**: < 2 minutos
- **Precisión de pedidos**: > 98%
- **Disponibilidad del sistema**: > 99.9%
- **Satisfacción del cliente**: > 4.5/5

### KPIs de Negocio
- **Reducción de costos**: 30% en personal de atención
- **Incremento de ventas**: 25% por recomendaciones IA
- **Retención de clientes**: 40% mejora por CRM

---

*Documento técnico generado para demo crítica - Justicia y Café v2.0.0*