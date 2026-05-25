from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
import logging

from database import init_db, execute_query, authenticate_user
from security import require_api_key, get_safe_schema, mask_sensitive_data
from llm_service import get_sql_from_text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar base de datos
init_db()

# Crear aplicación Flask
app = Flask(__name__)

# Configurar Swagger
app.config['SWAGGER'] = {
    'title': 'Text-to-SQL Secure API',
    'uiversion': 3,
    'description': 'Middleware entre un LLM y una base de datos legacy, con protección de datos sensibles.'
}
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Text-to-SQL Secure API",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header"
        }
    },
    "security": [
        {"APIKeyHeader": []}
    ]
})

@app.route("/")
def read_root():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing credentials"}), 400
    
    user_info = authenticate_user(data['username'], data['password'])
    if user_info:
        return jsonify({"success": True, "user": user_info}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route("/query", methods=['POST'])
@require_api_key
def process_natural_language_query():
    """
    Consulta SQL mediante Lenguaje Natural
    ---
    tags:
      - Consultas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            question:
              type: string
              example: "¿Cuántos empleados hay en el departamento de ingeniería?"
              description: "Pregunta en lenguaje natural para consultar la base de datos."
    responses:
      200:
        description: Respuesta exitosa
        schema:
          type: object
          properties:
            original_question:
              type: string
            generated_sql:
              type: string
            data:
              type: array
              items:
                type: object
      400:
        description: Petición inválida
      403:
        description: No autorizado (Falta API Key)
      500:
        description: Error interno del servidor
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Bad Request: 'question' is required in JSON body"}), 400

    question = data['question']
    current_user_id = data.get('employee_id') # Puede ser None si es anonimo

    try:
        # 1. Obtener el esquema seguro
        safe_schema = get_safe_schema()
        
        # 2. Generar SQL
        sql_query = get_sql_from_text(question, safe_schema)
        
        # 3. Ejecutar la consulta
        raw_results = execute_query(sql_query)
        
        # 4. Enmascarar con RLS (pasando el usuario actual)
        safe_results = mask_sensitive_data(raw_results, current_user_id)
        
        return jsonify({
            "original_question": question,
            "generated_sql": sql_query,
            "data": safe_results
        }), 200
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error interno: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
