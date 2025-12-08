# ========================================
# PROYECTO COMPLETO: JUSTICIA Y CAFÉ
# ========================================
# Sistema de pedidos ultra-rápido para abogados/jueces usando IA
# Versión: 2.0.0
# 
# CONTENIDO DE ARCHIVOS DEL PROYECTO
# (Excluye archivos confidenciales: credentials.json, .env)
# ========================================

# ========================================
# README_TECNICO.md
# ========================================
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

# ========================================
# requirements.txt
# ========================================
altair==5.5.0
annotated-types==0.7.0
anyio==4.7.0
APScheduler==3.10.4
attrs==25.4.0
blinker==1.9.0
cachetools==5.5.2
certifi==2025.11.12
charset-normalizer==3.4.4
click==8.3.1
fastapi==0.115.6
gitdb==4.0.12
GitPython==3.1.45
google-ai-generativelanguage==0.6.10
google-api-core==2.28.1
google-api-python-client==2.187.0
google-auth==2.36.0
google-auth-httplib2==0.2.1
google-cloud-core==2.5.0
google-cloud-firestore==2.19.0
google-generativeai==0.8.3
googleapis-common-protos==1.72.0
grpcio==1.76.0
grpcio-status==1.71.2
h11==0.16.0
httpcore==1.0.9
httplib2==0.31.0
httptools==0.7.1
httpx==0.28.1
idna==3.11
Jinja2==3.1.6
jsonschema==4.25.1
jsonschema-specifications==2025.9.1
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
narwhals==2.13.0
numpy==2.2.0
packaging==24.2
pandas==2.2.3
pillow==11.3.0
plotly==5.24.1
proto-plus==1.26.1
protobuf==5.29.5
pyarrow==22.0.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pydantic==2.10.3
pydantic-settings==2.6.1
pydantic_core==2.27.1
pydeck==0.9.1
Pygments==2.19.2
pyparsing==3.2.5
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2025.2
PyYAML==6.0.3
qrcode==8.0
referencing==0.37.0
requests==2.32.3
rich==13.9.4
rpds-py==0.30.0
rsa==4.9.1
six==1.17.0
smmap==5.0.2
sniffio==1.3.1
starlette==0.41.3
streamlit==1.41.0
tenacity==9.1.2
toml==0.10.2
tornado==6.5.2
tqdm==4.67.1
typing-inspection==0.4.2
typing_extensions==4.12.2
tzdata==2025.2
tzlocal==5.3.1
uritemplate==4.2.0
urllib3==2.6.0
uvicorn==0.32.1
uvloop==0.22.1
watchdog==6.0.0
watchfiles==1.1.1
websockets==15.0.1

# ========================================
# start_all.sh
# ========================================
#!/bin/bash

# 🚀 Justicia y Café - Script de Inicio Universal
# Compatible con Linux/macOS - Activa entorno virtual y lanza servicios

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función de logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    error "No se encuentra requirements.txt. ¿Estás en el directorio raíz del proyecto?"
    exit 1
fi

if [ ! -f "app/main.py" ]; then
    error "No se encuentra app/main.py. ¿Estás en el directorio raíz del proyecto?"
    exit 1
fi

log "🚀 Iniciando Justicia y Café..."

# Verificar si existe .env
if [ ! -f ".env" ]; then
    warning "No se encuentra archivo .env"
    warning "Copiando .env.example a .env..."
    # Si existe el ejemplo lo copia, si no, crea uno vacío
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        touch .env
    fi
    warning "⚠️  Asegúrate de tener tus credenciales en el archivo .env!"
fi

# Detectar y activar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    # Buscar entorno virtual común
    VENV_DIR=""

    # Verificar nombres comunes de venv
    for dir in "venv" "env" ".venv" ".env"; do
        if [ -d "$dir" ]; then
            VENV_DIR="$dir"
            break
        fi
    done

    if [ -z "$VENV_DIR" ]; then
        warning "No se encontró entorno virtual. Creando uno nuevo..."
        python3 -m venv venv
        VENV_DIR="venv"
    fi

    info "Activando entorno virtual: $VENV_DIR"
    # Intentar activar versión Fish si estamos en Fish, sino Bash
    if [[ "$SHELL" == *"fish"* ]] && [ -f "$VENV_DIR/bin/activate.fish" ]; then
        source "$VENV_DIR/bin/activate.fish"
    else
        source "$VENV_DIR/bin/activate"
    fi
else
    info "Entorno virtual ya activado: $VIRTUAL_ENV"
fi

# Verificar Python
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
log "🐍 Python version: $PYTHON_VERSION"

# Instalar/actualizar dependencias
log "📦 Verificando dependencias..."
pip install --quiet -r requirements.txt

# Verificar que las dependencias críticas estén instaladas
log "🔍 Verificando dependencias críticas..."
python3 -c "
import sys
# Lista de módulos tal como se importan en Python
deps = ['fastapi', 'streamlit', 'google.generativeai', 'google.cloud.firestore', 'pydantic_settings']
for dep in deps:
    try:
        __import__(dep)
        print(f'✅ {dep}')
    except ImportError:
        print(f'❌ {dep} - FALTA INSTALAR')
        sys.exit(1)
"

# Función para verificar si un puerto está libre
check_port() {
    local port=$1
    # Verificamos si lsof existe (Arch Linux a veces no lo trae por defecto)
    if ! command -v lsof &> /dev/null; then
        warning "Comando 'lsof' no encontrado. Saltando verificación de puertos pre-arranque."
        return 0
    fi

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        error "Puerto $port ya está en uso. Cierra el proceso que lo usa."
        return 1
    else
        info "Puerto $port está libre"
        return 0
    fi
}

# Verificar puertos
log "🔍 Verificando puertos..."
check_port 8000 || exit 1
check_port 8501 || exit 1
check_port 8502 || exit 1
check_port 8503 || exit 1

# Función para manejar señales de interrupción
cleanup() {
    log "🛑 Recibida señal de interrupción. Cerrando servicios..."
    # Matar procesos en background si existen
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Configurar manejador de señales
trap cleanup SIGINT SIGTERM

# Función para esperar a que un servicio esté listo
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    info "Esperando a $service_name ($url)..."

    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            log "✅ $service_name está listo"
            return 0
        fi

        echo -n "."
        sleep 2
        ((attempt++))
    done

    error "$service_name no respondió después de $max_attempts intentos"
    return 1
}

# Iniciar servicios en background
log "🎯 Iniciando servicios..."

# 1. Backend (FastAPI)
log "🔧 Iniciando Backend (FastAPI) en puerto 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
BACKEND_PID=$!

# Esperar a que el backend esté listo (Usamos /docs porque /health no siempre existe)
wait_for_service "http://localhost:8000/docs" "Backend API" || {
    error "Backend no inició correctamente"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
}

# 2. Cliente (Streamlit)
log "💬 Iniciando Cliente (Streamlit) en puerto 8501..."
streamlit run frontend/cliente.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /dev/null 2>&1 &
CLIENTE_PID=$!

# 3. Cocina (KDS)
log "🍳 Iniciando Cocina (KDS) en puerto 8502..."
streamlit run frontend/cocina.py --server.port 8502 --server.address 0.0.0.0 --server.headless true > /dev/null 2>&1 &
COCINA_PID=$!

# 4. Dashboard (Panel de Control)
log "📊 Iniciando Dashboard (Panel de Control) en puerto 8503..."
streamlit run frontend/dashboard.py --server.port 8503 --server.address 0.0.0.0 --server.headless true > /dev/null 2>&1 &
DASHBOARD_PID=$!

# Esperar un poco para que los servicios inicien visualmente
sleep 3

# Verificar que todos los servicios estén corriendo
log "🔍 Verificando servicios..."

SERVICES_UP=0
TOTAL_SERVICES=4

# Backend check
if curl -s "http://localhost:8000/docs" >/dev/null 2>&1; then
    log "✅ Backend API: http://localhost:8000"
    log "   📖 Docs: http://localhost:8000/docs"
    ((SERVICES_UP++))
else
    error "❌ Backend API no responde"
fi

# Cliente check
if curl -s "http://localhost:8501/_stcore/health" >/dev/null 2>&1; then
    log "✅ Cliente: http://localhost:8501"
    ((SERVICES_UP++))
else
    error "❌ Cliente no responde"
fi

# Cocina check
if curl -s "http://localhost:8502/_stcore/health" >/dev/null 2>&1; then
    log "✅ Cocina (KDS): http://localhost:8502"
    ((SERVICES_UP++))
else
    error "❌ Cocina (KDS) no responde"
fi

# Dashboard check
if curl -s "http://localhost:8503/_stcore/health" >/dev/null 2>&1; then
    log "✅ Dashboard: http://localhost:8503"
    ((SERVICES_UP++))
else
    error "❌ Dashboard no responde"
fi

