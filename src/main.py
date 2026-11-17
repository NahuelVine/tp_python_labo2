import json
import runpy
import sys
from html import escape
from pathlib import Path
# GUI de la app
import streamlit as st

# Aseguramos que el script apunte a la carpeta del proyecto
RAIZ = Path(__file__).resolve().parent.parent
# Assets
sys.path.append(str(RAIZ))
# Config
sys.path.append(str(RAIZ / "src"))      


# Configuracion y assets
from Assets import assets
import config

# Funcion para volver al menu principal desde la pantalla del minijuego Ahorcado.py
def volver_al_menu():
    st.session_state["pantalla"] = "menu"
# Añadimos el boton a la pantalla de juego
if st.session_state.get("pantalla") == "juego":
    runpy.run_path(str(RAIZ / "Ahorcado.py"))
    st.sidebar.button("⬅ Volver al menú principal", on_click=volver_al_menu)
    st.stop()

# Cargamos configuracion
configuracion = config.cargar()
# El idioma va a determinar como mostramos los textos
idioma = configuracion["idioma"]
ancho, _alto = configuracion["tamano"].split("x")
textos = assets.BOTON_TEXTOS[idioma]

# Configuracion de la ventana de pagina
st.set_page_config(
    page_title=assets.VENTANA_TITULO[idioma]["titulo"],
    page_icon="🎯",
    layout="centered",
)

# Estilos para la pagina
# Diseño sale de styles.css 
# Textos/colores de assets.py
def cargar_css():
    tarjetas = assets.MENU_TARJETAS[idioma]
    variables = f"""
    :root {{
        --fondo: {assets.VENTANA_BG};
        --desc-jugar: {json.dumps(tarjetas["jugar"], ensure_ascii=False)};
        --desc-idioma: {json.dumps(tarjetas["idioma"], ensure_ascii=False)};
    }}
    """
    # Importamos la fuente Anton para el texto
    fuente = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;500;700&display=swap');"
    css = (RAIZ/"Assets"/"styles.css").read_text(encoding="utf-8") # Con encoding UTf-8 nos aseguramos que se muestren todos los caracteres necesarios
    st.markdown(f"<style>{fuente}{variables}{css}</style>", unsafe_allow_html=True)

cargar_css()

# Streamlit vuelve a ejecutar este script en cada clic, por eso la
# opcion elegida se guarda en session_state
def seleccionar_jugar():
    st.session_state["pantalla"] = "juego"

# Alterna el idioma entre "es" y "en" y lo guarda en config.txt
def cambiar_idioma():
    cfg = config.cargar()
    cfg["idioma"] = "en" if cfg["idioma"] == "es" else "es"
    config.guardar(cfg)

# Armamos el HTML del titulo
titulo = assets.TITULO[idioma]
st.markdown(
    "<div class='titulo'><div class='titulo-caja'>"
    f"<div class='titulo-genero'>{escape(titulo['genero'])}</div>"
    f"<div class='titulo-nombre'>{escape(titulo['nombre'])}</div>"
    f"<div class='titulo-promesa'>{escape(titulo['promesa'])}</div>"
    "</div></div>",
    unsafe_allow_html=True,
)

# HTML encabezado + botonera
with st.container(key="menu"):
    st.markdown(
        f"<div class='menu-encabezado'>{escape(assets.MENU_ENCABEZADO[idioma])}</div>",
        unsafe_allow_html=True,
    )
    st.button(textos["btn_jugar"], key="btn_jugar", on_click=seleccionar_jugar)
    st.button(textos["btn_idioma"], key="btn_idioma", on_click=cambiar_idioma)

# HTML footer
footer = assets.FOOTER[idioma]
st.markdown(
    "<div class='footer'>"
    f"<span class='footer-creditos'>{escape(footer['creditos'])}</span>"
    f"<span class='footer-version'>{escape(footer['idioma'])}/{escape(assets.VERSION)}</span>"
    "</div>",
    unsafe_allow_html=True,
)