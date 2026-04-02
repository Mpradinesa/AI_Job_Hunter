# AI Job Hunter 🎯

**AI Job Hunter** es un asistente inteligente diseñado para optimizar la búsqueda de empleo en el sector tecnológico. Combina **Python**, **IA Generativa (Gemini)** y **Análisis de Datos** para encontrar las mejores oportunidades según un perfil híbrido del usuario, transformando la búsqueda de empleo en un proceso de Business Intelligence. Desarrollado por una  Full Stack Developer.

## 🚀 Características Principales
- **Análisis de Perfil Híbrido:** Cruza datos técnicos (Python, React) con visión de negocio (Logística, Retail, Finanzas).
- **Control de Duplicados:** Implementación de hashing **SHA-256** para evitar el re-procesamiento de avisos.
- **Scoring de Match:** Evaluación de vacantes de GetOnBrd para priorizar las de mayor potencial.
- **Escalabilidad:** Arquitectura preparada para migrar a una aplicación móvil (Kotlin/Jetpack Compose).

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **IA:** Google Gemini Pro API
- **Persistencia:** Sistema de logs indexados (Hash-based)
- **Entorno:** Dockerizado (en progreso)

## 📋 Cómo empezar
1. Clona el repositorio.
2. Crea tu archivo `.env` basado en `.env.example`.
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta: `python src/main.py`