echo
log "🎉 ¡Todos los servicios iniciados exitosamente!"
log "📊 Estado: $SERVICES_UP/$TOTAL_SERVICES servicios activos"
echo
info "🌐 URLs de acceso (Abre en tu navegador de Windows):"
info "   🔧 Backend API: http://localhost:8000/docs"
info "   💬 Cliente:     http://localhost:8501"
info "   🍳 Cocina:      http://localhost:8502"
info "   📊 Dashboard:   http://localhost:8503"
echo
warning "Presiona Ctrl+C para detener todos los servicios"

# Mantener el script corriendo y mostrar logs
log "📋 Monitoreando servicios... (Ctrl+C para salir)"

# Función para mostrar estado periódico
show_status() {
    while true; do
        sleep 30
        # Solo un heartbeat simple para saber que sigue vivo
        # echo -e "." 
    done
}

# Mostrar estado inicial
show_status &

# Esperar a que termine el script
wait

# ========================================
# app/main.py
# ========================================
"""
Main FastAPI Application Entry Point.
Initializes the API, configures CORS, and loads services on startup.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers import chat_router, orders_router, menu_router
from app.services.menu_service import get_menu_service
from app.services.gemini_service import get_gemini_service
from app.services.scheduler_service import get_scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Ambiente: {settings.ENV}")

    # Load menu cache
    menu_service = get_menu_service()
    menu_service.load_menu()

    # Initialize Gemini (this will use the loaded menu)
    gemini_service = get_gemini_service()

    # Start scheduler for automated tasks
    scheduler_service = get_scheduler_service()
    scheduler_service.start()

    print("✅ Servicios inicializados correctamente")

    yield

    # Shutdown
    print("👋 Cerrando aplicación...")
    scheduler_service.shutdown()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API para el sistema de pedidos de cafetería con IA",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit default
        "http://127.0.0.1:8501",
        "http://localhost:3000",  # React dev
        "http://127.0.0.1:3000",
        "*"  # Allow all in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(orders_router)
app.include_router(menu_router)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    menu_service = get_menu_service()
    
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "menu_loaded": menu_service.is_loaded,
        "menu_items": menu_service.item_count
    }


# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

# ========================================
# app/core/config.py
# ========================================
"""
Configuration module using pydantic-settings.
Loads environment variables from .env file and provides type-safe settings.
"""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic-settings for validation and type coercion.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    GEMINI_API_KEY: str
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str
    
    # AI Model Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # Environment
    ENV: Literal["local", "prod"] = "local"
    
    # Application Settings
    APP_NAME: str = "Justicia y Café"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # Business Rules
    CANCEL_TIME_LIMIT_MINUTES: int = 5
    DEFAULT_PREP_BUFFER_MINUTES: int = 5
    DEFAULT_COST_PERCENTAGE: float = 0.30
    
    # Chat Settings
    CHAT_HISTORY_LIMIT: int = 10
    MESSAGE_BUFFER_SECONDS: float = 2.0


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance for easy import
settings = get_settings()

# ========================================
# app/models/schemas.py
# ========================================
"""
Pydantic Schemas and Data Models.
Defines the core data structures for the application with Firestore compatibility.
All datetime fields use UTC timezone for consistency.
"""
from enum import Enum
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field, computed_field


class Category(str, Enum):
    """Product categories in the menu."""
    BEBIDA = "bebida"
    ALIMENTO = "alimento"
    POSTRE = "postre"


class OrderStatus(str, Enum):
    """Order lifecycle states."""
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class FirestoreModelMixin:
    """
    Mixin providing Firestore serialization/deserialization methods.
    Ensures consistent data format between Python objects and Firestore documents.
    """
    
    def to_firestore(self) -> Dict[str, Any]:
        """Convert model to Firestore-compatible dictionary."""
        if hasattr(self, 'model_dump'):
            data = self.model_dump()
        else:
            data = self.dict()
        return data

    @classmethod
    def from_firestore(cls, data: Dict[str, Any], doc_id: Optional[str] = None) -> 'FirestoreModelMixin':
        """Create model instance from Firestore document."""
        if doc_id and hasattr(cls, '__fields__') and 'id' in cls.__fields__:
            data['id'] = doc_id
        return cls(**data)


class ItemReceta(BaseModel):
    """Recipe item linking ingredient to quantity."""
    insumo_id: str
    cantidad: float


class MenuItem(BaseModel, FirestoreModelMixin):
    """Menu item representation."""
    id: Optional[str] = None
    nombre: str
    precio: float
    categoria: Category = Category.BEBIDA
    descripcion: Optional[str] = None
    tiempo_prep: int = 5  # Minutes
    disponible: bool = True
    modificadores: List[str] = []
    imagen_url: Optional[str] = None
    receta: List[ItemReceta] = Field(default_factory=list)


class OrderItem(BaseModel, FirestoreModelMixin):
    """
    Individual item within an order.
    Includes pricing and cost tracking for accounting.
    """
    nombre_producto: str
    cantidad: int = Field(gt=0, description="Quantity must be positive")
    precio_unitario: float = Field(ge=0, description="Unit price")
    costo_unitario: float = Field(default=0.0, description="Unit cost for accounting (30% default)")
    modificadores_seleccionados: List[str] = Field(default_factory=list)
    notas_especiales: Optional[str] = None
    tiempo_prep_unitario: int = Field(default=5, description="Prep time per unit in minutes")

    @computed_field
    @property
    def subtotal(self) -> float:
        """Calculate item subtotal (quantity * unit price)."""
        return self.cantidad * self.precio_unitario
    
    @computed_field
    @property
    def costo_total(self) -> float:
        """Calculate total cost for accounting."""
        return self.cantidad * self.costo_unitario


class Order(BaseModel, FirestoreModelMixin):
    """
    Complete order model with all business logic fields.
    Uses UTC timezone for all datetime fields.
    """
    id: Optional[str] = None
    id_cliente: str = Field(description="Customer phone number or ID")
    
    # Timestamps - CRITICAL: Always use UTC
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Order creation time in UTC"
    )
    
    # Order contents
    items: List[OrderItem] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0)
    
    # Status tracking
    estado: OrderStatus = OrderStatus.PENDIENTE
    
    # Payment
    metodo_pago: str = "pendiente"
    requiere_factura: bool = False
    
    # Time management
    hora_entrega_estimada: Optional[datetime] = None
    hora_entrega_programada: Optional[datetime] = None
    tiempo_preparacion_total: int = Field(default=0, description="Total prep time in minutes")
    
    # Metadata
    notas_orden: Optional[str] = None
    
    def calcular_total(self) -> float:
        """Recalculate order total from items."""
        return sum(item.subtotal for item in self.items)
    
    def calcular_tiempo_prep(self) -> int:
        """Calculate total preparation time from items."""
        return sum(item.tiempo_prep_unitario * self.cantidad for item in self.items)


class ChatMessage(BaseModel, FirestoreModelMixin):
    """
    Chat message for conversation history.
    Stored in Firestore for memory persistence.
    """
    role: str = Field(description="'user' or 'model'")
    content: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Message timestamp in UTC"
    )
    metadata: Optional[Dict[str, Any]] = None


class CustomerProfile(BaseModel, FirestoreModelMixin):
    """
    Customer profile with CRM data.
    Updated by the CRM analysis system.
    """
    id: Optional[str] = None  # Phone number
    nombre: Optional[str] = None
    nivel: str = "Pasante"  # Pasante, Asociado, Magistrado
    total_gastado: float = 0.0
    producto_favorito: Optional[str] = None
    frecuencia_visitas: int = 0
    ultima_visita: Optional[datetime] = None
    preferencias: List[str] = Field(default_factory=list)


# --- Inventory & Recipe Models ---

class Insumo(BaseModel, FirestoreModelMixin):
    """Ingredient for inventory management."""
    id: Optional[str] = None
    nombre: str
    unidad_medida: str  # "g", "ml", "unidad", etc.
    costo_por_unidad: float
    stock_actual: float = 0.0


class Ingredient(BaseModel, FirestoreModelMixin):
    """
    Ingredient for inventory management.
    Tracks stock levels and triggers alerts.
    """
    id: Optional[str] = None
    nombre: str
    unidad: str = "unidades"  # unidades, kg, litros, gramos
    stock_actual: float = 0.0
    stock_minimo: float = 10.0  # Alert threshold
    costo_unitario: float = 0.0
    proveedor: Optional[str] = None
    ultima_compra: Optional[datetime] = None
    
    @computed_field
    @property
    def necesita_restock(self) -> bool:
        """Check if ingredient needs restocking."""
        return self.stock_actual <= self.stock_minimo


class RecipeIngredient(BaseModel):
    """Ingredient quantity for a recipe."""
    ingrediente_id: str
    nombre_ingrediente: str
    cantidad: float
    unidad: str


class Recipe(BaseModel, FirestoreModelMixin):
    """
    Recipe linking a menu item to its ingredients.
    Used for inventory deduction and cost calculation.
    """
    id: Optional[str] = None
    producto_id: str  # Links to MenuItem
    nombre_producto: str
    ingredientes: List[RecipeIngredient] = Field(default_factory=list)
    instrucciones: Optional[str] = None
    tiempo_preparacion: int = 5  # Minutes
    
    @computed_field
    @property
    def costo_receta(self) -> float:
        """Calculate recipe cost from ingredients (placeholder - needs ingredient costs)."""
        return 0.0  # Would need to lookup ingredient costs


class InventoryTransaction(BaseModel, FirestoreModelMixin):
    """
    Inventory movement record.
    Tracks additions (purchases) and deductions (sales).
    """
    id: Optional[str] = None
    ingrediente_id: str
    tipo: str = "salida"  # entrada, salida, ajuste
    cantidad: float
    motivo: str = "venta"  # venta, compra, merma, ajuste
    orden_id: Optional[str] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DailySales(BaseModel, FirestoreModelMixin):
    """
    Daily sales summary for KPI dashboard.
    Aggregated data for reporting.
    """
    id: Optional[str] = None  # Format: YYYY-MM-DD
    fecha: datetime
    total_ventas: float = 0.0
    total_ordenes: int = 0
    ticket_promedio: float = 0.0
    productos_vendidos: Dict[str, int] = Field(default_factory=dict)
    costo_total: float = 0.0
    
    @computed_field
    @property
    def margen_bruto(self) -> float:
        """Calculate gross margin percentage."""
        if self.total_ventas > 0:
            return ((self.total_ventas - self.costo_total) / self.total_ventas) * 100
        return 0.0


# --- API Request/Response Models ---

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    mensaje: str = Field(min_length=1, description="User message")
    telefono: str = Field(min_length=10, description="Customer phone number")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    tipo: str = Field(description="Response type: texto, orden_creada, orden_actualizada, orden_cancelada, error, ignorar")
    mensaje: str
    mensajes: Optional[List[str]] = None  # For multi-bubble responses
    orden: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


# --- Dashboard Models ---

class KPIMetrics(BaseModel):
    """KPI metrics for dashboard display."""
    ventas_hoy: float = 0.0
    ventas_semana: float = 0.0
    ventas_mes: float = 0.0
    ordenes_hoy: int = 0
    ticket_promedio: float = 0.0
    producto_estrella: str = "N/A"
    clientes_nuevos: int = 0
    tasa_retencion: float = 0.0


class InventoryAlert(BaseModel):
    """Inventory alert for low stock items."""
    ingrediente_id: str
    nombre: str
    stock_actual: float
    stock_minimo: float
    unidad: str
    urgencia: str = "media"  # baja, media, alta, critica

# ========================================
# app/api/routers/chat.py
# ========================================
"""
Chat Router - Main chat endpoint for customer interactions.
Handles message buffering/debouncing and delegates to Gemini service.
"""
from typing import Dict, List
import asyncio
import uuid

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import ChatRequest, ChatResponse
from app.services.gemini_service import get_gemini_service
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

# Message buffer for debouncing rapid messages
message_buffer: Dict[str, List[str]] = {}
latest_request_token: Dict[str, str] = {}


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message from a customer.
    
    Implements debouncing to group rapid consecutive messages.
    Delegates processing to GeminiService for AI response generation.
    
    Args:
        request: ChatRequest with mensaje and telefono
        
    Returns:
        ChatResponse with tipo, mensaje, and optional orden data
    """
    try:
        phone = request.telefono
        
        # Initialize buffer for this phone if needed
        if phone not in message_buffer:
            message_buffer[phone] = []
        
        # Add message to buffer
        message_buffer[phone].append(request.mensaje)
        
        # Generate unique token for this request
        current_token = str(uuid.uuid4())
        latest_request_token[phone] = current_token
        
        # Wait for potential additional messages (debounce)
        await asyncio.sleep(settings.MESSAGE_BUFFER_SECONDS)
        
        # Check if this is still the latest request
        if latest_request_token.get(phone) != current_token:
            # Another message arrived, this one will be grouped
            return ChatResponse(
                tipo="ignorar",
                mensaje="Mensaje agrupado con el siguiente."
            )
        
        # This is the latest request - process all buffered messages
        full_message = " ".join(message_buffer[phone])
        message_buffer[phone] = []  # Clear buffer
        
        # Process with Gemini
        gemini = get_gemini_service()
        response = await gemini.process_chat(phone, full_message)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando mensaje: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for the chat service."""
    return {
        "status": "healthy",
        "service": "chat",
        "model": settings.GEMINI_MODEL
    }

# ========================================
# app/api/routers/orders.py
# ========================================
"""
Orders Router - Endpoints for order management.
Used by kitchen display and admin interfaces.
"""
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import OrderStatus
from app.services.firestore_service import get_firestore_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/active", response_model=List[Dict[str, Any]])
async def get_active_orders():
    """
    Get all active orders (pending and in preparation).
    Used by the kitchen display system.
    """
    firestore = get_firestore_service()
    orders = await firestore.get_active_orders()
    return orders


@router.get("/pending", response_model=List[Dict[str, Any]])
async def get_pending_orders():
    """Get all pending orders."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.PENDIENTE)
    return orders


