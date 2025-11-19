# 🪟 Guía de Instalación para Windows

Documentación completa para instalar y configurar el sistema de educación financiera en Windows.

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10 o superior
- **Python**: 3.8 o superior (recomendado 3.10, 3.11 o 3.13)
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espacio en disco**: 500MB libres
- **Conexión a Internet**: Para descargar dependencias

**Nota sobre Python 3.13:**
- Python 3.13 es compatible con este proyecto
- El `requirements.txt` incluye versiones compatibles (numpy>=2.0.0, streamlit>=1.39.0)
- Si encuentras problemas con numpy, instálalo primero: `pip install numpy>=2.0.0`

## 🔧 Instalación de Software Base

### Paso 1: Instalar Python

1. **Descargar Python:**
   - Visita: https://www.python.org/downloads/
   - Descarga la versión más reciente (Python 3.10, 3.11 o 3.13 recomendado)
   - Elige el instalador "Windows installer (64-bit)"

2. **Ejecutar el Instalador:**
   - Haz doble clic en el archivo descargado (ej: `python-3.11.x-amd64.exe`)
   - **IMPORTANTE**: Marca la casilla **"Add Python to PATH"** ✅
   - Haz clic en "Install Now"
   - Espera a que termine la instalación

3. **Verificar la Instalación:**
   - Abre PowerShell o CMD (Símbolo del sistema)
   - Ejecuta:
   ```powershell
   python --version
   ```
   - Deberías ver algo como: `Python 3.11.x`

4. **Verificar pip:**
   ```powershell
   pip --version
   ```
   - Deberías ver: `pip 23.x.x`

**⚠️ Si no funciona:**
- Reinicia tu terminal después de instalar Python
- Verifica que Python esté en el PATH del sistema
- Prueba con `py` en lugar de `python`:
  ```powershell
  py --version
  ```

### Paso 2: Instalar Git (Opcional)

Si necesitas clonar el repositorio:

1. **Descargar Git:**
   - Visita: https://git-scm.com/download/win
   - Descarga el instalador

2. **Instalar Git:**
   - Ejecuta el instalador
   - Sigue las instrucciones (puedes dejar las opciones por defecto)
   - Asegúrate de seleccionar "Git from the command line and also from 3rd-party software"

3. **Verificar:**
   ```powershell
   git --version
   ```

## 🚀 Instalación del Proyecto

### Paso 1: Abrir Terminal en Windows

Tienes varias opciones:

**Opción A: PowerShell (Recomendado)**
- Presiona `Windows + X`
- Selecciona "Windows PowerShell" o "Terminal"
- O busca "PowerShell" en el menú de inicio

**Opción B: CMD (Símbolo del sistema)**
- Presiona `Windows + R`
- Escribe `cmd` y presiona Enter

**Opción C: Terminal de Windows 11**
- Presiona `Windows + X`
- Selecciona "Terminal"

### Paso 2: Navegar al Directorio del Proyecto

```powershell
# Ejemplo: Si el proyecto está en el Escritorio
cd "C:\Users\TuUsuario\Desktop\Sistemas\proyectoaulico"

# Ejemplo: Si el proyecto está en OneDrive
cd "C:\Users\TuUsuario\OneDrive\Escritorio\Sistema\sistemas python\proyectoaulico"

# O si está en otra ubicación
cd "ruta\completa\al\proyecto"
```

**💡 Tip:** 
- Puedes escribir `cd ` y luego arrastrar la carpeta del proyecto a la terminal para obtener la ruta automáticamente
- Si la ruta tiene espacios, siempre usa comillas dobles alrededor de la ruta

### Paso 3: Crear Entorno Virtual

```powershell
python -m venv venv
```

Si `python` no funciona, prueba:
```powershell
py -m venv venv
```

Esto creará una carpeta `venv` en tu proyecto.

### Paso 4: Activar el Entorno Virtual

**En PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Si obtienes un error de política de ejecución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**En CMD (Símbolo del sistema):**
```cmd
venv\Scripts\activate.bat
```

**Verificación:** Deberías ver `(venv)` al inicio de tu línea:
```
(venv) PS C:\Users\TuUsuario\Desktop\Sistemas\proyectoaulico>
```

### Paso 5: Instalar Dependencias

Con el entorno virtual activado:

**Para Python 3.13 (recomendado):**
```powershell
# Instalar numpy primero (compatible con Python 3.13)
pip install "numpy>=2.0.0"
# Luego instalar el resto
pip install -r requirements.txt
```

**Para Python 3.10 o 3.11:**
```powershell
pip install -r requirements.txt
```

**Si obtienes errores de permisos:**
```powershell
pip install --user -r requirements.txt
```

**Si obtienes errores al compilar numpy (Python 3.13):**
```powershell
# Instalar numpy precompilado primero
pip install "numpy>=2.0.0"
# Luego continuar con el resto
pip install -r requirements.txt
```

