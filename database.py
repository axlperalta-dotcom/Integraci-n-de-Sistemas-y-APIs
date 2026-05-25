import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

DB_PATH = "legacy_db.sqlite"

def init_db():
    """Inicializa la base de datos con datos de prueba si no existe."""
    if os.path.exists(DB_PATH):
        return

    logger.info("Inicializando la base de datos simulada con soporte RLS...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla principal con datos mixtos y credenciales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL,        -- DATO SENSIBLE
            ssn TEXT NOT NULL UNIQUE,    -- DATO SENSIBLE
            hire_date TEXT NOT NULL
        )
    ''')

    # Insertar datos ficticios
    sample_data = [
        (1, "alice.s", "pass123", "Alice", "Smith", "Engineering", "Software Engineer", 95000, "123-45-6789", "2021-03-15"),
        (2, "bob.j", "pass123", "Bob", "Johnson", "Engineering", "Senior Software Engineer", 120000, "987-65-4321", "2019-07-01"),
        (3, "charlie.w", "pass123", "Charlie", "Williams", "HR", "HR Manager", 85000, "456-78-9012", "2020-11-20"),
        (4, "diana.b", "pass123", "Diana", "Brown", "Sales", "Sales Representative", 65000, "321-65-0987", "2022-01-10"),
        (5, "eve.d", "pass123", "Eve", "Davis", "Engineering", "QA Engineer", 80000, "567-89-0123", "2021-09-05"),
        # USUARIO LEGAL (VIP)
        (99, "legal", "admin", "Usuario", "Legal", "Executive", "Director", 250000, "000-00-0000", "2015-01-01")
    ]

    cursor.executemany('''
        INSERT INTO employees (id, username, password, first_name, last_name, department, role, salary, ssn, hire_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada correctamente.")

def execute_query(query: str) -> list[dict]:
    """Ejecuta una consulta SQL de solo lectura y devuelve los resultados."""
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        return result
    except sqlite3.Error as e:
        logger.error(f"Error ejecutando consulta: {e}")
        raise ValueError(f"Database error: {str(e)}")
    finally:
        conn.close()

def authenticate_user(username, password):
    """Verifica credenciales y devuelve el ID del empleado."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name FROM employees WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1]}
    return None

def get_db_schema() -> str:
    """Devuelve el esquema completo de la base de datos (para uso interno)."""
    return '''
    Table: employees
    Columns:
    - id (INTEGER, PRIMARY KEY)
    - username (TEXT)
    - password (TEXT)
    - first_name (TEXT)
    - last_name (TEXT)
    - department (TEXT)
    - role (TEXT)
    - salary (REAL) -- SENSITIVE
    - ssn (TEXT)    -- SENSITIVE
    - hire_date (TEXT)
    '''