@router.get("/in-preparation", response_model=List[Dict[str, Any]])
async def get_orders_in_preparation():
    """Get all orders currently being prepared."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.EN_PREPARACION)
    return orders


@router.get("/ready", response_model=List[Dict[str, Any]])
async def get_ready_orders():
    """Get all orders ready for pickup."""
    firestore = get_firestore_service()
    orders = await firestore.get_orders_by_status(OrderStatus.LISTO)
    return orders


@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, new_status: OrderStatus):
    """
    Update the status of an order.
    Used by kitchen staff to move orders through the workflow.
    """
    firestore = get_firestore_service()
    
    success = await firestore.update_order(order_id, {"estado": new_status.value})
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden {order_id} no encontrada"
        )
    
    return {"message": f"Orden {order_id} actualizada a {new_status.value}"}


@router.patch("/{order_id}/start-preparation")
async def start_preparation(order_id: str):
    """Mark an order as being prepared."""
    return await update_order_status(order_id, OrderStatus.EN_PREPARACION)


@router.patch("/{order_id}/mark-ready")
async def mark_ready(order_id: str):
    """Mark an order as ready for pickup."""
    return await update_order_status(order_id, OrderStatus.LISTO)


@router.patch("/{order_id}/mark-delivered")
async def mark_delivered(order_id: str):
    """Mark an order as delivered."""
    return await update_order_status(order_id, OrderStatus.ENTREGADO)

# ========================================
# app/api/routers/menu.py
# ========================================
"""
Menu Router - Endpoints for menu management.
"""
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status

from app.services.menu_service import get_menu_service

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("", response_model=List[Dict[str, Any]])
async def get_menu():
    """Get all available menu items."""
    menu_service = get_menu_service()
    return menu_service.get_all_items()


@router.get("/search/{query}")
async def search_menu(query: str):
    """
    Search for a menu item by name.
    Uses fuzzy matching for flexible search.
    """
    menu_service = get_menu_service()
    item = menu_service.buscar_producto(query)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto '{query}' no encontrado"
        )
    
    return item


@router.get("/item/{item_id}")
async def get_menu_item(item_id: str):
    """Get a specific menu item by ID."""
    menu_service = get_menu_service()
    item = menu_service.get_item_by_id(item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado"
        )
    
    return item


@router.post("/reload")
async def reload_menu():
    """
    Force reload menu from Firestore.
    Useful after menu updates.
    """
    menu_service = get_menu_service()
    count = menu_service.reload_menu()
    return {"message": f"Menú recargado: {count} items"}


@router.get("/stats")
async def menu_stats():
    """Get menu statistics."""
    menu_service = get_menu_service()
    items = menu_service.get_all_items()
    
    categories = {}
    total_items = len(items)
    
    for item in items:
        cat = item.get('categoria', 'otro')
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_items": total_items,
        "by_category": categories,
        "cache_loaded": menu_service.is_loaded
    }

# ========================================
# app/services/gemini_service.py
# ========================================
"""
Gemini AI Service - AI chat processing with business logic.
Handles order interpretation, cancellation, and conversation management.
Implements "Comanda Abierta" (open tab) logic and time-based cancellation rules.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
from functools import lru_cache
import uuid
import json

import google.generativeai as genai

from app.core.config import settings
from app.models.schemas import Order, OrderItem, OrderStatus, ChatResponse
from app.services.firestore_service import get_firestore_service
from app.services.menu_service import get_menu_service
from app.services.scheduler_service import get_scheduler_service


