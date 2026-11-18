# Desarrollado por Nahuel Iovine y Marcos Zurita Tropea
import json, runpy, sys
from html import escape
from pathlib import Path
# GUI de la app
import streamlit as st
from PIL import Image

# Aseguramos que el script apunte a la carpeta del proyecto
raiz_path = Path(__file__).resolve().parent.parent
# Assets
sys.path.append(str(raiz_path))
# Config
sys.path.append(str(raiz_path/"src"))      

# Configuracion y assets
from Assets import assets
import config

# Funcion para volver al menu principal desde la pantalla del minijuego Ahorcado.py
def volver_al_menu():
    st.session_state["pantalla"] = "menu"
# Añadimos el boton a la pantalla de juego
if st.session_state.get("pantalla") == "juego":
    runpy.run_path(str(raiz_path/"src"/"Ahorcado.py"))
    st.sidebar.button(assets.JUEGO_TEXTOS[st.session_state["idioma"]]["volver"], on_click=volver_al_menu)
    st.stop()

# Cargamos configuracion
config.cargar_idioma()
textos = assets.BOTON_TEXTOS[st.session_state["idioma"]]
icon = raiz_path/"Assets"/"icon.png"

# Configuracion de la ventana de pagina
st.set_page_config(
    page_title=assets.VENTANA_TITULO[st.session_state["idioma"]]["titulo"],
    page_icon=Image.open(icon) if icon.exists() else "➰",
    layout="centered",
)

# Estilos para la pagina
# Diseño sale de styles.css 
# Textos/colores de assets.py
def cargar_css():
    tarjetas = assets.MENU_TARJETAS[st.session_state["idioma"]]
    # Declaramos las variables para usar en el CSS, valores que se van a repetir o queremos tener a mano para modificar.
    variables = f"""
    :root {{
        --fondo: {assets.VENTANA_BG};
        --desc-jugar: {json.dumps(tarjetas["jugar"], ensure_ascii=False)};
        --desc-idioma: {json.dumps(tarjetas["idioma"], ensure_ascii=False)};
    }}
    """
    # Importamos la fuente Anton y Space Grotesk para los textos del menú (encabezado y botones) desde Google Fonts
    fuente = "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;500;700&display=swap');"
    css = (raiz_path/"Assets"/"styles.css").read_text(encoding="utf-8") # Con encoding UTf-8 nos aseguramos que se muestren todos los caracteres necesarios
    st.markdown(f"<style>{fuente}{variables}{css}</style>", unsafe_allow_html=True)

cargar_css()

# Streamlit vuelve a ejecutar este script en cada clic, por eso la
# opcion elegida se guarda en session_state
def seleccionar_jugar():
    st.session_state["pantalla"] = "juego"

# Alterna el idioma entre "es" y "en"
def cambiar_idioma():
    config.guardar_idioma("en" if st.session_state["idioma"] == "es" else "es")

# Streamlit trabaja en cascada, por eso es importante el orden del armado: Header -> Menu -> Footer

# HEADER
# Armamos el HTML del titulo
titulo = assets.TITULO[st.session_state["idioma"]]
st.markdown(
    "<div class='titulo'><div class='titulo-caja'>"
    f"<div class='titulo-genero'>{escape(titulo['genero'])}</div>"
    f"<div class='titulo-nombre'>{escape(titulo['nombre'])}</div>"
    f"<div class='titulo-promesa'>{escape(titulo['promesa'])}</div>"
    "</div></div>",
    unsafe_allow_html=True,
)

# MENU
# Mascota + botonera
col_mascota, col_menu = st.columns([301, 440], vertical_alignment="bottom")
with col_mascota:
    logo = raiz_path/"Assets"/"mascot_logo.png"
    if logo.exists():
        st.image(Image.open(logo), width=187)

with col_menu, st.container(key="menu"):
    st.markdown(
        f'<div class="menu-encabezado">{escape(assets.MENU_ENCABEZADO[st.session_state["idioma"]])}</div>',
        unsafe_allow_html=True,
    )
    st.button(textos["btn_jugar"], key="btn_jugar", on_click=seleccionar_jugar)
    st.button(textos["btn_idioma"], key="btn_idioma", on_click=cambiar_idioma)

# FOOTER
footer = assets.FOOTER[st.session_state["idioma"]]
st.markdown(
    "<div class='footer'>"
    f"<span class='footer-creditos'>{escape(footer['creditos'])}</span>"
    f"<span class='footer-version'>{escape(footer['idioma'])}/{escape(assets.VERSION)}</span>"
    "</div>",
    unsafe_allow_html=True,
)

# Al final para evitar modificar la interfaz
config.sincronizar_cookie()