**Tiempo estimado:** 3-5 minutos dependiendo de tu conexión.

### Paso 6: Configurar Variables de Entorno

**Opción A: Usando PowerShell**
```powershell
Copy-Item .env.example .env
```

**Opción B: Usando CMD**
```cmd
copy .env.example .env
```

**Opción C: Manualmente**
- Copia el archivo `.env.example`
- Renómbralo a `.env`
- Ábrelo con el Bloc de notas y edita si es necesario

### Paso 7: Aplicar Migraciones de Base de Datos

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### Paso 8: Crear Datos Iniciales (Opcional pero Recomendado)

```powershell
python manage.py shell
```

Dentro del shell de Python:
```python
from tareas.models import Categoria

# Crear categorías de ingresos
Categoria.objects.get_or_create(nombre="Salario", defaults={'tipo': 'ingreso', 'icono': '💼', 'color': '#2ecc71'})
Categoria.objects.get_or_create(nombre="Freelance", defaults={'tipo': 'ingreso', 'icono': '💻', 'color': '#27ae60'})
Categoria.objects.get_or_create(nombre="Inversiones", defaults={'tipo': 'ingreso', 'icono': '📈', 'color': '#16a085'})

# Crear categorías de gastos
Categoria.objects.get_or_create(nombre="Alimentación", defaults={'tipo': 'gasto', 'icono': '🍔', 'color': '#e74c3c'})
Categoria.objects.get_or_create(nombre="Transporte", defaults={'tipo': 'gasto', 'icono': '🚗', 'color': '#3498db'})
Categoria.objects.get_or_create(nombre="Entretenimiento", defaults={'tipo': 'gasto', 'icono': '🎮', 'color': '#9b59b6'})
Categoria.objects.get_or_create(nombre="Educación", defaults={'tipo': 'gasto', 'icono': '📚', 'color': '#f39c12'})
Categoria.objects.get_or_create(nombre="Salud", defaults={'tipo': 'gasto', 'icono': '🏥', 'color': '#e67e22'})
Categoria.objects.get_or_create(nombre="Servicios", defaults={'tipo': 'gasto', 'icono': '💡', 'color': '#f1c40f'})

print("✅ Categorías creadas exitosamente!")
exit()
```

### Paso 9: Crear Superusuario (Opcional)

Para acceder al panel de administración:

```powershell
python manage.py createsuperuser
```

Sigue las instrucciones para crear un usuario administrador.

## 🏃 Ejecutar el Sistema

El sistema requiere **DOS ventanas de terminal** abiertas simultáneamente.

### Terminal 1: Servidor Django (Backend/API)

1. **Abre una nueva ventana de PowerShell o CMD**

2. **Navega al proyecto:**
   ```powershell
   # Ajusta la ruta según tu ubicación
   cd "C:\Users\TuUsuario\OneDrive\Escritorio\Sistema\sistemas python\proyectoaulico"
   # O si está en otra ubicación
   cd "ruta\completa\al\proyecto"
   ```

3. **Activa el entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   # O en CMD:
   venv\Scripts\activate.bat
   ```

4. **Inicia el servidor Django:**
   ```powershell
   python manage.py runserver
   ```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**✅ Verificación:** Abre tu navegador en `http://localhost:8000/api/`

### Terminal 2: Aplicación Streamlit (Frontend)

1. **Abre otra ventana de PowerShell o CMD**

2. **Navega al proyecto:**
   ```powershell
   # Ajusta la ruta según tu ubicación
   cd "C:\Users\TuUsuario\OneDrive\Escritorio\Sistema\sistemas python\proyectoaulico"
   # O si está en otra ubicación
   cd "ruta\completa\al\proyecto"
   ```

3. **Activa el entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Inicia Streamlit:**
   ```powershell
   streamlit run app_streamlit.py
   ```

**Salida esperada:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**✅ Verificación:** Abre tu navegador en `http://localhost:8501`

## 🌐 Acceder a la Aplicación

Una vez que ambos servidores estén corriendo:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Aplicación Principal** | http://localhost:8501 | Interfaz de usuario Streamlit |
| **API REST** | http://localhost:8000/api/ | Endpoints de la API |
| **Panel Admin Django** | http://localhost:8000/admin | Panel de administración |

## 📦 Resumen de Comandos para Windows

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
Copy-Item .env.example .env

# 5. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. En Terminal 1: Iniciar Django
python manage.py runserver

# 7. En Terminal 2: Iniciar Streamlit
streamlit run app_streamlit.py
```

## 🔧 Solución de Problemas Específicos de Windows

### Error: "python no se reconoce como comando"

**Solución 1:** Usar `py` en lugar de `python`
```powershell
py -m venv venv
py manage.py runserver
```

**Solución 2:** Agregar Python al PATH
1. Busca "Variables de entorno" en el menú de inicio
2. Click en "Variables de entorno"
3. En "Variables del sistema", selecciona "Path" y click en "Editar"
4. Agrega la ruta a Python (ej: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311`)
5. Reinicia la terminal