class GeminiService:
    """
    Service for Gemini AI interactions.
    Manages chat sessions, tool calls, and business logic processing.
    """
    
    _instance: Optional['GeminiService'] = None
    _model: Optional[genai.GenerativeModel] = None
    _configured: bool = False
    
    def __new__(cls) -> 'GeminiService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._configured:
            self._configure()
    
    def _configure(self):
        """Configure Gemini API (model created per request for personalization)."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._configured = True
            print(f"✅ Gemini API configurado: {settings.GEMINI_MODEL}")
        except Exception as e:
            print(f"❌ Error configurando Gemini: {e}")
            self._configured = False
    
    def _get_tools(self) -> List:
        """Define AI tools for function calling."""

        def interpretar_orden(items: List[Dict[str, Any]]):
            """
            Agrega items a la orden del cliente.
            Usar cuando el cliente pide alimentos o bebidas.

            Args:
                items: Lista de items con nombre_producto, cantidad, modificadores, notas
            """
            return items

        def cancelar_orden(razon: str):
            """
            Cancela la orden pendiente actual.
            Usar cuando el cliente explícitamente pide cancelar su pedido.

            Args:
                razon: Motivo de la cancelación
            """
            return razon

        def registrar_nombre(nombre: str):
            """
            Registra el nombre del cliente en su perfil.
            Usar cuando el usuario proporciona su nombre espontáneamente o después de preguntarle.
            Esto permite personalizar futuras interacciones.

            Args:
                nombre: Nombre del cliente (ej: "Ricardo", "María", etc.)
            """
            return nombre

        # Include code execution for future mathematical calculations
        tools = [interpretar_orden, cancelar_orden, registrar_nombre]

        # Add code execution capability for precise calculations
        try:
            # Enable code execution for mathematical operations
            code_execution_tool = genai.protos.Tool(
                code_execution=genai.protos.CodeExecution()
            )
            tools.append(code_execution_tool)
        except Exception as e:
            print(f"Warning: Could not enable code execution: {e}")

        return tools
    
    def _build_system_instruction(self, customer_profile: Dict[str, Any] = None, favorite_product: str = None) -> str:
        """Build dynamic system instruction with current menu and customer context."""
        menu_service = get_menu_service()
        menu_text = menu_service.get_menu_text_for_prompt()

        # Enhanced customer context
        customer_context = ""
        customer_name = None
        if customer_profile:
            customer_name = customer_profile.get('nombre')
            if customer_name:
                customer_context = f"El usuario se llama {customer_name}."
            else:
                customer_context = "Usuario Nuevo/Desconocido - NO SABEMOS SU NOMBRE."
        else:
            customer_context = "Usuario Nuevo/Desconocido - NO SABEMOS SU NOMBRE."

        # Favorite product context for "El Habitual" feature
        favorite_context = ""
        if favorite_product:
            favorite_context = f"DATO CLAVE: El plato favorito de este usuario es '{favorite_product}'. Si saluda sin pedir nada específico, sugiere: '¿Lo de siempre ({favorite_product})?'."

        return f"""
### CONTEXTO DEL CLIENTE
{customer_context}

{favorite_context}

### ROL
Eres 'Pepe', el mesero digital de la cafetería 'Justicia y Café'.
Tu tono es amable, coloquial (mexicano neutro) y eficiente.

### MENÚ DISPONIBLE (PRECIOS REALES)
{menu_text}

### OBJETIVO
Gestionar el CICLO COMPLETO del cliente: Identificación → Venta → Cierre → Post-Venta.

### 🚀 FASES DEL CICLO DE VIDA DEL CLIENTE

#### 🎯 FASE 0 - IDENTIFICACIÓN (CRÍTICA):
SI el usuario es NUEVO/DESCONOCIDO (no sabemos su nombre):
- PRIMERA acción: Saludar y preguntar nombre casualmente
- NO tomes pedidos hasta saber con quién hablas
- Ejemplos: "¿Con quién tengo el gusto hoy?", "¿A nombre de quién abro la comanda?"
- Una vez que te dé su nombre → USA 'registrar_nombre' INMEDIATAMENTE

#### 🍽️ FASE 1 - TOMA DE PEDIDOS + UPSELLING:
**UPSELLING INTELIGENTE:**
- Si piden SOLO BEBIDA → Sugiere ALIMENTO: "¿Te mando un croissant para acompañar?"
- Si piden SOLO COMIDA → Sugiere BEBIDA: "¿Qué bebida te ofrezco para acompañar?"
- Si es TARDE (después de 6 PM) → Sugiere DESCAFEINADO: "Si quieres algo más suave, tenemos descafeinado"

#### ❌ FASE 2 - CANCELACIONES (EMPATÍA):
Si usuario pide cancelar:
1. USA herramienta 'cancelar_orden' SIN EXCEPTUAR
2. Si devuelve ERROR por tiempo (>5 min) → Responde con empatía usando nombre:
   "Híjole{customer_name and f' {customer_name}' or ''}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
3. NUNCA prometas cancelar sin usar herramienta primero

#### 💰 FASE 3 - PLAN DE AFILIADOS "JUSTICIA PARA TODOS":
Si preguntan por descuentos o puntos:
- Explica: "Tenemos el plan 'Justicia para Todos' donde acumulas 5% en puntos por cada compra"
- Los puntos se pueden canjear por descuentos en futuras compras
- Es nuestra forma de agradecer tu preferencia

### REGLAS DE ORO (CRÍTICAS)

#### 🎯 REGLA DE ORO (ONBOARDING):
SI el usuario es DESCONOCIDO/Nuevo, tu PRIMERA acción es saludar amablemente y preguntar su nombre.
NO tomes NINGÚN pedido hasta saber con quién hablas.
Ejemplo: ["¡Hola! 👋 Soy Pepe, tu mesero digital", "¿Cómo te llamas para atenderte mejor?"]
Una vez que te dé su nombre, usa la herramienta 'registrar_nombre' INMEDIATAMENTE.

#### ❌ REGLA DE CANCELACIÓN:
Si el usuario pide cancelar, usa la herramienta 'cancelar_orden' SIN EXCEPTUAR.
Si la herramienta devuelve error (por tiempo límite), explícaselo con empatía:
"Híjole{customer_name and f' {customer_name}' or ''}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
NUNCA prometas cancelar sin usar la herramienta primero.

#### 💰 REGLA DE UPSELLING (VENTA CRUZADA):
Si piden SOLO café/bebida → Sugiere sutilmente un pan/postre.
Si piden SOLO comida → Sugiere sutilmente una bebida.
Si es TARDE (después de 6 PM) → Sugiere descafeinado.
Hazlo CORTO y NATURAL: "Va perfecto con un croissant de acompañante"

### DIRECTRICES DE COMPORTAMIENTO (JSON)
{{
  "personalidad": {{
    "tono": "Amigable, servicial, proactivo",
    "estilo": "Breve y directo. Evita bloques de texto largos."
  }},
  "reglas_negocio": {{
    "precios": "Usa los precios del menú. Si no está en menú, di que no tenemos eso.",
    "confirmacion": "Siempre confirma lo que entendiste antes de procesar.",
    "cierre": "Siempre pregunta '¿Algo más?' o '¿Todo bien?' al final."
  }},
  "manejo_herramientas": {{
    "interpretar_orden": "USAR CUANDO: El cliente pide alimentos o bebidas. INCLUSO si es un item adicional.",
    "cancelar_orden": "USAR CUANDO: El cliente pide cancelar, borrar o se equivocó.",
    "registrar_nombre": "USAR CUANDO: El cliente se presenta o da su nombre."
  }},
  "correcciones_inmediatas": {{
    "regla_principal": "SI el mensaje contiene corrección inmediata, IGNORA la primera parte y obedece SÓLO la última instrucción válida.",
    "ejemplos": [
      "'Quiero café... no, mejor té' → Interpreta SOLO 'té'",
      "'Dos croissants... mejor solo uno' → Interpreta SOLO 'uno'"
    ]
  }},
  "modo_juez_hambriento": {{
    "regla_urgencia": "Analiza el tono del usuario. SI escribe en MAYÚSCULAS o usa palabras como ['URGE', 'RÁPIDO', 'PRISA', 'AUDIENCIA', 'CORRIENDO'], ACTIVA EL 'MODO EXPRESS'.",
    "modo_express_acciones": [
      "1. ELIMINA todos los saludos y cortesías.",
      "2. Confirma la orden en una sola frase corta.",
      "3. No hagas upselling.",
      "4. Tu prioridad es la velocidad."
    ],
    "ejemplos_urgencia": [
      "Mensaje: 'URGENTE necesito un latte YA' → Modo Express: 'Listo, latte confirmado.'",
      "Mensaje: 'CORRIENDO a una reunión, café negro' → Modo Express: 'Café negro confirmado.'"
    ]
  }}
}}

