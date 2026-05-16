import streamlit as st
import json
import random
from pathlib import Path

CARPETA_DATA = Path("data")
TOTAL_PREGUNTAS = 10

st.set_page_config(
    page_title="Banco de Preguntas por Temas",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0A1931 0%, #102542 100%);
    color: white;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4, p, label, span {
    color: white !important;
}

.header-card {
    background: linear-gradient(90deg, #0F172A, #1D4ED8);
    padding: 24px;
    border-radius: 20px;
    border: 2px solid #FACC15;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

.header-card h1 {
    font-size: 42px;
    margin: 0;
    letter-spacing: 1px;
}

.subtitle {
    color: #DBEAFE !important;
    font-size: 18px;
    margin-top: 8px;
}

.tema-card {
    background: #102542;
    border: 1px solid #334155;
    border-radius: 22px;
    padding: 24px;
    height: 260px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    margin-bottom: 12px;
}

.tema-titulo {
    font-size: 1.65rem;
    font-weight: 800;
    color: white;
    line-height: 1.2;
    min-height: 88px;
}

.tema-info {
    font-size: 1.05rem;
    color: #DBEAFE;
    line-height: 1.6;
}

.question-card {
    background: #132F4C;
    border-left: 8px solid #FACC15;
    padding: 24px;
    border-radius: 18px;
    min-height: 310px;
    max-height: 430px;
    overflow-y: auto;
    font-size: 19px;
    line-height: 1.7;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.option-title {
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 14px;
    color: white;
}

/* BOTONES NORMALES */
.stButton > button {
    border-radius: 14px;
    min-height: 52px;
    font-weight: 700;
    font-size: 15px;
    border: 1px solid #FACC15 !important;
    white-space: normal;
    text-align: center;
    background-color: #102542 !important;
    color: #FFFFFF !important;
}

/* HOVER */
.stButton > button:hover {
    background-color: #FACC15 !important;
    color: #0A1931 !important;
    border-color: #FFFFFF !important;
}

/* BOTONES PRIMARY */
.stButton > button[kind="primary"] {
    background-color: #FACC15 !important;
    color: #0A1931 !important;
    border: 1px solid #FACC15 !important;
}

/* BOTONES PRIMARY HOVER */
.stButton > button[kind="primary"]:hover {
    background-color: #FFE066 !important;
    color: #0A1931 !important;
    border-color: #FFFFFF !important;
}

/* BOTONES DESHABILITADOS */
.stButton > button:disabled {
    background-color: #1E293B !important;
    color: #94A3B8 !important;
    border: 1px solid #475569 !important;
}

div[data-testid="stMetric"] {
    background: #102542;
    border: 1px solid #334155;
    padding: 14px;
    border-radius: 16px;
}

div[data-testid="stMetricValue"] {
    color: #FACC15 !important;
}

div[data-testid="stProgress"] > div > div > div {
    background-color: #FACC15;
}

div[data-testid="stExpander"] {
    background-color: #102542;
    border: 1px solid #334155;
    border-radius: 12px;
}

hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)


def cargar_archivos_temas():
    if not CARPETA_DATA.exists():
        st.error("No existe la carpeta data/.")
        st.stop()

    archivos = sorted(CARPETA_DATA.glob("*.json"))

    if not archivos:
        st.error("No se encontraron archivos JSON dentro de data/.")
        st.stop()

    temas = []

    for archivo in archivos:
        with open(archivo, "r", encoding="utf-8") as f:
            preguntas = json.load(f)

        preguntas_validas = []

        for p in preguntas:
            if (
                isinstance(p, dict)
                and "tema" in p
                and "pregunta" in p
                and "opciones" in p
                and "respuesta" in p
                and isinstance(p["opciones"], dict)
                and all(letra in p["opciones"] for letra in ["A", "B", "C", "D"])
                and p["respuesta"] in ["A", "B", "C", "D"]
            ):
                preguntas_validas.append(p)

        if preguntas_validas:
            temas.append({
                "archivo": archivo,
                "tema": preguntas_validas[0]["tema"],
                "total": len(preguntas_validas),
                "preguntas": preguntas_validas
            })

    if not temas:
        st.error("No hay preguntas válidas en los archivos JSON.")
        st.stop()

    return temas


def iniciar_juego(tema_info):
    preguntas_tema = tema_info["preguntas"]

    if len(preguntas_tema) < TOTAL_PREGUNTAS:
        st.error(f"El tema {tema_info['tema']} no tiene suficientes preguntas.")
        st.stop()

    st.session_state.tema = tema_info["tema"]
    st.session_state.preguntas = random.sample(preguntas_tema, TOTAL_PREGUNTAS)
    st.session_state.indice = 0
    st.session_state.respuestas = [""] * TOTAL_PREGUNTAS
    st.session_state.finalizado = False
    st.session_state.juego_iniciado = True
    st.session_state.juego_id = random.randint(10000, 99999)


def calcular_puntaje():
    return sum(
        1 for i, p in enumerate(st.session_state.preguntas)
        if st.session_state.respuestas[i] == p["respuesta"]
    )


def pantalla_temas():
    temas = cargar_archivos_temas()

    st.markdown("""
    <div class="header-card">
        <h1>🧠 BANCO DE PREGUNTAS</h1>
        <p class="subtitle">Selecciona un tema para comenzar tu práctica</p>
    </div>
    """, unsafe_allow_html=True)

    columnas = st.columns(3)

    for i, tema_info in enumerate(temas):
        with columnas[i % 3]:
            st.markdown(f"""
            <div class="tema-card">
                <div>
                    <div class="tema-titulo">{tema_info["tema"]}</div>
                    <div class="tema-info">
                        {tema_info["total"]} preguntas disponibles<br>
                        Se elegirán {TOTAL_PREGUNTAS} preguntas al azar.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Comenzar",
                key=f"tema_{i}_{tema_info['archivo'].stem}",
                use_container_width=True,
                type="primary"
            ):
                iniciar_juego(tema_info)
                st.rerun()


def pantalla_juego():
    indice = st.session_state.indice
    pregunta = st.session_state.preguntas[indice]
    respuesta_actual = st.session_state.respuestas[indice]

    st.markdown(f"""
    <div class="header-card">
        <h1>{st.session_state.tema}</h1>
        <p class="subtitle">Pregunta {indice + 1} de {TOTAL_PREGUNTAS}</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress((indice + 1) / TOTAL_PREGUNTAS)

    col_pregunta, col_opciones = st.columns([2.25, 1])

    with col_pregunta:
        st.subheader("Pregunta")
        pregunta_html = str(pregunta["pregunta"]).replace("\n", "<br>")
        st.markdown(f"""
        <div class="question-card">
            {pregunta_html}
        </div>
        """, unsafe_allow_html=True)

    with col_opciones:
        st.markdown('<div class="option-title">Opciones</div>', unsafe_allow_html=True)

        for letra in ["A", "B", "C", "D"]:
            texto = pregunta["opciones"][letra]
            seleccionada = respuesta_actual == letra
            tipo = "primary" if seleccionada else "secondary"

            if st.button(
                f"{letra}) {texto}",
                key=f"{st.session_state.juego_id}_{indice}_{pregunta.get('id', indice)}_{letra}",
                use_container_width=True,
                type=tipo
            ):
                st.session_state.respuestas[indice] = letra
                st.rerun()

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button("⬅ Anterior", disabled=indice == 0, use_container_width=True):
            st.session_state.indice -= 1
            st.rerun()

    with c2:
        if st.button("Saltar", use_container_width=True):
            st.session_state.respuestas[indice] = ""

            if indice < TOTAL_PREGUNTAS - 1:
                st.session_state.indice += 1
            else:
                st.session_state.finalizado = True

            st.rerun()

    with c3:
        if st.button("Siguiente ➡", use_container_width=True):
            if indice < TOTAL_PREGUNTAS - 1:
                st.session_state.indice += 1
            else:
                st.session_state.finalizado = True

            st.rerun()

    with c4:
        if st.button("Finalizar", type="primary", use_container_width=True):
            st.session_state.finalizado = True
            st.rerun()


def pantalla_resultados():
    puntaje = calcular_puntaje()
    respondidas = sum(1 for r in st.session_state.respuestas if r)
    saltadas = TOTAL_PREGUNTAS - respondidas
    incorrectas = respondidas - puntaje

    st.markdown(f"""
    <div class="header-card">
        <h1>Resultados</h1>
        <p class="subtitle">Tema: {st.session_state.tema}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Correctas", puntaje)

    with c2:
        st.metric("Incorrectas", incorrectas)

    with c3:
        st.metric("Saltadas", saltadas)

    with c4:
        st.metric("Puntaje final", f"{puntaje}/{TOTAL_PREGUNTAS}")

    st.subheader("Detalle de respuestas")

    for i, pregunta in enumerate(st.session_state.preguntas):
        usuario = st.session_state.respuestas[i]
        correcta = pregunta["respuesta"]

        if not usuario:
            estado = "Saltada"
        elif usuario == correcta:
            estado = "Correcta"
        else:
            estado = "Incorrecta"

        with st.expander(f"Pregunta {i + 1} - {estado}"):
            st.write("**Pregunta:**")
            st.write(pregunta["pregunta"])

            st.write("**Opciones:**")
            for letra, texto in pregunta["opciones"].items():
                st.write(f"{letra}) {texto}")

            st.write(f"**Respuesta correcta:** {correcta}")
            st.write(f"**Respuesta del usuario:** {usuario if usuario else 'Sin responder'}")
            st.write(f"**Estado:** {estado}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reiniciar mismo tema", type="primary", use_container_width=True):
            tema_actual = st.session_state.tema
            temas = cargar_archivos_temas()
            tema_info = next((t for t in temas if t["tema"] == tema_actual), None)

            if tema_info:
                iniciar_juego(tema_info)
                st.rerun()

    with col2:
        if st.button("Volver a temas", use_container_width=True):
            st.session_state.clear()
            st.rerun()


if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    pantalla_temas()
elif st.session_state.finalizado:
    pantalla_resultados()
else:
    pantalla_juego()