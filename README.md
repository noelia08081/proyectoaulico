# proyectoaulico
app de proyecto de facultad

## 📦 Librerías Necesarias

Este proyecto requiere las siguientes librerías de Python:

### Instalación

Para instalar todas las dependencias, ejecuta:

```bash
pip install -r requirements.txt
```

**Nota:** Estas versiones han sido probadas y son compatibles con Python 3.13. Pandas 2.3.3 incluye soporte nativo para Python 3.13.

### Dependencias Principales

| Paquete | Versión | Estado |
|---------|---------|--------|
| **Django** | 4.2.7 | ✅ Instalado |
| **Django REST Framework** | 3.14.0 | ✅ Instalado |
| **Streamlit** | 1.28.1 | ✅ Instalado |
| **Pandas** | 2.3.3 | ✅ Instalado (compatible con Python 3.13) |
| **Plotly** | 5.18.0 | ✅ Instalado |
| **Requests** | 2.31.0 | ✅ Instalado |
| **python-dotenv** | 1.0.0 | ✅ Instalado |
| **django-cors-headers** | 4.3.1 | ✅ Instalado (requerido para CORS) |
| **numpy** | (dependencia) | ✅ Instalado automáticamente con pandas/streamlit |

### Descripción de Uso

- **Django**: Backend del proyecto, maneja la base de datos y la API REST
- **Django REST Framework**: Crea los endpoints de la API que consume Streamlit
- **Streamlit**: Frontend de la aplicación de educación financiera
- **Requests**: Permite que Streamlit se comunique con la API de Django
- **Pandas y Plotly**: Se usan para análisis de datos y visualizaciones en Streamlit