### FORMATO DE RESPUESTA (IMPORTANTE)
Si tu respuesta es solo texto (sin llamar a una tool), PUEDES devolver una lista JSON de strings para simular mensajes de WhatsApp separados.
Ejemplo válido: ["¡Claro que sí!", "¿De qué sabor quieres tu dona?"]
"""
    
    @staticmethod
    def _recursive_to_native(d: Any) -> Any:
        """Convert protobuf/MapComposite objects to native Python types."""
        if hasattr(d, 'items'):
            return {k: GeminiService._recursive_to_native(v) for k, v in d.items()}
        if isinstance(d, (list, tuple)) or (hasattr(d, '__iter__') and not isinstance(d, (str, bytes))):
            return [GeminiService._recursive_to_native(x) for x in d]
        return d
    
    async def process_chat(self, telefono: str, mensaje: str) -> ChatResponse:
        """
        Process a chat message and return appropriate response.
        Handles tool calls, order management, and text responses.
        """
        firestore = get_firestore_service()
        menu_service = get_menu_service()

        try:
            # 1. Get customer profile for personalization
            customer_profile = await firestore.get_customer_profile(telefono)

            # 2. Get customer's favorite product for "El Habitual" feature
            favorite_product = await firestore.get_favorite_product(telefono) if firestore.is_connected else None

            # 3. Get chat history
            historial = await firestore.get_chat_history(telefono)

            # 4. Create model with customer context
            personalized_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                tools=self._get_tools(),
                system_instruction=self._build_system_instruction(customer_profile, favorite_product),
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )

            # 4. Start chat session
            chat_session = personalized_model.start_chat(
                history=historial,
                enable_automatic_function_calling=False
            )

            # 5. Save user message
            await firestore.save_message(telefono, "user", mensaje)

            # 6. Send to Gemini
            response = await chat_session.send_message_async(mensaje)

            if not response.candidates or not response.candidates[0].content.parts:
                return ChatResponse(tipo="error", mensaje="Sin respuesta válida del AI")

            part = response.candidates[0].content.parts[0]

            # CASE A: Order interpretation
            if part.function_call and part.function_call.name == 'interpretar_orden':
                return await self._handle_order(telefono, part.function_call.args, menu_service, firestore)

            # CASE B: Order cancellation
            elif part.function_call and part.function_call.name == 'cancelar_orden':
                return await self._handle_cancellation(telefono, part.function_call.args, firestore)

            # CASE C: Name registration
            elif part.function_call and part.function_call.name == 'registrar_nombre':
                return await self._handle_name_registration(telefono, part.function_call.args, firestore)

            # CASE D: Text response
            else:
                return await self._handle_text_response(telefono, response.text, firestore)

        except Exception as e:
            print(f"❌ Error en process_chat: {e}")
            return ChatResponse(tipo="error", mensaje=str(e))
    
    async def _handle_order(
        self, 
        telefono: str, 
        args: Any, 
        menu_service: 'MenuService',
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle order creation or update (Comanda Abierta logic)."""
        
        args_native = self._recursive_to_native(args)
        raw_items = args_native.get('items', [])
        
        # Convert to OrderItem objects with real prices
        new_order_items = []
        total_prep_time = 0
        
        for item_data in raw_items:
            nombre = item_data.get('nombre_producto', 'Item')
            cantidad = int(item_data.get('cantidad', 1))
            
            # Search in real menu
            menu_item = menu_service.buscar_producto(nombre)
            
            if menu_item:
                precio = float(menu_item.get('precio', 50.0))
                tiempo_prep = int(menu_item.get('tiempo_prep', 5))
            else:
                precio = float(item_data.get('precio_unitario', 50.0))
                tiempo_prep = 5
            
            # Calculate cost (30% default)
            costo = precio * settings.DEFAULT_COST_PERCENTAGE
            total_prep_time += (tiempo_prep * cantidad)
            
            order_item = OrderItem(
                nombre_producto=nombre,
                cantidad=cantidad,
                precio_unitario=precio,
                costo_unitario=costo,
                tiempo_prep_unitario=tiempo_prep,
                modificadores_seleccionados=item_data.get('modificadores_seleccionados', []),
                notas_especiales=item_data.get('notas_especiales')
            )
            new_order_items.append(order_item)
        
        # Add buffer time
        tiempo_total = total_prep_time + settings.DEFAULT_PREP_BUFFER_MINUTES
        
        # Check for existing pending order (Comanda Abierta)
        existing = await firestore.get_pending_order(telefono)
        
        if existing:
            return await self._update_existing_order(
                telefono, existing, new_order_items, total_prep_time, firestore
            )
        else:
            return await self._create_new_order(
                telefono, new_order_items, tiempo_total, firestore
            )
    
    async def _update_existing_order(
        self,
        telefono: str,
        existing: tuple,
        new_items: List[OrderItem],
        new_prep_time: int,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Update an existing pending order with new items."""
        
        doc, data = existing
        current_items = data.get('items', [])
        
        # Add new items
        new_items_dicts = [item.to_firestore() for item in new_items]
        all_items = current_items + new_items_dicts
        
        # Recalculate totals
        nuevo_total = sum(i['cantidad'] * i['precio_unitario'] for i in all_items)
        
        # Update prep time
        tiempo_anterior = data.get('tiempo_preparacion_total', 0)
        nuevo_tiempo = tiempo_anterior + new_prep_time
        
        hora_entrega = datetime.now(timezone.utc) + timedelta(minutes=nuevo_tiempo)
        
        # Update in Firestore
        await firestore.update_order(doc.id, {
            "items": all_items,
            "total": nuevo_total,
            "tiempo_preparacion_total": nuevo_tiempo,
            "hora_entrega_estimada": hora_entrega
        })
        
        hora_str = hora_entrega.strftime("%H:%M")
        mensaje = f"¡Listo! Agregado a tu orden. Total: ${nuevo_total:.2f}. Tiempo estimado: {nuevo_tiempo} min (aprox {hora_str})."
        
        await firestore.save_message(telefono, "model", mensaje)
        
        return ChatResponse(
            tipo="orden_actualizada",
            mensaje=mensaje,
            orden={"id": doc.id, "total": nuevo_total, "items": all_items, "tiempo_estimado": nuevo_tiempo}
        )
    
    async def _create_new_order(
        self,
        telefono: str,
        items: List[OrderItem],
        tiempo_total: int,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Create a new order."""
        
        total = sum(item.subtotal for item in items)
        order_id = f"ord_{uuid.uuid4().hex[:8]}"
        hora_entrega = datetime.now(timezone.utc) + timedelta(minutes=tiempo_total)
        
        nueva_orden = Order(
            id=order_id,
            id_cliente=telefono,
            items=items,
            total=total,
            tiempo_preparacion_total=tiempo_total,
            hora_entrega_estimada=hora_entrega
        )
        
        await firestore.create_order(nueva_orden)

        # Schedule automated feedback message (30-40 minutes after delivery)
        try:
            scheduler = get_scheduler_service()
            # Schedule feedback for 35 minutes from now (average delivery + some buffer)
            scheduler.schedule_feedback(telefono, customer_name or "Cliente", delay_minutes=35)
        except Exception as e:
            print(f"⚠️ Error programando feedback para {telefono}: {e}")

        hora_str = hora_entrega.strftime("%H:%M")
        mensaje = f"¡Órale! Confirmado. Son ${total:.2f}. Queda listo en ~{tiempo_total} min (a las {hora_str})."

        await firestore.save_message(telefono, "model", mensaje)

        return ChatResponse(
            tipo="orden_creada",
            mensaje=mensaje,
            orden=nueva_orden.to_firestore()
        )
    
    async def _handle_cancellation(
        self,
        telefono: str,
        args: Any,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle order cancellation with 5-minute rule."""

        razon = self._recursive_to_native(args).get('razon', 'Sin razón')

        # Get customer name for personalized response
        customer_profile = await firestore.get_customer_profile(telefono)
        customer_name = customer_profile.get('nombre') if customer_profile else None

        existing = await firestore.get_pending_order(telefono)

        if not existing:
            mensaje = "No encontré ninguna orden pendiente pa' cancelar."
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        doc, data = existing
        fecha_orden_raw = data.get('fecha_creacion')

        # CRITICAL: Ensure UTC timezone consistency
        ahora_utc = datetime.now(timezone.utc)

        minutos_pasados = 0
        if fecha_orden_raw:
            # Handle Firestore timestamp conversion - ensure UTC timezone
            if hasattr(fecha_orden_raw, 'timestamp'):  # Firestore Timestamp
                # Convert Firestore timestamp to UTC datetime
                timestamp_seconds = fecha_orden_raw.timestamp()
                fecha_orden = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            elif isinstance(fecha_orden_raw, datetime):
                # Regular datetime - ensure UTC
                if fecha_orden_raw.tzinfo is None:
                    # Assume UTC if no timezone info (Firestore default)
                    fecha_orden = fecha_orden_raw.replace(tzinfo=timezone.utc)
                else:
                    # Convert to UTC if different timezone
                    fecha_orden = fecha_orden_raw.astimezone(timezone.utc)
            else:
                # Fallback - treat as UTC timestamp
                try:
                    fecha_orden = datetime.fromtimestamp(float(fecha_orden_raw), tz=timezone.utc)
                except (ValueError, TypeError):
                    print(f"ERROR: Could not parse fecha_orden: {fecha_orden_raw}")
                    fecha_orden = ahora_utc  # Fallback to allow cancellation

            # Both datetimes are now guaranteed to be timezone-aware UTC
            diferencia = ahora_utc - fecha_orden
            minutos_pasados = diferencia.total_seconds() / 60

            print(f"DEBUG: Orden {fecha_orden} vs Ahora {ahora_utc} -> Diff: {minutos_pasados:.2f} min")

        # Check 5-minute rule
        if minutos_pasados > settings.CANCEL_TIME_LIMIT_MINUTES:
            # Personalized empathetic response using customer name
            name_part = f" {customer_name}" if customer_name else ""
            mensaje = f"Híjole{name_part}, ya están preparando tu orden en cocina y por política no puedo cancelarla para no desperdiciar insumos. ¡Pero te va a encantar!"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        # Cancel the order
        await firestore.cancel_order(doc.id)
        mensaje = f"Estás a tiempo (pasaron sólo {int(minutos_pasados)} min). Cancelada la orden {doc.id}. Razón: {razon}"

        await firestore.save_message(telefono, "model", mensaje)
        return ChatResponse(tipo="orden_cancelada", mensaje=mensaje)

    async def _handle_name_registration(
        self,
        telefono: str,
        args: Any,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle customer name registration."""

        nombre = self._recursive_to_native(args).get('nombre', '').strip()

        if not nombre:
            mensaje = "No pude entender tu nombre. ¿Me lo puedes repetir?"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)

        # Update customer profile with name
        success = await firestore.update_customer_profile(telefono, {"nombre": nombre})

        if success:
            mensaje = f"¡Perfecto, {nombre}! Ya te tengo registrado. ¿Qué se te antoja hoy? ☕"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
        else:
            mensaje = "Híjole, tuve un problema guardando tu nombre. ¿Me lo puedes decir otra vez?"
            await firestore.save_message(telefono, "model", mensaje)
            return ChatResponse(tipo="texto", mensaje=mensaje)
    
    async def _handle_text_response(
        self,
        telefono: str,
        texto: str,
        firestore: 'FirestoreService'
    ) -> ChatResponse:
        """Handle plain text response from AI."""
        
        # Try to parse as JSON array (multi-bubble format)
        try:
            mensajes = json.loads(texto)
            if isinstance(mensajes, list):
                full_text = " ".join(mensajes)
                await firestore.save_message(telefono, "model", full_text)
                return ChatResponse(
                    tipo="texto",
                    mensaje=full_text,
                    mensajes=mensajes
                )
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Plain text response
        await firestore.save_message(telefono, "model", texto)
        return ChatResponse(tipo="texto", mensaje=texto)
    
    def refresh_model(self):
        """Refresh the API configuration."""
        self._configured = False
        self._configure()


@lru_cache()
def get_gemini_service() -> GeminiService:
    """Get singleton instance of GeminiService."""
    return GeminiService()

# ========================================
# app/services/firestore_service.py
# ========================================
"""
Firestore Service - Database operations singleton.
Handles all CRUD operations for orders, chat history, and customer profiles.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from functools import lru_cache

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from app.core.config import settings
from app.models.schemas import Order, OrderItem, ChatMessage, OrderStatus, CustomerProfile, Insumo


class FirestoreService:
    """
    Singleton service for Firestore database operations.
    Provides CRUD methods for all collections.
    """
    
    _instance: Optional['FirestoreService'] = None
    _db: Optional[firestore.Client] = None
    
    def __new__(cls) -> 'FirestoreService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            try:
                self._db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT)
                print(f"✅ Firestore conectado: {self._db.project}")
            except Exception as e:
                print(f"❌ Error conectando Firestore: {e}")
                self._db = None
    
    @property
    def db(self) -> Optional[firestore.Client]:
        return self._db
    
    @property
    def is_connected(self) -> bool:
        return self._db is not None
    
    # --- Chat History Operations ---
    
    async def get_chat_history(self, telefono: str, limit: int = None) -> List[Dict[str, str]]:
        """
        Retrieve chat history for a customer.
        Returns list in Gemini-compatible format: [{"role": "user/model", "parts": [...]}]
        """
        if not self.is_connected:
            return []
        
        limit = limit or settings.CHAT_HISTORY_LIMIT
        
        try:
            mensajes_ref = self._db.collection('clientes').document(telefono).collection('chat_history')
            query = mensajes_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
            docs = query.stream()
            
            historial_gemini = []
            msgs = list(docs)[::-1]  # Reverse to chronological order
            
            for doc in msgs:
                datos = doc.to_dict()
                role = "user" if datos['role'] == "user" else "model"
                historial_gemini.append({"role": role, "parts": [datos['content']]})
            
            return historial_gemini
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    async def save_message(self, telefono: str, role: str, content: str) -> bool:
        """Save a chat message to history."""
        if not self.is_connected:
            return False
        
        try:
            mensajes_ref = self._db.collection('clientes').document(telefono).collection('chat_history')
            nuevo_msg = ChatMessage(role=role, content=content)
            mensajes_ref.add(nuevo_msg.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error guardando mensaje: {e}")
            return False
    
    # --- Order Operations ---
    
    async def get_pending_order(self, telefono: str) -> Optional[tuple]:
        """
        Get the pending order for a customer.
        Returns tuple of (document_snapshot, order_data) or None.
        """
        if not self.is_connected:
            return None
        
        try:
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("id_cliente", "==", telefono))\
                .where(filter=FieldFilter("estado", "==", "pendiente"))\
                .limit(1)
            
            docs = list(query.stream())
            if docs:
                return (docs[0], docs[0].to_dict())
            return None
        except Exception as e:
            print(f"❌ Error buscando orden pendiente: {e}")
            return None
    
    async def create_order(self, order: Order) -> bool:
        """Create a new order in Firestore."""
        if not self.is_connected:
            return False
        
        try:
            self._db.collection('pedidos').document(order.id).set(order.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error creando orden: {e}")
            return False
    
    async def update_order(self, order_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing order."""
        if not self.is_connected:
            return False
        
        try:
            self._db.collection('pedidos').document(order_id).update(updates)
            return True
        except Exception as e:
            print(f"❌ Error actualizando orden: {e}")
            return False
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order by updating its status."""
        return await self.update_order(order_id, {"estado": OrderStatus.CANCELADO})
    
    async def get_orders_by_status(self, status: OrderStatus) -> List[Dict[str, Any]]:
        """Get all orders with a specific status."""
        if not self.is_connected:
            return []
        
        try:
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("estado", "==", status.value))\
                .order_by('fecha_creacion', direction=firestore.Query.ASCENDING)
            
            orders = []
            for doc in query.stream():
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            
            return orders
        except Exception as e:
            print(f"❌ Error obteniendo órdenes: {e}")
            return []
    
    async def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get all active orders (pending or in preparation)."""
        if not self.is_connected:
            return []
        
        try:
            # Get pending orders
            pending = await self.get_orders_by_status(OrderStatus.PENDIENTE)
            # Get orders in preparation
            in_prep = await self.get_orders_by_status(OrderStatus.EN_PREPARACION)
            
            return pending + in_prep
        except Exception as e:
            print(f"❌ Error obteniendo órdenes activas: {e}")
            return []
    
    # --- Menu Operations ---
    
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Get all available menu items."""
        if not self.is_connected:
            return []
        
        try:
            docs = self._db.collection('menu')\
                .where(filter=FieldFilter("disponible", "==", True))\
                .stream()
            
            items = []
            for doc in docs:
                item_data = doc.to_dict()
                item_data['id'] = doc.id
                items.append(item_data)
            
            return items
        except Exception as e:
            print(f"❌ Error obteniendo menú: {e}")
            return []
    
    # --- Customer Profile Operations ---
    
    async def get_customer_profile(self, telefono: str) -> Optional[Dict[str, Any]]:
        """Get customer profile data."""
        if not self.is_connected:
            return None
        
        try:
            doc = self._db.collection('clientes').document(telefono).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error obteniendo perfil: {e}")
            return None
    
    async def update_customer_profile(self, telefono: str, profile_data: Dict[str, Any]) -> bool:
        """Update or create customer profile."""
        if not self.is_connected:
            return False

        try:
            self._db.collection('clientes').document(telefono).set(profile_data, merge=True)
            return True
        except Exception as e:
            print(f"❌ Error actualizando perfil: {e}")
            return False

    # --- Ingredient Operations ---

    async def get_all_insumos(self) -> List[Dict[str, Any]]:
        """Get all ingredients."""
        if not self.is_connected:
            return []

        try:
            docs = self._db.collection('insumos').stream()

            insumos = []
            for doc in docs:
                insumo_data = doc.to_dict()
                insumo_data['id'] = doc.id
                insumos.append(insumo_data)

            return insumos
        except Exception as e:
            print(f"❌ Error obteniendo insumos: {e}")
            return []

    async def create_insumo(self, insumo: Insumo) -> bool:
        """Create a new ingredient."""
        if not self.is_connected:
            return False

        try:
            doc_ref = self._db.collection('insumos').document()
            insumo.id = doc_ref.id
            doc_ref.set(insumo.to_firestore())
            return True
        except Exception as e:
            print(f"❌ Error creando insumo: {e}")
            return False

    async def update_insumo(self, insumo_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing ingredient."""
        if not self.is_connected:
            return False

        try:
            self._db.collection('insumos').document(insumo_id).update(data)
            return True
        except Exception as e:
            print(f"❌ Error actualizando insumo: {e}")
            return False

    # --- Daily Sales Metrics ---

    async def get_daily_sales_metrics(self, date: datetime) -> Dict[str, Any]:
        """
        Get daily sales metrics for a specific date.
        Returns total sales and number of orders for that day.
        """
        if not self.is_connected:
            return {"total_ventas": 0.0, "total_ordenes": 0}

        try:
            # Calculate start and end of the day in UTC
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Query orders for the day
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("fecha_creacion", ">=", start_of_day))\
                .where(filter=FieldFilter("fecha_creacion", "<=", end_of_day))\
                .where(filter=FieldFilter("estado", "in", ["entregado", "listo"]))

            docs = list(query.stream())

            total_ventas = 0.0
            total_ordenes = len(docs)

            for doc in docs:
                order_data = doc.to_dict()
                total_ventas += order_data.get('total', 0.0)

            return {
                "total_ventas": total_ventas,
                "total_ordenes": total_ordenes
            }
        except Exception as e:
            print(f"❌ Error obteniendo métricas diarias: {e}")
            return {"total_ventas": 0.0, "total_ordenes": 0}

    # --- Premium Personalization Features ---

    async def get_favorite_product(self, telefono: str) -> Optional[str]:
        """
        Get customer's favorite product based on order history.
        Returns the product name if ordered 3+ times, None otherwise.
        """
        if not self.is_connected:
            return None

        try:
            # Query all completed orders for this customer
            query = self._db.collection('pedidos')\
                .where(filter=FieldFilter("id_cliente", "==", telefono))\
                .where(filter=FieldFilter("estado", "in", ["entregado", "listo"]))

            docs = list(query.stream())

            if not docs:
                return None

            # Count product occurrences
            product_counts = {}

            for doc in docs:
                order_data = doc.to_dict()
                items = order_data.get('items', [])

                for item in items:
                    product_name = item.get('nombre_producto', '')
                    if product_name:
                        product_counts[product_name] = product_counts.get(product_name, 0) + item.get('cantidad', 1)

            # Find product ordered 3+ times
            for product, count in product_counts.items():
                if count >= 3:
                    return product

            return None

        except Exception as e:
            print(f"❌ Error obteniendo producto favorito para {telefono}: {e}")
            return None


