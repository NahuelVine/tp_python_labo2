import random               # Permite generar números aleatorios. Y sí, sabemos que no son realmente aleatorios, pero a efectos prácticos de este código sí que lo son.
from pathlib import Path    # Permite trabajar con rutas de archivos entre plataformas.
import streamlit as st      # Framework que sí que nos dejan usar.

st.set_page_config(page_title="AHORCADO - La película, Solo en Labo 2", page_icon="🎯")

# Función que le da formato al texto, eso que dice "background-color" le da color too'guapo al fondo; mientras que lo que dice "color" sería el color del texto en cuestión.
st.markdown("""                             
    <style>
    /* Fondo personalizado */
    .stApp {
        background-color: #3E0000;                                   
    }
    
    /* Tipografía Impact y letras blancas para textos generales */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown {
        color: #F7F7F7 !important;
        font-family: 'Impact', sans-serif !important;
        letter-spacing: 2px;
    }
    
    pre {
        font-family: 'Impact', sans-serif !important;
        color: #F7F7F7 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
    }

    .stButton>button, .stNumberInput input {
        font-family: 'Impact', sans-serif !important;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Evita que haya discriminación entre las MAYÚSCULAS, minúsculas y demás letras esotéricas del español.
def limpiar_texto(texto):
    """Elimina tildes, convierte a mayúsculas y maneja la Ñ para que los pinches gringos vayan a llorar un rato."""
    texto = texto.upper()
    reemplazos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U',
        'Ñ': 'N'
    }
    for con_tilde, sin_tilde in reemplazos.items():
        texto = texto.replace(con_tilde, sin_tilde)
    return texto

def cargar_datos(idioma):
    """Carga el archivo de palabras y su respectiva ayuda (si existe) según el idioma seleccionado."""
    archivos = {
        "Español": ("Palabras_es.txt", None),
        "Inglés": ("Palabras_en.txt", None),
        "Coreano": ("Palabras_kr.txt", "Ayudas_kr.txt"),
        "Japonés": ("Palabras_jp.txt", "Ayudas_jp.txt"),
        "Chino": ("Palabras_ch.txt", "Ayudas_ch.txt")
    }
    
    palabras_file, ayuda_file = archivos.get(idioma, ("Palabras_es.txt", None))
    
    # Cargar palabras con respaldo por defecto
    palabras = ["PYTHON", "STREAMLIT", "AHORCADO"]
    archivo_p = Path(palabras_file)
    if not archivo_p.exists():
        archivo_p = Path(palabras_file.lower())
        
    if archivo_p.exists():
        with open(archivo_p, encoding="utf-8") as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
            if lineas:
                palabras = [limpiar_texto(l) for l in lineas]
                
    # Cargar ayudas / etimologías si corresponde
    ayudas = []
    if ayuda_file:
        archivo_a = Path(ayuda_file)
        if not archivo_a.exists():
            archivo_a = Path(ayuda_file.lower())
        if archivo_a.exists():
            with open(archivo_a, encoding="utf-8") as f:
                ayudas = [linea.strip() for linea in f if linea.strip()]
                
    return palabras, ayudas

# Dibujos del monigote.
AHORCADO = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========""",
]

# Lógica del código en cuestión, ahora con soporte para pistas indexadas.
class AhorcadoLogica:
    def __init__(self, palabras, ayudas=None, max_intentos=6):
        self.palabras = palabras
        self.ayudas = ayudas if ayudas else []
        self.indice = random.randint(0, len(palabras) - 1)
        self.palabra = self.palabras[self.indice]
        self.adivinadas = set()
        self.falladas = set()
        self.max_intentos = max_intentos

    @property
    def intentos_restantes(self):
        return self.max_intentos - len(self.falladas)

    @property
    def ayuda_actual(self):
        if self.ayudas and self.indice < len(self.ayudas):
            return self.ayudas[self.indice]
        return None

    def estado(self):
        return " ".join(c if limpiar_texto(c) in self.adivinadas else "_" for c in self.palabra)

    def intentar(self, letra):
        letra_limpia = limpiar_texto(letra)
        if len(letra_limpia) != 1 or not letra_limpia.isalpha():
            return "invalido"
        if letra_limpia in self.adivinadas or letra_limpia in self.falladas:
            return "repetida"
        
        palabra_limpia = limpiar_texto(self.palabra)
        if letra_limpia in palabra_limpia:
            self.adivinadas.add(letra_limpia)
            return "acierto"
        
        self.falladas.add(letra_limpia)
        return "fallo"

    def gano(self):
        palabra_limpia = limpiar_texto(self.palabra)
        return all(limpiar_texto(c) in self.adivinadas for c in palabra_limpia)

    def perdio(self):
        return self.intentos_restantes <= 0


