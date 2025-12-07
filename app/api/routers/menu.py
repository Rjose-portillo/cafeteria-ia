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