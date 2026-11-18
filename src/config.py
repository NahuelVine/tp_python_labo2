import streamlit as st
import streamlit.components.v1 as components

lista_idiomas = ("es", "en")
cookie_default = "es"
cookie_nombre = "idioma"
cookie_fecha = 60 * 60 * 24 * 365 # Dura un año

def cargar_idioma():
    if cookie_nombre not in st.session_state:
        valor = st.context.cookies.get(cookie_nombre, cookie_default)
        st.session_state[cookie_nombre] = valor if valor in lista_idiomas else cookie_default

def guardar_idioma(idioma: str):
    st.session_state[cookie_nombre] = idioma

def sincronizar_cookie():
    idioma = st.session_state[cookie_nombre]
    components.html(
        f"<script>window.parent.document.cookie = "
        f"'{cookie_nombre}={idioma}; path=/; max-age={cookie_fecha}; SameSite=Lax';</script>",
        height=0,
    )