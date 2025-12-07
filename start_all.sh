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

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
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

# Esperar un poco para que los servicios inicien visualmente
sleep 3

# Verificar que todos los servicios estén corriendo
log "🔍 Verificando servicios..."

SERVICES_UP=0
TOTAL_SERVICES=3

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

echo
log "🎉 ¡Todos los servicios iniciados exitosamente!"
log "📊 Estado: $SERVICES_UP/$TOTAL_SERVICES servicios activos"
echo
info "🌐 URLs de acceso (Abre en tu navegador de Windows):"
info "   🔧 Backend API: http://localhost:8000/docs"
info "   💬 Cliente:     http://localhost:8501"
info "   🍳 Cocina:      http://localhost:8502"
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