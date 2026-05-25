import logging

logger = logging.getLogger(__name__)

def generate_sql_prompt(question: str, safe_schema: str) -> str:
    """Construye el prompt que sería enviado al LLM real."""
    prompt = f"""
    Actúa como un experto en SQL. 
    Tienes acceso a una base de datos SQLite con el siguiente esquema:
    
    {safe_schema}
    
    Instrucciones críticas:
    1. Responde ÚNICAMENTE con una consulta SQL válida (sin markdown, sin explicaciones).
    2. Usa SOLO las columnas especificadas en el esquema.
    3. Asegúrate de que la consulta responda a la pregunta del usuario.
    
    Pregunta del usuario: {question}
    SQL:
    """
    return prompt

def mock_llm_call(prompt: str, question: str) -> str:
    """
    Simula la respuesta de un LLM analizando palabras clave en la pregunta.
    En un entorno real, aquí harías la llamada a OpenAI, Anthropic, Gemini, etc.
    """
    logger.info(f"Enviando prompt al LLM (Simulado):\n{prompt}")
    
    question_lower = question.lower()
    
    # Lógica rudimentaria para simular Text-to-SQL
    if "cuantos" in question_lower or "cuántos" in question_lower:
        if "ingeniería" in question_lower or "engineering" in question_lower:
            return "SELECT COUNT(*) as count FROM employees WHERE department = 'Engineering';"
        else:
            return "SELECT COUNT(*) as count FROM employees;"
    elif "nombre" in question_lower and "ingeniería" in question_lower:
        return "SELECT first_name, last_name FROM employees WHERE department = 'Engineering';"
    elif "todos" in question_lower or "todo" in question_lower:
        return "SELECT * FROM employees;"
    elif "seguro social" in question_lower or "ssn" in question_lower:
        # El LLM no debería poder hacer esto si el prompt usó safe_schema, 
        # pero si el usuario explícitamente pide "ssn", el mock intentará consultarlo 
        # para demostrar cómo la capa de seguridad bloquea/enmascara.
        return "SELECT first_name, ssn FROM employees;"
    elif "salario" in question_lower or "salary" in question_lower:
        return "SELECT first_name, salary FROM employees;"
    elif "privado" in question_lower or "confidencial" in question_lower:
        return "SELECT id, first_name, last_name, salary, ssn FROM employees;"
    else:
        # Fallback genérico
        return "SELECT first_name, last_name, department FROM employees LIMIT 5;"

def get_sql_from_text(question: str, safe_schema: str) -> str:
    """Función principal que coordina la generación de SQL."""
    prompt = generate_sql_prompt(question, safe_schema)
    sql_query = mock_llm_call(prompt, question)
    
    logger.info(f"SQL generado por LLM: {sql_query}")
    return sql_query.strip()
