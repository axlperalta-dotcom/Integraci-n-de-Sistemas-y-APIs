# Secure Text-to-SQL AI Middleware

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey)
![Security](https://img.shields.io/badge/Row--Level%20Security-Active-success)

## 📌 Resumen del Proyecto
Este proyecto es una solución integral "Full-Stack" diseñada para democratizar el acceso a los datos corporativos. Actúa como un middleware seguro entre un Modelo de Lenguaje Grande (LLM) y una base de datos legado. 

Permite a usuarios no técnicos hacer preguntas en lenguaje natural (ej. *"¿Cuántos empleados hay en el departamento de ingeniería?"*) y obtener resultados en tiempo real a través de una interfaz de usuario Premium ("Glassmorphism"), todo mientras se garantiza la protección de información sensible mediante técnicas avanzadas de seguridad cibernética.

## ✨ Características Principales
1. **Motor Text-to-SQL**: Traducción de lenguaje natural a sentencias SQL exactas y optimizadas.
2. **Capa de Seguridad (RLS - Row Level Security)**:
   - **Autorización y Autenticación**: Sistema de login y protección de endpoints por `API Key`.
   - **Filtrado de Esquema Ofuscado**: Se le ocultan al LLM las columnas críticas (como salarios o identificadores gubernamentales) para prevenir inyecciones o alucinaciones peligrosas.
   - **Enmascaramiento Dinámico**: Si se solicita información transversal (ej. `SELECT *`), el sistema detecta quién es el usuario logueado. Permite ver en claro sus propios datos y enmascara dinámicamente (con `****MASKED****`) los datos de otros empleados.
3. **Frontend Premium**: Interfaz moderna desarrollada con HTML/CSS/JS nativo, incorporando efectos visuales "Glassmorphism", modo oscuro y renderizado dinámico (Tarjetas de KPI para métricas únicas y Tablas de datos para registros masivos).
4. **Documentación Automática**: Generación de Swagger UI (`/apidocs`) para facilitar la integración por parte de terceros.

## 🚀 Arquitectura
- **Backend Framework**: Flask + Flasgger
- **Base de Datos**: SQLite (simulando un entorno legacy)
- **Frontend**: Vanilla JS, CSS3, HTML5
- **Seguridad**: Decoradores personalizados y middleware de intercepción de datos.

## 📦 Estructura del Proyecto
```text
/
├── database.py       # Inicialización de DB y ejecución segura de SQL
├── llm_service.py    # Motor de prompting e integración con IA
├── main.py           # Aplicación Flask y endpoints principales
├── security.py       # Lógica de RLS y enmascaramiento de datos
├── requirements.txt  # Dependencias del proyecto
├── /static
│   ├── app.js        # Lógica asíncrona del cliente
│   └── style.css     # Sistema de diseño Premium
├── /templates
│   └── index.html    # Estructura del Frontend interactivo
└── /docs             # Archivos multimedia y walkthrough
```

## 🛠 Instalación y Uso
1. Clona el repositorio e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor local:
   ```bash
   python main.py
   ```
3. Navega a `http://127.0.0.1:8000/` para acceder al Frontend, o a `/apidocs` para explorar la API.

---
*Desarrollado como demostración de integración segura de Inteligencia Artificial en entornos corporativos.*
