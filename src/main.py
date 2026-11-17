# Aseguramos que el script apunte a la carpeta del proyecto
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ))              # para importar Assets
sys.path.append(str(RAIZ / "src"))      # para importar config

# Librerias GUI
import streamlit as st
from PIL import Image

# Librerias custom de configuracion
from Assets import assets
import config

# Cargamos configuracion
configuracion = config.cargar()
idioma = configuracion["idioma"]
ancho, _alto = configuracion["tamano"].split("x")
textos = assets.BOTON_TEXTOS[idioma]

# Configuracion de la pagina (tiene que ser lo primero de Streamlit)
icono = RAIZ / "Assets" / "logo.png"
st.set_page_config(
    page_title=assets.VENTANA_TITULO[idioma]["titulo"],
    page_icon=Image.open(icono) if icono.exists() else "🎯",
    layout="centered",
)

# Estilos de la pagina: color de fondo y ancho maximo segun la configuracion
def cargar_css():
    variables = f"""
    :root {{
        --fondo: {assets.VENTANA_BG};
        --separacion: {assets.BOTON_SEPARACION}px;
        --boton-ancho: {assets.BOTON_ANCHO}px;
        --boton-alto: {assets.BOTON_ALTO}px;
        --boton-color: {assets.BOTON_COLOR};
    }}
    """
    css = (RAIZ / "Assets" / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{variables}{css}</style>", unsafe_allow_html=True)

cargar_css()

# Streamlit vuelve a ejecutar este script en cada clic, por eso la
# opcion elegida se guarda en session_state
def seleccionar_jugar(accion):
    st.session_state["accion"] = accion

# Alterna el idioma entre "es" y "en" y lo guarda en config.txt
# (recarga la config adentro para no usar valores de la ejecucion anterior)
def cambiar_idioma():
    cfg = config.cargar()
    cfg["idioma"] = "en" if cfg["idioma"] == "es" else "es"
    config.guardar(cfg)
    st.session_state["accion"] = "idioma"

# Mensaje de la opcion seleccionada (linea de alto fijo para que no salte el layout)
mensajes = {
    "jugar": textos["lbl_jugar"],
    "idioma": textos["lbl_idioma"]
}
mensaje = mensajes.get(st.session_state.get("accion"), "")
st.markdown(
    f"<p style='text-align:center; color:#000; min-height:2em;'>{escape(mensaje)}</p>",
    unsafe_allow_html=True,
)

# Crear y mostrar botones (on_click corre antes del script, asi el mensaje se actualiza)
st.button(textos["btn_jugar"], on_click=seleccionar_jugar, args=("jugar",))
st.button(textos["btn_idioma"], on_click=cambiar_idioma)