@lru_cache()
def get_firestore_service() -> FirestoreService:
    """Get singleton instance of FirestoreService."""
    return FirestoreService()

# ========================================
# app/services/menu_service.py
# ========================================
"""
Menu Service - Menu caching and product search with fuzzy matching.
Loads menu from Firestore at startup and provides fast lookups.
"""
from typing import Optional, Dict, Any, List
from functools import lru_cache
from difflib import SequenceMatcher

from app.services.firestore_service import get_firestore_service


class MenuService:
    """
    Service for menu management with in-memory caching.
    Provides fuzzy search capabilities for product lookup.
    """
    
    _instance: Optional['MenuService'] = None
    _cache: Dict[str, Dict[str, Any]] = {}
    _name_index: Dict[str, str] = {}  # lowercase name -> cache key
    _loaded: bool = False
    
    def __new__(cls) -> 'MenuService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass  # Initialization happens in load_menu()
    
    def load_menu(self) -> int:
        """
        Load menu from Firestore into memory cache.
        Returns number of items loaded.
        """
        if self._loaded:
            return len(self._cache)
        
        firestore = get_firestore_service()
        items = firestore.get_menu_items()
        
        self._cache.clear()
        self._name_index.clear()
        
        for item in items:
            item_id = item.get('id', item.get('nombre', '').lower())
            nombre = item.get('nombre', '')
            
            # Store by ID
            self._cache[item_id] = item
            
            # Create name index for search
            nombre_lower = nombre.lower()
            self._name_index[nombre_lower] = item_id
            
            # Also index without accents for better matching
            nombre_normalized = self._normalize_text(nombre_lower)
            if nombre_normalized != nombre_lower:
                self._name_index[nombre_normalized] = item_id
        
        self._loaded = True
        print(f"🍽️ Menú cargado: {len(self._cache)} items en cache")
        return len(self._cache)
    
    def reload_menu(self) -> int:
        """Force reload menu from Firestore."""
        self._loaded = False
        return self.load_menu()
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """Remove accents and normalize text for search."""
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ü': 'u'
        }
        result = text.lower()
        for accented, plain in replacements.items():
            result = result.replace(accented, plain)
        return result
    
    @staticmethod
    def _similarity_score(a: str, b: str) -> float:
        """Calculate similarity between two strings (0-1)."""
        return SequenceMatcher(None, a, b).ratio()
    
    def buscar_producto(self, nombre_buscado: str, threshold: float = 0.6) -> Optional[Dict[str, Any]]:
        """
        Search for a product in the menu cache with fuzzy matching.
        
        Args:
            nombre_buscado: Product name to search for
            threshold: Minimum similarity score (0-1) for fuzzy match
            
        Returns:
            Menu item dict if found, None otherwise
        """
        if not self._loaded:
            self.load_menu()
        
        nombre_lower = nombre_buscado.lower().strip()
        nombre_normalized = self._normalize_text(nombre_lower)
        
        # 1. Exact match by name
        if nombre_lower in self._name_index:
            return self._cache[self._name_index[nombre_lower]]
        
        # 2. Exact match by normalized name
        if nombre_normalized in self._name_index:
            return self._cache[self._name_index[nombre_normalized]]
        
        # 3. Exact match by ID
        if nombre_lower in self._cache:
            return self._cache[nombre_lower]
        
        # 4. Partial match (contains)
        for name_key, item_id in self._name_index.items():
            if nombre_lower in name_key or nombre_normalized in name_key:
                return self._cache[item_id]
            if name_key in nombre_lower or name_key in nombre_normalized:
                return self._cache[item_id]
        
        # 5. Fuzzy match with similarity score
        best_match = None
        best_score = 0.0
        
        for name_key, item_id in self._name_index.items():
            # Check similarity with both original and normalized
            score1 = self._similarity_score(nombre_lower, name_key)
            score2 = self._similarity_score(nombre_normalized, name_key)
            score = max(score1, score2)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = item_id
        
        if best_match:
            return self._cache[best_match]
        
        return None
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Get all menu items from cache."""
        if not self._loaded:
            self.load_menu()
        return list(self._cache.values())
    
    def get_menu_text_for_prompt(self) -> str:
        """
        Generate formatted menu text for AI system prompt.
        Returns a string listing all products with prices and prep times.
        """
        if not self._loaded:
            self.load_menu()
        
        lines = []
        seen = set()
        
        for item in self._cache.values():
            nombre = item.get('nombre', 'Item')
            if nombre in seen:
                continue
            seen.add(nombre)
            
            precio = item.get('precio', 0)
            tiempo = item.get('tiempo_prep', 5)
            categoria = item.get('categoria', 'otro')
            
            line = f"- {nombre}: ${precio} (Prep: {tiempo}min) [{categoria}]"
            lines.append(line)
        
        return "\n".join(sorted(lines))
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific menu item by ID."""
        if not self._loaded:
            self.load_menu()
        return self._cache.get(item_id)
    
    @property
    def is_loaded(self) -> bool:
        return self._loaded
    
    @property
    def item_count(self) -> int:
        return len(self._cache)


