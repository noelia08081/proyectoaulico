#!/bin/bash

echo "🚀 Iniciando aplicación de Educación Financiera"
echo "================================================"
echo ""

# Verificar si existe entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar e instalar dependencias
echo "📥 Verificando dependencias..."
if ! python -c "import django" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar migraciones
echo "🗄️  Verificando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "✅ Configuración completada!"
echo ""
echo "📋 Para iniciar la aplicación, abre DOS terminales:"
echo ""
echo "Terminal 1 - Django (API):"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Terminal 2 - Streamlit (Frontend):"
echo "  source venv/bin/activate"
echo "  streamlit run app_streamlit.py"
echo ""
echo "🌐 Luego abre en tu navegador:"
echo "  - Streamlit: http://localhost:8501"
echo "  - Django Admin: http://localhost:8000/admin"
echo ""

