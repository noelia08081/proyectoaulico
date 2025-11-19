# 🚀 Guía Rápida para Iniciar la Aplicación

## Opción 1: Script Automático (Recomendado)

Ejecuta el script de configuración:

```bash
./iniciar_app.sh
```

Este script:
- Crea el entorno virtual si no existe
- Instala todas las dependencias
- Aplica las migraciones de Django

Luego sigue las instrucciones que aparecen en pantalla.

## Opción 2: Manual (Paso a Paso)

### Paso 1: Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Aplicar migraciones de Django

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 4: (Opcional) Crear categorías de ejemplo

```bash
python manage.py shell
```

Dentro del shell de Python:
```python
from tareas.models import Categoria

# Crear categorías de ejemplo
Categoria.objects.create(nombre="Salario", tipo="ingreso", icono="💼", color="#2ecc71")
Categoria.objects.create(nombre="Alimentación", tipo="gasto", icono="🍔", color="#e74c3c")
Categoria.objects.create(nombre="Transporte", tipo="gasto", icono="🚗", color="#3498db")
Categoria.objects.create(nombre="Entretenimiento", tipo="gasto", icono="🎮", color="#9b59b6")
Categoria.objects.create(nombre="Educación", tipo="gasto", icono="📚", color="#f39c12")

# Salir
exit()
```

### Paso 5: (Opcional) Crear superusuario para Django Admin

```bash
python manage.py createsuperuser
```

## 🏃 Ejecutar la Aplicación

**IMPORTANTE**: Necesitas abrir **DOS terminales** diferentes.

### Terminal 1 - Servidor Django (API)

```bash
# Asegúrate de estar en el directorio del proyecto
cd /Users/mambo/Desktop/Sistemas/proyectoaulico

# Activa el entorno virtual
source venv/bin/activate

# Inicia el servidor Django
python manage.py runserver
```

Deberías ver algo como:
```
Starting development server at http://127.0.0.1:8000/
```

### Terminal 2 - Aplicación Streamlit (Frontend)

```bash
# Asegúrate de estar en el directorio del proyecto
cd /Users/mambo/Desktop/Sistemas/proyectoaulico

# Activa el entorno virtual
source venv/bin/activate

# Inicia Streamlit
streamlit run app_streamlit.py
```

Deberías ver algo como:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

## 🌐 Acceder a la Aplicación

Una vez que ambos servidores estén corriendo:

1. **Aplicación Principal (Streamlit)**: 
   - Abre tu navegador en: `http://localhost:8501`
   - Aquí verás la interfaz principal con todas las funcionalidades

2. **Panel de Administración Django**:
   - Abre tu navegador en: `http://localhost:8000/admin`
   - Inicia sesión con el superusuario que creaste
   - Aquí puedes gestionar todos los datos directamente

3. **API REST**:
   - Accede a: `http://localhost:8000/api/`
   - Verás la lista de endpoints disponibles

## ✅ Verificar que Todo Funciona

1. **Verifica Django**: Abre `http://localhost:8000/api/categorias/` - deberías ver `[]` (lista vacía) o las categorías que creaste

2. **Verifica Streamlit**: Abre `http://localhost:8501` - deberías ver el dashboard de educación financiera

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'django'"
- **Solución**: Asegúrate de haber activado el entorno virtual y de haber instalado las dependencias

### Error: "Port 8000 already in use"
- **Solución**: Django ya está corriendo en otra terminal, o cambia el puerto:
  ```bash
  python manage.py runserver 8001
  ```
  (Luego actualiza `API_BASE_URL` en `app_streamlit.py`)

### Error: "Port 8501 already in use"
- **Solución**: Streamlit ya está corriendo, o cambia el puerto:
  ```bash
  streamlit run app_streamlit.py --server.port 8502
  ```

### Error: "No migrations to apply"
- **Solución**: Esto es normal si ya aplicaste las migraciones. Si es la primera vez, ejecuta:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### La aplicación Streamlit no se conecta a Django
- **Solución**: 
  1. Verifica que Django esté corriendo en `http://localhost:8000`
  2. Abre `http://localhost:8000/api/` en tu navegador para verificar
  3. Si cambiaste el puerto de Django, actualiza `API_BASE_URL` en `app_streamlit.py`

## 📝 Notas Importantes

- **Siempre activa el entorno virtual** antes de ejecutar comandos
- **Mantén ambas terminales abiertas** mientras uses la aplicación
- **Django debe estar corriendo antes** de abrir Streamlit
- Los datos se guardan en `db.sqlite3` (base de datos SQLite)

## 🎉 ¡Listo!

Una vez que ambos servidores estén corriendo, podrás:
- ✅ Ver el dashboard financiero
- ✅ Agregar transacciones
- ✅ Crear presupuestos
- ✅ Establecer metas financieras
- ✅ Ver análisis y gráficos
- ✅ Acceder a lecciones educativas

¡Disfruta explorando la aplicación! 💵📊

