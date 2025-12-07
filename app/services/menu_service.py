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