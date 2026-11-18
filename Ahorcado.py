import random
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="AHORCADO - La película, Solo en Labo 2", page_icon="🎯")

st.markdown("""                             
    <style>
    .stApp {
        background-color: #3E0000;                                   
    }
    
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

def limpiar_texto(texto):
    texto = texto.upper()
    reemplazos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U',
        'Ñ': 'N'
    }
    for con_tilde, sin_tilde in reemplazos.items():
        texto = texto.replace(con_tilde, sin_tilde)
    return texto

def cargar_datos(idioma):
    archivos = {
        "Español": ("Palabras_es.txt", None),
        "Inglés": ("Palabras_en.txt", None),
        "Coreano": ("Palabras_kr.txt", "Ayudas_kr.txt"),
        "Japonés": ("Palabras_jp.txt", "Ayudas_jp.txt"),
        "Chino": ("Palabras_ch.txt", "Ayudas_ch.txt")
    }
    
    palabras_file, ayuda_file = archivos.get(idioma, ("Palabras_es.txt", None))
    
    palabras = ["PYTHON", "STREAMLIT", "AHORCADO"]
    archivo_p = Path(palabras_file)
    if not archivo_p.exists():
        archivo_p = Path(palabras_file.lower())
        
    if archivo_p.exists():
        with open(archivo_p, encoding="utf-8") as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
            if lineas:
                palabras = [limpiar_texto(l) for l in lineas]
                
    ayudas = []
    if ayuda_file:
        archivo_a = Path(ayuda_file)
        if not archivo_a.exists():
            archivo_a = Path(ayuda_file.lower())
        if archivo_a.exists():
            with open(archivo_a, encoding="utf-8") as f:
                ayudas = [linea.strip() for linea in f if linea.strip()]
                
    return palabras, ayudas

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


class AhorcadoSupervivencia:
    def __init__(self, palabras, ayudas=None, max_vidas=6):
        self.palabras = palabras
        self.ayudas = ayudas if ayudas else []
        self.max_vidas = max_vidas
        self.vidas_restantes = max_vidas
        self.palabras_adivinadas = 0
        self._cargar_nueva_palabra()

    def _cargar_nueva_palabra(self):
        self.indice = random.randint(0, len(self.palabras) - 1)
        self.palabra = self.palabras[self.indice]
        self.adivinadas = set()
        self.falladas_palabra = set()

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
        if letra_limpia in self.adivinadas or letra_limpia in self.falladas_palabra:
            return "repetida"
        
        palabra_limpia = limpiar_texto(self.palabra)
        if letra_limpia in palabra_limpia:
            self.adivinadas.add(letra_limpia)
            return "acierto"
        
        self.falladas_palabra.add(letra_limpia)
        self.vidas_restantes -= 1
        return "fallo"

    def gano(self):
        palabra_limpia = limpiar_texto(self.palabra)
        return all(limpiar_texto(c) in self.adivinadas for c in palabra_limpia)

    def siguiente_palabra(self):
        self.palabras_adivinadas += 1
        self._cargar_nueva_palabra()

    def perdio(self):
        return self.vidas_restantes <= 0


if "idioma_config" not in st.session_state:
    st.session_state.idioma_config = "Español"
if "vidas_config" not in st.session_state:
    st.session_state.vidas_config = 6
if "modo_config" not in st.session_state:
    st.session_state.modo_config = "Clásico"


st.sidebar.title("📌 Menú Principal")
opcion = st.sidebar.radio("Selecciona una opción:", ["JUGAR", "Configuración", "Salir"])


if opcion == "JUGAR":
    if st.session_state.modo_config == "Clásico":
        st.title("AHORCADO, la película, solo en Labo 2")
        
        palabras, ayudas = cargar_datos(st.session_state.idioma_config)
        
        if "juego" not in st.session_state or st.session_state.juego.max_intentos != st.session_state.vidas_config or len(st.session_state.juego.palabras) != len(palabras):
            st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)

        juego = st.session_state.juego

        indice_dibujo = min(len(juego.falladas), len(AHORCADO) - 1)
        st.text(AHORCADO[indice_dibujo])
        
        st.markdown(f"### Palabra: `{juego.estado()}`")
        st.write(f"**Modo / Idioma:** {st.session_state.idioma_config} (Clásico)")
        st.write(f"**Falladas:** {' '.join(sorted(juego.falladas)) or '-'}")
        st.write(f"**Intentos restantes:** {juego.intentos_restantes}")

        ayuda_actual = juego.ayuda_actual
        if ayuda_actual:
            st.info(f"💡 **Etimología / Pista ({st.session_state.idioma_config}):**\n\n{ayuda_actual}")

        if juego.gano():
            st.success(f"🎉 ¡GRANDE! Le pegaste a la palabra, la cual por cierto era: {juego.palabra}")
            if st.button("¿Querés volver a jugar?"):
                st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
                st.rerun()
        elif juego.perdio():
            st.error(f"   Una pena, perdiste. La palabra era: {juego.palabra}")
            if st.button("Por favor, volvé a jugar así te superás a vos mismo."):
                st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
                st.rerun()
        else:
            letra = st.text_input("Ingresa una letra:", max_chars=1, key="input_clasico")
            
            if st.button("Ver si está en la palabra.", key="btn_clasico"):
                if letra:
                    resultado = juego.intentar(letra)
                    if resultado == "invalido":
                        st.warning("No podés con esa letra.")
                    elif resultado == "repetida":
                        st.info("Ya usaste la letra...")
                    elif resultado == "acierto":
                        st.success("✅ CORRECTO ✅")
                    elif resultado == "fallo":
                        st.error("❌ EPIC FAIL ❌")
                    st.rerun()
                    
    elif st.session_state.modo_config == "Supervivencia":
        st.title("🔥 AHORCADO: MODO SUPERVIVENCIA 🔥")
        
        palabras, ayudas = cargar_datos(st.session_state.idioma_config)
        
        if "juego_supervivencia" not in st.session_state or st.session_state.juego_supervivencia.max_vidas != st.session_state.vidas_config or len(st.session_state.juego_supervivencia.palabras) != len(palabras):
            st.session_state.juego_supervivencia = AhorcadoSupervivencia(palabras, ayudas, max_vidas=st.session_state.vidas_config)

        juego = st.session_state.juego_supervivencia

        intentos_fallidos = juego.max_vidas - juego.vidas_restantes
        indice_dibujo = min(int((intentos_fallidos / juego.max_vidas) * (len(AHORCADO) - 1)), len(AHORCADO) - 1)
        st.text(AHORCADO[indice_dibujo])
        
        st.markdown(f"### Palabra: `{juego.estado()}`")
        st.markdown(f"🏆 **Palabras adivinadas en la sesión:** `{juego.palabras_adivinadas}`")
        st.write(f"**Modo / Idioma:** {st.session_state.idioma_config} (Supervivencia)")
        st.write(f"**Letras falladas en esta palabra:** {' '.join(sorted(juego.falladas_palabra)) or '-'}")
        st.write(f"❤️ **Vidas restantes (Globales):** {juego.vidas_restantes} / {juego.max_vidas}")

        ayuda_actual = juego.ayuda_actual
        if ayuda_actual:
            st.info(f"💡 **Etimología / Pista ({st.session_state.idioma_config}):**\n\n{ayuda_actual}")

        if juego.perdio():
            st.error(f"💀 ¡SE ACABÓ EL JUEGO! Te quedaste sin vidas. Lograste adivinar **{juego.palabras_adivinadas}** palabras. ¡Fracasado total, JAAAAA!")
            if st.button("🔄 Volver a intentar Supervivencia"):
                st.session_state.juego_supervivencia = AhorcadoSupervivencia(palabras, ayudas, max_vidas=st.session_state.vidas_config)
                st.rerun()
        else:
            if juego.gano():
                st.success(f"🎉 ¡PALABRA SUPERADA! Era: **{juego.palabra}**. Pasando a la siguiente...")
                juego.siguiente_palabra()
                st.rerun()
            else:
                letra = st.text_input("Ingresa una letra:", max_chars=1, key="input_supervivencia")
                
                if st.button("Ver si está en la palabra.", key="btn_supervivencia"):
                    if letra:
                        resultado = juego.intentar(letra)
                        if resultado == "invalido":
                            st.warning("No podés con esa letra.")
                        elif resultado == "repetida":
                            st.info("Ya usaste la letra...")
                        elif resultado == "acierto":
                            st.success("✅ CORRECTO ✅")
                        elif resultado == "fallo":
                            st.error("❌ ¡VIDA GLOBAL PERDIDA! ❌")
                        st.rerun()

elif opcion == "Configuración":
    st.title("⚙️ CONFIGURACIÓN ⚙️")
    st.write("Cambiar parámetros de la partida.")
    
    modos_disponibles = ["Clásico", "Supervivencia"]
    nuevo_modo = st.selectbox(
        "Selecciona el modo de juego:",
        modos_disponibles,
        index=modos_disponibles.index(st.session_state.modo_config) if st.session_state.modo_config in modos_disponibles else 0
    )
    
    idiomas_disponibles = ["Español", "Inglés", "Coreano", "Japonés", "Chino"]
    nuevo_idioma = st.selectbox(
        "Selecciona el idioma / modo de juego:",
        idiomas_disponibles,
        index=idiomas_disponibles.index(st.session_state.idioma_config) if st.session_state.idioma_config in idiomas_disponibles else 0
    )
    
    nuevas_vidas = st.number_input(
        "Cantidad de vidas (Escribir entre el 3 y 20):", 
        min_value=3, 
        max_value=20, 
        value=st.session_state.vidas_config, 
        step=1
    )
    
    if st.button("Guardar configuración"):
        st.session_state.modo_config = nuevo_modo
        st.session_state.idioma_config = nuevo_idioma
        st.session_state.vidas_config = nuevas_vidas
        if "juego" in st.session_state:
            del st.session_state.juego
        if "juego_supervivencia" in st.session_state:
            del st.session_state.juego_supervivencia
        st.success(f"¡Confirmado! Modo: {nuevo_modo} | Idioma: {nuevo_idioma} | Vidas: {nuevas_vidas}.")

elif opcion == "Salir":
    st.title("¡¡¡Hasta la proximaaaaa!!!")
    st.write("Podés cerrar la pestaña sin problemas (no la de los ojos).")
    if "juego" in st.session_state:
        del st.session_state.juego
    if "juego_supervivencia" in st.session_state:
        del st.session_state.juego_supervivencia