### Error: "No se puede cargar el archivo porque la ejecución de scripts está deshabilitada"

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar el entorno virtual nuevamente.

### Error: "pip no se reconoce como comando"

**Solución:**
```powershell
python -m pip install -r requirements.txt
# O
py -m pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Solución:**
1. Cierra la ventana de terminal que tiene Django corriendo
2. O cambia el puerto:
   ```powershell
   python manage.py runserver 8001
   ```
3. Actualiza `API_BASE_URL` en `app_streamlit.py` a `http://localhost:8001`

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución:**
1. Verifica que el entorno virtual esté activado (deberías ver `(venv)`)
2. Si no está activado:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

### Error al instalar numpy o pandas (especialmente en Python 3.13)

**Problema:** numpy 1.26.4 no tiene wheels precompilados para Python 3.13 y falla al compilar.

**Solución:**
```powershell
# Instalar numpy 2.0+ primero (tiene soporte para Python 3.13)
pip install "numpy>=2.0.0"
# Luego instalar el resto de dependencias
pip install -r requirements.txt
```

**Si aún tienes problemas:**
```powershell
pip install --upgrade pip
pip install "numpy>=2.0.0" --no-cache-dir
pip install -r requirements.txt
```

**Nota:** El `requirements.txt` ya incluye `numpy>=2.0.0` y `streamlit>=1.39.0` para compatibilidad con Python 3.13.

### Problemas con rutas con espacios

Si tu proyecto está en una ruta con espacios (ej: `C:\Users\Mi Usuario\...`):

**Solución:** Usa comillas:
```powershell
cd "C:\Users\Mi Usuario\Desktop\Sistemas\proyectoaulico"
```

### Error: "Permission denied" al crear archivos

**Solución:**
1. Ejecuta PowerShell como Administrador
2. O cambia los permisos de la carpeta del proyecto
3. O mueve el proyecto a una ubicación sin restricciones (ej: `C:\proyectos\`)

## 💡 Consejos para Windows

### 1. Usar PowerShell en lugar de CMD
PowerShell es más moderno y tiene mejor soporte para scripts.

### 2. Usar Terminal de Windows 11
Si tienes Windows 11, usa la Terminal de Windows que soporta múltiples pestañas.

### 3. Crear Accesos Directos
Puedes crear scripts `.bat` o `.ps1` para iniciar los servidores:

**iniciar_django.bat:**
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python manage.py runserver
pause
```

**iniciar_streamlit.bat:**
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
streamlit run app_streamlit.py
pause
```

### 4. Usar Visual Studio Code
VS Code tiene excelente soporte para Python y terminales integradas:
- Descarga: https://code.visualstudio.com/
- Extensión recomendada: Python (de Microsoft)

## ✅ Checklist de Instalación para Windows

- [ ] Python 3.8+ instalado con "Add to PATH" marcado
- [ ] pip funcionando (`pip --version`)
- [ ] Entorno virtual creado (`python -m venv venv`)
- [ ] Entorno virtual activado (ves `(venv)` en la terminal)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Datos iniciales creados (categorías)
- [ ] Django corriendo en puerto 8000
- [ ] Streamlit corriendo en puerto 8501
- [ ] Aplicación accesible en http://localhost:8501

## 🎯 Comandos Rápidos de Referencia

| Acción | Comando |
|--------|---------|
| Activar entorno virtual | `.\venv\Scripts\Activate.ps1` |
| Desactivar entorno virtual | `deactivate` |
| Instalar dependencias | `pip install -r requirements.txt` |
| Iniciar Django | `python manage.py runserver` |
| Iniciar Streamlit | `streamlit run app_streamlit.py` |
| Verificar Python | `python --version` |
| Verificar pip | `pip --version` |

## 📚 Recursos Adicionales

- **Documentación Python para Windows**: https://docs.python.org/3/using/windows.html
- **PowerShell Documentation**: https://docs.microsoft.com/powershell/
- **Guía general de instalación**: Ver `INSTALACION.md`
- **Guía rápida**: Ver `INSTALACION_RAPIDA.md`

## 🆘 Obtener Ayuda

Si encuentras problemas:

1. Revisa la sección "Solución de Problemas Específicos de Windows"
2. Verifica que cumplas todos los requisitos
3. Asegúrate de seguir los pasos en orden
4. Verifica los logs de error para más detalles
5. Consulta `INSTALACION.md` para problemas generales

---

**¡Listo!** Una vez completados todos los pasos, tu sistema de educación financiera estará funcionando en Windows. 🎉

