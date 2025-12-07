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
    
    print("✅ Servicios inicializados correctamente")
    
    yield
    
    # Shutdown
    print("👋 Cerrando aplicación...")


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