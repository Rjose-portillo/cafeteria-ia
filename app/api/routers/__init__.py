"""
API Routers module
"""
from app.api.routers.chat import router as chat_router
from app.api.routers.orders import router as orders_router
from app.api.routers.menu import router as menu_router

__all__ = ["chat_router", "orders_router", "menu_router"]