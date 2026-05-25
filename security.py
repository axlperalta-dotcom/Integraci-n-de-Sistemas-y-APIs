from typing import List, Dict, Any
from functools import wraps
from flask import request, jsonify

API_KEY = "my-secret-token"
API_KEY_NAME = "X-API-Key"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get(API_KEY_NAME)
        if key != API_KEY:
            return jsonify({"error": "Forbidden: Invalid or missing API Key"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- PROTECCIÓN DE DATOS (Row-Level Security) ---

SENSITIVE_COLUMNS = ["salary", "ssn", "password"]

def get_safe_schema() -> str:
    """Esquema sin columnas sensibles."""
    return '''
    Table: employees
    Columns:
    - id (INTEGER, PRIMARY KEY)
    - first_name (TEXT)
    - last_name (TEXT)
    - department (TEXT)
    - role (TEXT)
    - hire_date (TEXT)
    '''

def mask_sensitive_data(rows: List[Dict[str, Any]], current_user_id: int = None) -> List[Dict[str, Any]]:
    """
    Filtro de post-procesamiento con Row-Level Security (RLS).
    Si la fila pertenece al current_user_id, se desenmascara la información.
    Si pertenece a otro empleado, se ocultan los campos sensibles.
    """
    safe_rows = []
    for row in rows:
        safe_row = {}
        row_id = row.get('id')
        
        # ¿Es el usuario actual viendo sus propios datos?
        is_owner = (current_user_id is not None) and (row_id == current_user_id)
        
        for key, value in row.items():
            key_lower = key.lower()
            
            # Nunca mostrar contraseñas
            if key_lower == "password":
                continue
                
            # Si es sensible y no es el dueño, enmascarar
            if key_lower in SENSITIVE_COLUMNS and not is_owner:
                safe_row[key] = "****MASKED****"
            else:
                safe_row[key] = value
        safe_rows.append(safe_row)
    return safe_rows
