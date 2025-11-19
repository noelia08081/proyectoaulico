"""
Aplicación Streamlit para Educación Financiera
Prototipo de aplicación como apoyo a la educación financiera de adultos jóvenes paraguayos (2024-2025)
Consume la API REST de Django
"""
import streamlit as st
import requests
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from decimal import Decimal

# Configuración
API_BASE_URL = "http://localhost:8000/api"

# Configurar página
st.set_page_config(
    page_title="Educación Financiera - Paraguay",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066CC;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #0066CC, #00A8E8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 0.5rem 0;
    }
    .educativo-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f7ff;
        border-left: 4px solid #0066CC;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Funciones de API
def api_get(endpoint, params=None):
    """Realiza una petición GET a la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}/", params=params or {})
        response.raise_for_status()
        data = response.json()
        # Manejar respuestas paginadas de Django REST Framework
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {str(e)}")
        return None


def api_post(endpoint, data):
    """Realiza una petición POST a la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None


def api_patch(endpoint, item_id, data):
    """Realiza una petición PATCH a la API"""
    try:
        response = requests.patch(f"{API_BASE_URL}/{endpoint}/{item_id}/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None


def api_delete(endpoint, item_id):
    """Realiza una petición DELETE a la API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}/{item_id}/")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")
        return False


def formatear_moneda(monto):
    """Formatea un monto como moneda paraguaya (Guaraníes)"""
    return f"₲ {monto:,.0f}".replace(",", ".")


def main():
    # Header
    st.markdown('<div class="main-header">💵 Educación Financiera</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Prototipo de aplicación para adultos jóvenes paraguayos (2024-2025)</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navegación")
        pagina = st.radio(
            "Selecciona una sección:",
            ["🏠 Dashboard", "💰 Transacciones", "📊 Presupuestos", "🎯 Metas", "📚 Aprender", "📈 Análisis"],
            key="pagina_principal"
        )
        
        st.divider()
        st.caption("💡 Esta aplicación es un prototipo para validación de usabilidad y análisis de datos")
    
    # Contenido según la página seleccionada
    if pagina == "🏠 Dashboard":
        mostrar_dashboard()
    elif pagina == "💰 Transacciones":
        mostrar_transacciones()
    elif pagina == "📊 Presupuestos":
        mostrar_presupuestos()
    elif pagina == "🎯 Metas":
        mostrar_metas()
    elif pagina == "📚 Aprender":
        mostrar_lecciones()
    elif pagina == "📈 Análisis":
        mostrar_analisis()


def mostrar_dashboard():
    """Muestra el dashboard principal con resumen financiero"""
    st.header("🏠 Dashboard Financiero")
    
    # Obtener datos del dashboard
    datos = api_get("analisis/dashboard")
    
    if not datos:
        st.warning("⚠️ No se pudo conectar con la API. Asegúrate de que Django esté corriendo.")
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Ingresos del Mes",
            formatear_moneda(datos['mes_actual']['ingresos']),
            delta=None
        )
    
    with col2:
        st.metric(
            "Gastos del Mes",
            formatear_moneda(datos['mes_actual']['gastos']),
            delta=f"-{formatear_moneda(datos['mes_actual']['gastos'])}"
        )
    
    with col3:
        balance = datos['mes_actual']['balance']
        st.metric(
            "Balance",
            formatear_moneda(balance),
            delta=f"{'+' if balance >= 0 else ''}{formatear_moneda(balance)}"
        )
    
    with col4:
        st.metric(
            "Metas Activas",
            datos['metas']['total_metas'],
            delta=f"{formatear_moneda(datos['metas']['monto_total_ahorrado'])} ahorrado"
        )
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Resumen Mensual")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Ingresos',
            x=['Ingresos', 'Gastos'],
            y=[datos['mes_actual']['ingresos'], datos['mes_actual']['gastos']],
            marker_color=['#2ecc71', '#e74c3c']
        ))
        fig.update_layout(
            title="Ingresos vs Gastos",
            yaxis_title="Monto (₲)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Progreso de Metas")
        if datos['metas']['total_metas'] > 0:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=datos['metas']['porcentaje_promedio'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Progreso Promedio (%)"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 100], 'color': "gray"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                     'thickness': 0.75, 'value': 90}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay metas activas")
    
    # Presupuesto
    st.subheader("📊 Estado de Presupuestos")
    presupuesto_usado = datos['mes_actual']['presupuesto_usado']
    presupuesto_total = datos['mes_actual']['presupuesto_total']
    
    if presupuesto_total > 0:
        porcentaje = (presupuesto_usado / presupuesto_total) * 100
        st.progress(porcentaje / 100)
        col1, col2, col3 = st.columns(3)
        col1.metric("Presupuesto Total", formatear_moneda(presupuesto_total))
        col2.metric("Gastado", formatear_moneda(presupuesto_usado))
        col3.metric("Restante", formatear_moneda(datos['mes_actual']['presupuesto_restante']))
    else:
        st.info("No hay presupuestos configurados para este mes")
    
    # Categorías más usadas
    if datos.get('categorias_mas_usadas'):
        st.subheader("🏷️ Categorías Más Utilizadas")
        df_categorias = pd.DataFrame(datos['categorias_mas_usadas'])
        st.dataframe(df_categorias, use_container_width=True, hide_index=True)


def mostrar_transacciones():
    """Muestra la gestión de transacciones"""
    st.header("💰 Gestión de Transacciones")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_filtro = st.selectbox("Tipo", ["Todos", "Ingreso", "Gasto"], key="filtro_tipo")
    with col2:
        categorias = api_get("categorias")
        if categorias and isinstance(categorias, list) and len(categorias) > 0:
            categoria_opciones = ["Todas"] + [c.get('nombre', '') for c in categorias if isinstance(c, dict)]
            categoria_filtro = st.selectbox("Categoría", categoria_opciones, key="filtro_categoria")
        else:
            categoria_filtro = "Todas"
            categorias = []  # Asegurar que categorias sea una lista vacía
    with col3:
        fecha_filtro = st.date_input("Fecha", value=date.today(), key="filtro_fecha")
    
    # Obtener transacciones
    params = {}
    if tipo_filtro != "Todos":
        params['tipo'] = tipo_filtro.lower()
    if categoria_filtro != "Todas" and categorias:
        categoria_id = next((c.get('id') for c in categorias if isinstance(c, dict) and c.get('nombre') == categoria_filtro), None)
        if categoria_id:
            params['categoria'] = categoria_id
    
    transacciones = api_get("transacciones", params)
    
    # Formulario para nueva transacción
    with st.expander("➕ Agregar Nueva Transacción", expanded=False):
        with st.form("nueva_transaccion"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_tipo = st.selectbox("Tipo", ["ingreso", "gasto"], key="nuevo_tipo")
                nuevo_monto = st.number_input("Monto (₲)", min_value=0.0, step=1000.0, key="nuevo_monto")
            with col2:
                nueva_fecha = st.date_input("Fecha", value=date.today(), key="nueva_fecha")
                # Obtener categorías filtradas por tipo
                if not categorias:
                    categorias = api_get("categorias") or []
                categorias_filtradas = [c for c in categorias if isinstance(c, dict) and c.get('tipo') == nuevo_tipo]
                nueva_categoria_id = st.selectbox(
                    "Categoría",
                    options=[None] + [c.get('id') for c in categorias_filtradas if c.get('id')],
                    format_func=lambda x: next((c.get('nombre', 'Sin nombre') for c in categorias_filtradas if c.get('id') == x), "Sin categoría") if x else "Sin categoría",
                    key="nueva_categoria"
                )
            
            nueva_descripcion = st.text_input("Descripción", key="nueva_descripcion")
            nuevas_notas = st.text_area("Notas (opcional)", key="nuevas_notas")
            
            if st.form_submit_button("💾 Guardar Transacción", type="primary"):
                if nueva_descripcion and nuevo_monto > 0:
                    data = {
                        'descripcion': nueva_descripcion,
                        'monto': float(nuevo_monto),
                        'tipo': nuevo_tipo,
                        'fecha': nueva_fecha.isoformat(),
                        'notas': nuevas_notas
                    }
                    if nueva_categoria_id:
                        data['categoria'] = nueva_categoria_id
                    
                    resultado = api_post("transacciones", data)
                    if resultado:
                        st.success("✅ Transacción creada exitosamente!")
                        st.rerun()
                else:
                    st.warning("⚠️ Completa todos los campos obligatorios")
    
    # Lista de transacciones
    if transacciones:
        st.subheader(f"📋 Transacciones ({len(transacciones)} encontradas)")
        
        # Resumen
        ingresos = sum(t['monto'] for t in transacciones if t['tipo'] == 'ingreso')
        gastos = sum(t['monto'] for t in transacciones if t['tipo'] == 'gasto')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", formatear_moneda(ingresos))
        col2.metric("Total Gastos", formatear_moneda(gastos))
        col3.metric("Balance", formatear_moneda(ingresos - gastos))
        
        # Tabla de transacciones
        df = pd.DataFrame(transacciones)
        if not df.empty:
            df['monto_formateado'] = df['monto'].apply(formatear_moneda)
            df['fecha_formateada'] = pd.to_datetime(df['fecha']).dt.strftime('%d/%m/%Y')
            df_display = df[['fecha_formateada', 'descripcion', 'tipo', 'categoria_nombre', 'monto_formateado']].copy()
            df_display.columns = ['Fecha', 'Descripción', 'Tipo', 'Categoría', 'Monto']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Gráfico de transacciones
            st.subheader("📊 Visualización de Transacciones")
            fig = px.bar(
                df,
                x='fecha',
                y='monto',
                color='tipo',
                title="Transacciones por Fecha",
                labels={'monto': 'Monto (₲)', 'fecha': 'Fecha', 'tipo': 'Tipo'},
                color_discrete_map={'ingreso': '#2ecc71', 'gasto': '#e74c3c'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No hay transacciones registradas. ¡Agrega tu primera transacción!")


def mostrar_presupuestos():
    """Muestra la gestión de presupuestos"""
    st.header("📊 Gestión de Presupuestos")
    
    # Obtener presupuestos
    ahora = datetime.now()
    mes_actual = ahora.month
    año_actual = ahora.year
    
    col1, col2 = st.columns(2)
    with col1:
        mes_seleccionado = st.selectbox("Mes", list(range(1, 13)), index=mes_actual-1, key="mes_presupuesto")
    with col2:
        año_seleccionado = st.number_input("Año", min_value=2020, max_value=2030, value=año_actual, key="año_presupuesto")
    
    presupuestos = api_get("presupuestos", {'mes': mes_seleccionado, 'año': año_seleccionado})
    
    # Formulario para nuevo presupuesto
    with st.expander("➕ Crear Nuevo Presupuesto", expanded=False):
        with st.form("nuevo_presupuesto"):
            categorias_gastos = api_get("categorias", {'tipo': 'gasto'}) or []
            if not isinstance(categorias_gastos, list):
                categorias_gastos = []
            nuevo_nombre = st.text_input("Nombre del Presupuesto", key="nuevo_nombre_presupuesto")
            nueva_categoria = st.selectbox(
                "Categoría",
                options=[c.get('id') for c in categorias_gastos if isinstance(c, dict) and c.get('id')],
                format_func=lambda x: next((c.get('nombre', '') for c in categorias_gastos if isinstance(c, dict) and c.get('id') == x), ""),
                key="nueva_categoria_presupuesto"
            ) if categorias_gastos and len(categorias_gastos) > 0 else None
            nuevo_limite = st.number_input("Monto Límite (₲)", min_value=0.0, step=10000.0, key="nuevo_limite")
            
            if st.form_submit_button("💾 Crear Presupuesto", type="primary"):
                if nuevo_nombre and nueva_categoria and nuevo_limite > 0:
                    data = {
                        'nombre': nuevo_nombre,
                        'categoria': nueva_categoria,
                        'monto_limite': float(nuevo_limite),
                        'mes': mes_seleccionado,
                        'año': año_seleccionado
                    }
                    resultado = api_post("presupuestos", data)
                    if resultado:
                        st.success("✅ Presupuesto creado exitosamente!")
                        st.rerun()
    
    # Mostrar presupuestos
    if presupuestos:
        st.subheader(f"📊 Presupuestos para {mes_seleccionado}/{año_seleccionado}")
        
        for presupuesto in presupuestos:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{presupuesto['nombre']}** - {presupuesto['categoria_nombre']}")
                with col2:
                    st.metric("Límite", formatear_moneda(presupuesto['monto_limite']))
                with col3:
                    st.metric("Gastado", formatear_moneda(presupuesto['gasto_actual']))
                with col4:
                    st.metric("Restante", formatear_moneda(presupuesto['monto_restante']))
                
                porcentaje = presupuesto['porcentaje_usado']
                color = "green" if porcentaje < 80 else "orange" if porcentaje < 100 else "red"
                st.progress(porcentaje / 100)
                st.caption(f"{porcentaje:.1f}% del presupuesto usado")
                st.divider()
    else:
        st.info("📝 No hay presupuestos configurados para este mes. ¡Crea uno nuevo!")


def mostrar_metas():
    """Muestra la gestión de metas financieras"""
    st.header("🎯 Metas Financieras")
    
    metas = api_get("metas")
    
    # Formulario para nueva meta
    with st.expander("➕ Crear Nueva Meta", expanded=False):
        with st.form("nueva_meta"):
            nuevo_titulo = st.text_input("Título de la Meta", key="nuevo_titulo_meta")
            nueva_descripcion = st.text_area("Descripción", key="nueva_descripcion_meta")
            col1, col2 = st.columns(2)
            with col1:
                nuevo_monto = st.number_input("Monto Objetivo (₲)", min_value=0.0, step=100000.0, key="nuevo_monto_meta")
            with col2:
                nueva_fecha = st.date_input("Fecha Objetivo", key="nueva_fecha_meta")
            
            if st.form_submit_button("💾 Crear Meta", type="primary"):
                if nuevo_titulo and nuevo_monto > 0:
                    data = {
                        'titulo': nuevo_titulo,
                        'descripcion': nueva_descripcion,
                        'monto_objetivo': float(nuevo_monto),
                        'fecha_objetivo': nueva_fecha.isoformat(),
                        'estado': 'en_progreso'
                    }
                    resultado = api_post("metas", data)
                    if resultado:
                        st.success("✅ Meta creada exitosamente!")
                        st.rerun()
    
    # Mostrar metas
    if metas:
        st.subheader(f"🎯 Mis Metas ({len(metas)} activas)")
        
        for meta in metas:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    estado_emoji = "✅" if meta['estado'] == 'completada' else "🔄" if meta['estado'] == 'en_progreso' else "❌"
                    st.write(f"### {estado_emoji} {meta['titulo']}")
                    if meta['descripcion']:
                        st.write(meta['descripcion'])
                    
                    porcentaje = meta['porcentaje_completado']
                    st.progress(porcentaje / 100)
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Objetivo", formatear_moneda(meta['monto_objetivo']))
                    col_b.metric("Ahorrado", formatear_moneda(meta['monto_actual']))
                    col_c.metric("Restante", formatear_moneda(meta['monto_restante']))
                    col_d.metric("Progreso", f"{porcentaje:.1f}%")
                    
                    if meta['dias_restantes'] is not None:
                        st.caption(f"⏰ {meta['dias_restantes']} días restantes")
                
                with col2:
                    if meta['estado'] == 'en_progreso':
                        monto_agregar = st.number_input(
                            "Agregar (₲)",
                            min_value=0.0,
                            step=10000.0,
                            key=f"agregar_{meta['id']}"
                        )
                        if st.button("➕ Agregar", key=f"btn_agregar_{meta['id']}"):
                            data = {'monto': float(monto_agregar)}
                            resultado = api_post(f"metas/{meta['id']}/agregar_monto", data)
                            if resultado:
                                st.success("✅ Monto agregado!")
                                st.rerun()
                
                st.divider()
    else:
        st.info("📝 No hay metas financieras. ¡Crea tu primera meta!")


def mostrar_lecciones():
    """Muestra las lecciones educativas"""
    st.header("📚 Aprende sobre Finanzas Personales")
    
    st.markdown("""
    <div class="educativo-box">
    <h3>💡 Educación Financiera para Jóvenes Paraguayos</h3>
    <p>Aquí encontrarás lecciones y consejos prácticos para mejorar tu salud financiera.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtro por nivel
    nivel_filtro = st.selectbox("Nivel", ["Todos", "Básico", "Intermedio", "Avanzado"], key="filtro_nivel")
    
    params = {}
    if nivel_filtro != "Todos":
        params['nivel'] = nivel_filtro.lower()
    
    lecciones = api_get("lecciones", params)
    
    if lecciones:
        for leccion in lecciones:
            with st.expander(f"📖 {leccion['titulo']} - {leccion['nivel'].title()} ({leccion['duracion_minutos']} min)"):
                st.markdown(leccion['contenido'])
                st.caption(f"⏱️ Duración estimada: {leccion['duracion_minutos']} minutos")
    else:
        st.info("📝 No hay lecciones disponibles. Las lecciones se pueden agregar desde el panel de administración de Django.")
        
        # Contenido educativo básico
        st.markdown("""
        ### 💰 Conceptos Básicos de Finanzas Personales
        
        #### 1. Presupuesto Personal
        Un presupuesto es un plan que te ayuda a controlar tus ingresos y gastos. 
        Te permite saber cuánto dinero tienes y cómo lo estás gastando.
        
        #### 2. Ahorro
        El ahorro es la parte de tus ingresos que no gastas. Es importante ahorrar 
        para emergencias y para alcanzar tus metas financieras.
        
        #### 3. Metas Financieras
        Establecer metas financieras te ayuda a mantener el enfoque y la motivación 
        para ahorrar y gestionar mejor tu dinero.
        
        #### 4. Categorización de Gastos
        Clasificar tus gastos por categorías te ayuda a identificar en qué estás 
        gastando más dinero y dónde puedes reducir gastos.
        """)


def mostrar_analisis():
    """Muestra análisis detallados de datos financieros"""
    st.header("📈 Análisis Financiero")
    
    # Resumen mensual
    ahora = datetime.now()
    st.subheader("📊 Resumen Mensual")
    
    col1, col2 = st.columns(2)
    with col1:
        mes_analisis = st.selectbox("Mes", list(range(1, 13)), index=ahora.month-1, key="mes_analisis")
    with col2:
        año_analisis = st.number_input("Año", min_value=2020, max_value=2030, value=ahora.year, key="año_analisis")
    
    resumen = api_get("transacciones/resumen_mensual", {'mes': mes_analisis, 'año': año_analisis})
    
    if resumen:
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos", formatear_moneda(resumen['ingresos']))
        col2.metric("Gastos", formatear_moneda(resumen['gastos']))
        col3.metric("Balance", formatear_moneda(resumen['balance']))
        
        # Gráfico de gastos por categoría
        if resumen.get('gastos_por_categoria'):
            st.subheader("📊 Gastos por Categoría")
            df_gastos = pd.DataFrame(resumen['gastos_por_categoria'])
            fig = px.pie(
                df_gastos,
                values='total',
                names='categoria__nombre',
                title="Distribución de Gastos por Categoría"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tendencias
    st.subheader("📈 Tendencias de los Últimos Meses")
    meses_tendencia = st.slider("Meses a analizar", 3, 12, 6, key="meses_tendencia")
    tendencias = api_get("transacciones/tendencias", {'meses': meses_tendencia})
    
    if tendencias:
        df_tendencias = pd.DataFrame(tendencias)
        df_tendencias['periodo'] = df_tendencias.apply(
            lambda x: f"{int(x['mes'])}/{int(x['año'])}", axis=1
        )
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_tendencias['periodo'],
            y=df_tendencias['ingresos'],
            name='Ingresos',
            line=dict(color='#2ecc71', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_tendencias['periodo'],
            y=df_tendencias['gastos'],
            name='Gastos',
            line=dict(color='#e74c3c', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_tendencias['periodo'],
            y=df_tendencias['balance'],
            name='Balance',
            line=dict(color='#3498db', width=3, dash='dash')
        ))
        fig.update_layout(
            title="Tendencias Financieras",
            xaxis_title="Período",
            yaxis_title="Monto (₲)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