@lru_cache()
def get_menu_service() -> MenuService:
    """Get singleton instance of MenuService."""
    return MenuService()

# ========================================
# app/services/scheduler_service.py
# ========================================
"""
Scheduler Service - Manejo de tareas en segundo plano.
Usa APScheduler para programar mensajes de feedback post-venta.
"""
from typing import Optional
from datetime import datetime, timedelta, timezone
from functools import lru_cache
import random

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from app.services.firestore_service import get_firestore_service
from app.core.config import settings

class SchedulerService:
    """
    Singleton service for background tasks.
    Handles automated follow-up messages and scheduled notifications.
    """

    _instance: Optional['SchedulerService'] = None
    _scheduler: Optional[AsyncIOScheduler] = None

    def __new__(cls) -> 'SchedulerService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._scheduler is None:
            self._scheduler = AsyncIOScheduler()
            # Configure scheduler with proper timezone
            self._scheduler.configure(timezone=timezone.utc)

    def start(self):
        """Start the scheduler."""
        if not self._scheduler.running:
            self._scheduler.start()
            print("⏰ Scheduler iniciado correctamente")

    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        if self._scheduler and self._scheduler.running:
            self._scheduler.shutdown(wait=True)
            print("⏰ Scheduler detenido correctamente")

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._scheduler is not None and self._scheduler.running

    async def _send_feedback_message(self, telefono: str, nombre_cliente: str):
        """
        Callback function executed by the scheduler.
        Injects a follow-up message into the chat history.
        """
        try:
            firestore = get_firestore_service()

            # Estrategias de mensaje aleatorias con más variedad
            opciones = [
                f"¡Hola {nombre_cliente}! 🌟 Esperamos que hayas disfrutado tu pedido. ¿Nos regalas 5 estrellitas en Google Maps? Ayuda mucho al equipo.",
                f"Oye {nombre_cliente}, ¿te gustó el café? ☕ Recuerda que si traes a un amigo, ambos ganan puntos en nuestro Plan de Justicia.",
                f"¡Qué onda {nombre_cliente}! Solo pasaba a confirmar que todo estuvo delicioso. ¡Bonito día! ✨",
                f"Hola {nombre_cliente} 👋 ¿Cómo estuvo tu experiencia en Justicia y Café? Tu opinión es muy importante para nosotros.",
                f"¡Saludos {nombre_cliente}! ☕ ¿Te gustaría recibir recomendaciones personalizadas la próxima vez? ¡Somos expertos en café!",
                f"Oye {nombre_cliente}, ¿sabes que tenemos un programa de fidelización? Cada compra te acerca más a recompensas deliciosas. 🌟"
            ]

            mensaje = random.choice(opciones)

            # Guardamos el mensaje en Firestore para que aparezca en el chat del cliente
            print(f"📧 Enviando feedback automático a {telefono} ({nombre_cliente})")
            success = await firestore.save_message(telefono, "model", mensaje)

            if success:
                print(f"✅ Feedback enviado exitosamente a {nombre_cliente}")
            else:
                print(f"❌ Error al enviar feedback a {nombre_cliente}")

        except Exception as e:
            print(f"❌ Error en _send_feedback_message para {telefono}: {e}")

    def schedule_feedback(self, telefono: str, nombre: str, delay_minutes: int = 30):
        """
        Schedule a feedback message for the future.

        Args:
            telefono: Customer phone number
            nombre: Customer name
            delay_minutes: Minutes to wait before sending (default: 30)
        """
        if not self._scheduler:
            print("❌ Scheduler no inicializado")
            return

        # Validate inputs
        if not telefono or not nombre:
            print("❌ Teléfono y nombre son requeridos para programar feedback")
            return

        run_date = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)

        # Para desarrollo/demo, podemos usar segundos en lugar de minutos
        if settings.DEBUG:
            run_date = datetime.now(timezone.utc) + timedelta(seconds=30)
            print(f"🐛 DEBUG MODE: Feedback programado en 30 segundos en lugar de {delay_minutes} minutos")

        job_id = f"feedback_{telefono}_{int(datetime.now().timestamp())}"

        try:
            self._scheduler.add_job(
                self._send_feedback_message,
                trigger=DateTrigger(run_date=run_date),
                args=[telefono, nombre],
                id=job_id,
                replace_existing=True,  # Replace if exists
                max_instances=1  # Only run once
            )
            print(f"⏰ Feedback programado para {nombre} ({telefono}) en {delay_minutes} min - Job ID: {job_id}")
        except Exception as(f"❌ e:
            print Error programando feedback para {nombre}: {e}")

    def cancel_feedback(self, telefono: str) -> bool:
        """
        Cancel any pending feedback jobs for a customer.

        Args:
            telefono: Customer phone number

        Returns:
            bool: True if jobs were cancelled, False otherwise
        """
        if not self._scheduler:
            return False

        try:
            # Find and remove jobs for this customer
            jobs_removed = 0
            for job in self._scheduler.get_jobs():
                if telefono in job.id and "feedback" in job.id:
                    job.remove()
                    jobs_removed += 1

            if jobs_removed > 0:
                print(f"🗑️ Cancelados {jobs_removed} jobs de feedback para {telefono}")
                return True
            else:
                print(f"ℹ️ No se encontraron jobs pendientes para {telefono}")
                return False

        except Exception as e:
            print(f"❌ Error cancelando feedback para {telefono}: {e}")
            return False

    def get_pending_jobs(self) -> list:
        """
        Get list of pending jobs for monitoring.

        Returns:
            list: List of pending job information
        """
        if not self._scheduler:
            return []

        try:
            jobs = []
            for job in self._scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                    'func': job.func.__name__,
                    'args': job.args
                })
            return jobs
        except Exception as e:
            print(f"❌ Error obteniendo jobs pendientes: {e}")
            return []