# Configuración por defecto en session_state (idioma y vidas).
if "idioma_config" not in st.session_state:
    st.session_state.idioma_config = "Español"
if "vidas_config" not in st.session_state:
    st.session_state.vidas_config = 6


# Menú Principal puesto a un costado.
st.sidebar.title("📌 Menú Principal")
opcion = st.sidebar.radio("Selecciona una opción:", ["JUGAR", "Configuración", "Salir"])


# Lógicas de las opciones.
if opcion == "JUGAR":
    st.title("AHORCADO, la película, solo en Labo 2")
    
    # Cargar datos según el idioma seleccionado
    palabras, ayudas = cargar_datos(st.session_state.idioma_config)
    
    # Si no hay juego activo, o si cambió la configuración de vidas/idioma, reiniciamos la partida
    if "juego" not in st.session_state or st.session_state.juego.max_intentos != st.session_state.vidas_config or len(st.session_state.juego.palabras) != len(palabras):
        st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)

    juego = st.session_state.juego

    # Gráficos y Estado.
    indice_dibujo = min(len(juego.falladas), len(AHORCADO) - 1)
    st.text(AHORCADO[indice_dibujo])
    
    st.markdown(f"### Palabra: `{juego.estado()}`")
    st.write(f"**Modo / Idioma:** {st.session_state.idioma_config}")
    st.write(f"**Falladas:** {' '.join(sorted(juego.falladas)) or '-'}")
    st.write(f"**Intentos restantes:** {juego.intentos_restantes}")

    # Mostrar cuadro de ayuda/etimología si el idioma cuenta con archivo de ayuda
    ayuda_actual = juego.ayuda_actual
    if ayuda_actual:
        st.info(f"💡 **Etimología / Pista ({st.session_state.idioma_config}):**\n\n{ayuda_actual}")

    if juego.gano():
        st.success(f"🎉 ¡Q GRANDE! Le pegaste a la palabra, la cual por cierto era: {juego.palabra}")
        if st.button("¿Querés volver demostrar lo kpo que sos? ¿Cagoneta?"):
            st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
            st.rerun()
    elif juego.perdio():
        st.error(f"   JAAAAA, perdiste, fracasado, JAAAAA. La palabra era: {juego.palabra}")
        if st.button("Por favor, volvé a jugar así nos seguimos burlando de vos."):
            st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
            st.rerun()
    else:
        letra = st.text_input("Ingresa una letra:", max_chars=1)
        
        if st.button("Ver si está en la palabra."):
            if letra:
                resultado = juego.intentar(letra)
                if resultado == "invalido":
                    st.warning("Salame, no podés ingresar esa letra.")
                elif resultado == "repetida":
                    st.info("Ya usaste la letra, ¿para qué la volvés a iniciar?")
                elif resultado == "acierto":
                    st.success("✅ CORRECTO ✅")
                elif resultado == "fallo":
                    st.error("❌ EPIC FAIL ❌")
                st.rerun()

elif opcion == "Configuración":
    st.title("⚙️ CONFIGURACIÓN ⚙️")
    st.write("Cambiar parámetros de la partida.")
    
    # Selector de Idioma / Modo de juego
    idiomas_disponibles = ["Español", "Inglés", "Coreano", "Japonés", "Chino"]
    nuevo_idioma = st.selectbox(
        "Selecciona el idioma / modo de juego:",
        idiomas_disponibles,
        index=idiomas_disponibles.index(st.session_state.idioma_config) if st.session_state.idioma_config in idiomas_disponibles else 0
    )
    
    # Selector de cantidad de vidas (entre 3 y 20)
    nuevas_vidas = st.number_input(
        "Cantidad de vidas (Escribir entre el 3 y 20):", 
        min_value=3, 
        max_value=20, 
        value=st.session_state.vidas_config, 
        step=1
    )
    
    if st.button("Guardar configuración"):
        st.session_state.idioma_config = nuevo_idioma
        st.session_state.vidas_config = nuevas_vidas
        if "juego" in st.session_state:
            del st.session_state.juego
        st.success(f"¡Confirmado! Idioma: {nuevo_idioma} | Vidas: {nuevas_vidas}.")

elif opcion == "Salir":
    st.title("¡Gracias por hacer el ridículo! ¡Nos vemos!")
    st.write("Puedes cerrar esta pestaña del navegador de forma segura.")
    if "juego" in st.session_state:
        del st.session_state.juego