#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print('✅ Path injection working')

try:
    from app.services.firestore_service import get_firestore_service
    print('✅ Firestore service import: OK')
except Exception as e:
    print(f'❌ Firestore service import: {e}')

try:
    from app.services.menu_service import get_menu_service
    print('✅ Menu service import: OK')
except Exception as e:
    print(f'❌ Menu service import: {e}')

try:
    from app.models.schemas import Order, OrderItem, OrderStatus
    print('✅ Schemas import: OK')
except Exception as e:
    print(f'❌ Schemas import: {e}')

print('✅ All imports tested successfully!')