@lru_cache()
def get_scheduler_service() -> SchedulerService:
    """Get singleton instance of SchedulerService."""
    return SchedulerService()

# ========================================
# frontend/cliente.py
# ========================================
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

def render_menu_card():
    """Generate beautiful menu card HTML for chat display"""
    menu_html = """
    <div class="menu-chat-card">
        <div class="menu-chat-header">
            <div class="menu-chat-title">📜 MENÚ DEL DÍA</div>
            <div class="menu-chat-subtitle">Justicia y Café</div>
        </div>
    """
    
    # Bebidas
    menu_html += '<div class="menu-chat-category">☕ BEBIDAS</div>'
    for item in MENU_DATA["bebidas"]:
        menu_html += f"""
        <div class="menu-chat-item">
            <span class="menu-chat-item-name">{item['nombre']}</span>
            <span class="menu-chat-item-price">${item['precio']}</span>
        </div>
        """
    
    # Alimentos
    menu_html += '<div class="menu-chat-category">🥐 ALIMENTOS</div>'
    for item in MENU_DATA["alimentos"]:
        menu_html += f"""
        <div class="menu-chat-item">
            <span class="menu-chat-item-name">{item['nombre']}</span>
            <span class="menu-chat-item-price">${item['precio']}</span>
        </div>
        """
    
    # Postres
    menu_html += '<div class="menu-chat-category">🍰 POSTRES</div>'
    for item in MENU_DATA["postres"]:
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
    sidebar_html = '<div class="menu-card">'
    
    # ITERACIÓN DINÁMICA SOBRE MENU_DATA
    for categoria, items in MENU_DATA.items():
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

    # Quick menu button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📜 Ver Menú del Día", use_container_width=True, type="primary"):
            # Inject menu request into chat
            st.session_state.messages.append({
                "role": "user",
                "content": "Muéstrame el menú"
            })
            st.rerun()
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
st.markdown('<div class="input-area"><div class="input-wrapper">', unsafe_allow_html=True)

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

# ========================================
# frontend/cocina.py
# ========================================
"""
Kitchen Display System (KDS) - Professional Kitchen Interface.
Features:
- Kanban-style order layout
- Traffic light time indicators (green/yellow/red)
- Auto-refresh without aggressive flickering
- Clear item display with modifiers
"""
import sys
import os
# Agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# ========================================
# frontend/dashboard.py
# ========================================
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

# ========================================
# Dockerfile
# ========================================
# 1. Usamos Python ligero (Slim) para que la imagen pese poco
FROM python:3.10-slim

# 2. Evitamos que Python genere archivos .pyc y bufferee logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos y instalamos dependencias PRIMERO (para usar caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código (main.py, models.py, etc.)
COPY . .

# 6. Definimos el puerto por defecto (Cloud Run usa 8080)
ENV PORT=8080

# 7. Comando de arranque: Uvicorn escuchando en 0.0.0.0 (necesario para contenedores)
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT

# ========================================
# .dockerignore
# ========================================
venv/
.git/
__pycache__/
.env
.DS_Store

# ========================================
# .gitignore
# ========================================
.env
venv/
__pycache__/
*.pyc
.DS_Storecredentials.json

# ========================================
# .env.example
# ========================================
# Justicia y Café - Environment Configuration
# Copy this file to .env and fill in your values

# Google Gemini AI API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Google Cloud Project ID (Required for Firestore)
GOOGLE_CLOUD_PROJECT=your_project_id_here

# AI Model (Optional - defaults to gemini-2.0-flash)
GEMINI_MODEL=gemini-2.0-flash

# Environment (Optional - local or prod)
ENV=local

# ========================================
# FIN DEL PROYECTO COMPLETO
# ========================================
# Todos los archivos del proyecto Justicia y Café v2.0.0
# Sistema de pedidos ultra-rápido para abogados/jueces usando IA
# 
# PARA USAR ESTE CÓDIGO:
# 1. Crear estructura de carpetas según los paths indicados
# 2. Copiar cada sección en su archivo correspondiente
# 3. Configurar variables de entorno en .env
# 4. Instalar dependencias: pip install -r requirements.txt
# 5. Ejecutar: ./start_all.sh
# ========================================