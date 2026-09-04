from datetime import datetime
import os
from fpdf import FPDF
import pandas as pd
import streamlit as st
import time

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Asistencia e Incidencias - UEB",
    page_icon="🏫",
    layout="wide",
)

# --- ESTILOS CSS PROFESIONALES (ESTILO INSTITUCIONAL UEB) ---
st.markdown(
    """
    <style>
    /* Fondo general azul marino corporativo */
    .stApp {
        background: linear-gradient(135deg, #071328 0%, #0B1D3A 100%);
        color: #f1f5f9;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Tarjeta principal unificada */
    .login-box {
        background: #0B1D3A;
        border: 2px solid rgba(245, 158, 11, 0.35);
        border-radius: 20px;
        padding: 25px 45px 35px 45px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        max-width: 480px;
        margin: 10px auto;
        text-align: center;
    }

    /* Estilo del título y subtítulo dentro de la tarjeta */
    .login-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 5px;
        margin-bottom: 2px;
    }
    .login-subtitle {
        color: #94a3b8;
        font-size: 10px;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Etiquetas de campo */
    .field-label {
        text-align: left;
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 15px;
        margin-bottom: 5px;
        display: block;
    }

    /* Personalización del botón de entrada (Dorado/Naranja elegante) */
    div.stButton > button {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3) !important;
        margin-top: 15px !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #d97706 100%, #b45309 100%) !important;
    }

    /* Pie de tarjeta con iconos */
    .card-footer {
        display: flex;
        justify-content: space-between;
        margin-top: 25px;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 11px;
        color: #94a3b8;
    }
    .footer-item {
        text-align: center;
        flex: 1;
    }
    .footer-title {
        color: #f8fafc;
        font-weight: bold;
        display: block;
        font-size: 11px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 1. SISTEMA DE CREDENCIALES DINÁMICAS (CÉDULA Y CONTRASEÑA) ---
if "usuario_sistema" not in st.session_state:
    st.session_state.usuario_sistema = "1234567890"  # Número de cédula por defecto

if "password_sistema" not in st.session_state:
    st.session_state.password_sistema = "asistencia2026"  # Contraseña inicial por defecto

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown(
            """
            <div class="login-box">
            """,
            unsafe_allow_html=True,
        )

        # Mostrar el logo local perfectamente centrado dentro de la tarjeta
        if os.path.exists("logo_ueb.png"):
            col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
            with col_img2:
                st.image("logo_ueb.png", width=90)

        st.markdown(
            """
                <div style="text-align: center; margin-top: 5px;">
                    <div class="login-title">LOGIN - UEB</div>
                    <div class="login-subtitle">ACCESO AL SISTEMA ACADÉMICO</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<span class="field-label">🆔 &nbsp; NÚMERO DE CÉDULA</span>',
            unsafe_allow_html=True,
        )
        usuario_ingresado = st.text_input(
            "Cédula",
            placeholder="Ingrese su número de cédula...",
            key="user_input",
            label_visibility="collapsed",
        )

        st.markdown(
            '<span class="field-label">🔒 &nbsp; PASSWORD</span>',
            unsafe_allow_html=True,
        )
        password_ingresada = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingrese contraseña...",
            key="pwd_input",
            label_visibility="collapsed",
        )

        if st.button("➔ &nbsp; ENTRAR", use_container_width=True):
            if (
                usuario_ingresado == st.session_state.usuario_sistema
                and password_ingresada == st.session_state.password_sistema
            ):
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⚠️ Cédula o contraseña incorrectas. Verifique los datos.")

        st.markdown(
            """
                <div class="card-footer">
                    <div class="footer-item">
                        <span class="footer-title">🛡️ SEGURO</span>
                        <span>Datos protegidos</span>
                    </div>
                    <div class="footer-item">
                        <span class="footer-title">🎓 CONFIABLE</span>
                        <span>Sistema académico UEB</span>
                    </div>
                    <div class="footer-item">
                        <span class="footer-title">🕒 24/7</span>
                        <span>Disponible siempre</span>
                    </div>
                </div>
            </div>
            <div style="text-align: center; color: #64748b; font-size: 11px; margin-top: 15px; letter-spacing: 0.5px;">
                🔒 &nbsp; SISTEMA ACADÉMICO UEB<br>Unidad Educativa Babahoyo
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.stop()

# --- 2. BARRA DE CARGA INICIAL ---
if "cargado" not in st.session_state:
    with st.spinner("⚡ Conectando con los servidores de la institución..."):
        barra_progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            barra_progreso.progress(i + 1)
        time.sleep(0.2)
    st.session_state.cargado = True
    st.rerun()

# Inicializar base de datos general en memoria (Session State)
if "historial_df" not in st.session_state:
    st.session_state.historial_df = pd.DataFrame(
        columns=[
            "Fecha",
            "Curso",
            "Estudiante",
            "Estado / Asistencia",
            "Observación / Detalle",
        ]
    )

st.title("🏫 Sistema de Control de Asistencia y Novedades")
st.markdown("Gestión académica, control diario, histórico y reportes en PDF.")

# Cargar archivo Excel por pestañas
archivo_excel = "estudiantes.xlsx"
excel_file = None

if os.path.exists(archivo_excel):
    try:
        excel_file = pd.ExcelFile(archivo_excel)
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo Excel: {e}")

# --- PANEL LATERAL: CONFIGURACIÓN Y DATOS DEL DOCENTE ---
with st.sidebar:
    if os.path.exists("logo_ueb.png"):
        st.image("logo_ueb.png", width=120)

    st.header("⚙️ Configuración del Docente")

    docente_nombre = st.text_input(
        "Nombre del Docente", value="Lic. Mauricio Menéndez Real"
    )
    asignatura = st.text_input(
        "Asignatura / Área", value="DISEÑO Y DESARROLLO WEB"
    )
    institucion = st.text_input(
        "Institución Educativa", value="Unidad Educativa Babahoyo"
    )

    st.markdown("---")
    st.subheader("🔑 Seguridad y Cuenta")
    
    # Campo para configurar el número de cédula del docente directamente desde la sesión
    nueva_cedula = st.text_input("Número de Cédula", value=st.session_state.usuario_sistema)
    if nueva_cedula != st.session_state.usuario_sistema:
        st.session_state.usuario_sistema = nueva_cedula

    with st.expander("Cambiar Contraseña"):
        pass_actual = st.text_input("Contraseña Actual", type="password", key="p_act")
        nuevo_pass = st.text_input("Nueva Contraseña", type="password", key="p_nue")
        if st.button("Actualizar Clave"):
            if pass_actual == st.session_state.password_sistema:
                if nuevo_pass:
                    st.session_state.password_sistema = nuevo_pass
                    st.success("¡Contraseña actualizada con éxito! Ahora debe usar esta nueva clave.")
                else:
                    st.warning("La nueva contraseña no puede estar vacía.")
            else:
                st.error("⚠️ La contraseña actual no es correcta.")

    st.markdown("---")
    st.header("📅 Selección de Fecha y Curso")

    fecha_pase = st.date_input("Fecha de Registro / Consulta", datetime.now())
    fecha_str = fecha_pase.strftime("%Y-%m-%d")

    uploaded_file = st.file_uploader(
        "Subir tu archivo 'estudiantes.xlsx'", type=["xlsx"]
    )
    if uploaded_file is not None:
        excel_file = pd.ExcelFile(uploaded_file)

    if excel_file is not None:
        cursos_disponibles = excel_file.sheet_names
        curso_seleccionado = st.selectbox(
            "Seleccionar Curso", cursos_disponibles
        )
    else:
        curso_seleccionado = None
        st.warning("⚠️ Coloca el archivo 'estudiantes.xlsx' en tu carpeta.")

# --- PANEL PRINCIPAL: TOMA Y EDICIÓN DE ASISTENCIA ---
if excel_file is not None and curso_seleccionado:
    st.subheader(
        f"📋 Pase de Lista: {curso_seleccionado} | Fecha: {fecha_str}"
    )

    df_curso = pd.read_excel(excel_file, sheet_name=curso_seleccionado)
    df_curso.columns = df_curso.columns.str.strip()

    col_nombre = None
    for col in df_curso.columns:
        if "NOMBRE" in col.upper() or "APELLIDO" in col.upper():
            col_nombre = col
            break

    if not col_nombre and len(df_curso.columns) > 2:
        col_nombre = df_curso.columns[2]

    if col_nombre:
        lista_estudiantes = sorted(df_curso[col_nombre].dropna().tolist())

        df_existente = pd.DataFrame()
        if not st.session_state.historial_df.empty:
            df_existente = st.session_state.historial_df[
                (st.session_state.historial_df["Fecha"] == fecha_str)
                & (st.session_state.historial_df["Curso"] == curso_seleccionado)
            ]

        st.info(
            "💡 **Modo Edición Activo:** Si ya pasaste lista este día, los datos"
            " cargados reflejarán lo guardado. Puedes cambiar cualquier estado y"
            " volver a guardar para actualizar."
        )

        with st.form(f"form_asistencia_{curso_seleccionado}_{fecha_str}"):
            registros_dia = []

            cols_header = st.columns([3.5, 3, 4])
            cols_header[0].markdown("**Estudiante**")
            cols_header[1].markdown("**Estado / Novedad**")
            cols_header[2].markdown("**Observación / Minutos / Motivo**")

            estados_opciones = [
                "Presente",
                "Atraso",
                "Falta Injustificada",
                "Falta Justificada",
                "Permiso",
                "Fuga",
            ]

            for idx, estudiante in enumerate(lista_estudiantes):
                c1, c2, c3 = st.columns([3.5, 3, 4])

                estado_previo = "Presente"
                obs_previo = ""
                if not df_existente.empty:
                    match_est = df_existente[
                        df_existente["Estudiante"] == estudiante
                    ]
                    if not match_est.empty:
                        estado_previo = match_est.iloc[0]["Estado / Asistencia"]
                        obs_previo = match_est.iloc[0]["Observación / Detalle"]
                        if obs_previo == "-":
                            obs_previo = ""

                idx_estado = (
                    estados_opciones.index(estado_previo)
                    if estado_previo in estados_opciones
                    else 0
                )

                with c1:
                    st.write(f"{idx + 1}. {estudiante}")

                with c2:
                    estado = st.selectbox(
                        "Estado",
                        estados_opciones,
                        index=idx_estado,
                        key=f"estado_{idx}_{fecha_str}",
                        label_visibility="collapsed",
                    )

                with c3:
                    obs = st.text_input(
                        "Obs",
                        value=obs_previo,
                        placeholder=(
                            "Ej. 10 min de atraso"
                            if estado == "Atraso"
                            else "Escribe detalles..."
                        ),
                        key=f"obs_{idx}_{fecha_str}",
                        label_visibility="collapsed",
                    )

                registros_dia.append({
                    "Fecha": fecha_str,
                    "Curso": curso_seleccionado,
                    "Estudiante": estudiante,
                    "Estado / Asistencia": estado,
                    "Observación / Detalle": (
                        obs
                        if obs
                        else ("-" if estado == "Presente" else estado)
                    ),
                })

            st.markdown("---")
            guardar_btn = st.form_submit_button(
                "💾 Guardar / Actualizar Asistencia de este Curso",
                use_container_width=True,
            )

            if guardar_btn:
                nuevo_df = pd.DataFrame(registros_dia)

                if not st.session_state.historial_df.empty:
                    st.session_state.historial_df = st.session_state.historial_df[
                        ~(
                            (
                                st.session_state.historial_df["Fecha"]
                                == fecha_str
                            )
                            & (
                                st.session_state.historial_df["Curso"]
                                == curso_seleccionado
                            )
                        )
                    ]

                st.session_state.historial_df = pd.concat(
                    [st.session_state.historial_df, nuevo_df], ignore_index=True
                )
                st.success(
                    f"¡Asistencia de {curso_seleccionado} para el día"
                    f" {fecha_str} guardada / actualizada con éxito!"
                )
    else:
        st.error("No se encontró la columna de nombres de los estudiantes.")
else:
    st.warning("Selecciona un curso y asegúrate de tener tu archivo Excel.")

# --- SECCIÓN DE REPORTES Y DESCARGA EN PDF ---
st.markdown("---")
st.subheader("📊 Historial General, Filtros y Reportes Oficiales en PDF")

df_historial = st.session_state.historial_df

if df_historial.empty:
    st.info(
        "Aún no hay registros guardados en el sistema para generar reportes."
    )
else:
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_curso = st.selectbox(
            "Filtrar Reporte por Curso",
            options=["Todos"] + list(df_historial["Curso"].unique()),
        )
    with col_f2:
        filtro_fecha = st.selectbox(
            "Filtrar por Fecha",
            options=["Todas las Fechas"] + list(df_historial["Fecha"].unique()),
        )
    with col_f3:
        filtro_estado = st.multiselect(
            "Filtrar por Estado",
            options=[
                "Presente",
                "Atraso",
                "Falta Injustificada",
                "Falta Justificada",
                "Permiso",
                "Fuga",
            ],
            default=[
                "Presente",
                "Atraso",
                "Falta Injustificada",
                "Falta Justificada",
                "Permiso",
                "Fuga",
            ],
        )

    df_filtrado = df_historial[
        df_historial["Estado / Asistencia"].isin(filtro_estado)
    ]
    if filtro_curso != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Curso"] == filtro_curso]
    if filtro_fecha != "Todas las Fechas":
        df_filtrado = df_filtrado[df_filtrado["Fecha"] == filtro_fecha]

    # Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Total Faltas",
        len(
            df_filtrado[
                df_filtrado["Estado / Asistencia"].str.contains("Falta")
            ]
        ),
    )
    m2.metric(
        "Total Atrasos",
        len(df_filtrado[df_filtrado["Estado / Asistencia"] == "Atraso"]),
    )
    m3.metric(
        "Total Permisos",
        len(df_filtrado[df_filtrado["Estado / Asistencia"] == "Permiso"]),
    )
    m4.metric(
        "Total Fugas",
        len(df_filtrado[df_filtrado["Estado / Asistencia"] == "Fuga"]),
    )

    st.dataframe(df_filtrado, use_container_width=True)

    # Botones de descarga
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        csv_data = df_filtrado.to_csv(index=False, encoding="utf-8-sig").encode(
            "utf-8-sig"
        )
        st.download_button(
            label="📥 Descargar Reporte en CSV (Excel)",
            data=csv_data,
            file_name=(
                f"reporte_asistencia_{datetime.now().strftime('%Y-%m-%d')}.csv"
            ),
            mime="text/csv",
        )

    with col_d2:
        if st.button("📄 Generar Archivo PDF Oficial"):

            class PDF(FPDF):

                def header(self):
                    if os.path.exists("logo_ueb.png"):
                        self.image("logo_ueb.png", 10, 8, 22)
                    
                    self.set_font("helvetica", "B", 14)
                    self.cell(
                        0,
                        8,
                        str(institucion),
                        new_x="LMARGIN",
                        new_y="NEXT",
                        align="C",
                    )
                    self.set_font("helvetica", "B", 11)
                    self.cell(
                        0,
                        6,
                        "REPORTE OFICIAL DE ASISTENCIA E INCIDENCIAS",
                        new_x="LMARGIN",
                        new_y="NEXT",
                        align="C",
                    )
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("helvetica", "I", 8)
                    self.cell(
                        0,
                        10,
                        f"Página {self.page_no()} - Generado el"
                        f" {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        align="C",
                    )

            pdf = PDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            pdf.set_font("helvetica", "B", 10)
            pdf.cell(
                0,
                6,
                f"Docente: {docente_nombre}    |    Asignatura: {asignatura}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.cell(
                0,
                6,
                f"Curso Filtrado: {filtro_curso}    |    Fecha de Emisión:"
                f" {datetime.now().strftime('%Y-%m-%d')}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.ln(5)

            pdf.set_font("helvetica", "B", 9)
            pdf.set_fill_color(44, 62, 80)
            pdf.set_text_color(255, 255, 255)

            col_widths = [22, 28, 65, 30, 45]
            headers = ["Fecha", "Curso", "Estudiante", "Estado", "Observación"]

            for i, h in enumerate(headers):
                pdf.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
            pdf.ln()

            pdf.set_font("helvetica", "", 8)
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(255, 255, 255)

            for _, row in df_filtrado.iterrows():
                pdf.cell(
                    col_widths[0],
                    6,
                    str(row["Fecha"]),
                    border=1,
                    align="C",
                )
                pdf.cell(
                    col_widths[1],
                    6,
                    str(row["Curso"]),
                    border=1,
                    align="C",
                )
                pdf.cell(
                    col_widths[2],
                    6,
                    str(row["Estudiante"]),
                    border=1,
                    align="L",
                )
                pdf.cell(
                    col_widths[3],
                    6,
                    str(row["Estado / Asistencia"]),
                    border=1,
                    align="C",
                )
                pdf.cell(
                    col_widths[4],
                    6,
                    str(row["Observación / Detalle"]),
                    border=1,
                    align="L",
                )
                pdf.ln()

            pdf.ln(20)
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(
                0,
                6,
                "__________________________________________",
                new_x="LMARGIN",
                new_y="NEXT",
                align="C",
            )
            pdf.cell(
                0,
                6,
                f"{docente_nombre}",
                new_x="LMARGIN",
                new_y="NEXT",
                align="C",
            )
            pdf.cell(
                0,
                4,
                "Docente / Tutor",
                new_x="LMARGIN",
                new_y="NEXT",
                align="C",
            )

            pdf_output_path = "reporte_oficial.pdf"
            pdf.output(pdf_output_path)

            with open(pdf_output_path, "rb") as f:
                pdf_bytes = f.read()

            st.success("¡PDF Oficial generado con éxito!")
            st.download_button(
                label="📥 Descargar Archivo PDF",
                data=pdf_bytes,
                file_name=(
                    f"Reporte_Asistencia_{datetime.now().strftime('%Y-%m-%d')}.pdf"
                ),
                mime="application/pdf",
            )
