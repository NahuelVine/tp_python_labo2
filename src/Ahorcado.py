import random, sys
from pathlib import Path
import streamlit as st
from PIL import Image

# Aseguramos que el script apunte a la carpeta del proyecto
raiz_path = Path(__file__).resolve().parent.parent
# Assets
sys.path.append(str(raiz_path))
# Config
sys.path.append(str(raiz_path/"src"))
# Palabras
palabras_path = raiz_path/"Assets"/"Palabras"

# Configuracion y assets
from Assets import assets
import config

config.cargar_idioma()
textos_juego = assets.JUEGO_TEXTOS[st.session_state["idioma"]]
icon = raiz_path/"Assets"/"icon.png"

# Configuracion de la ventana de pagina
st.set_page_config(
    page_title=assets.VENTANA_TITULO[st.session_state["idioma"]]["titulo"],
    page_icon=Image.open(icon) if icon.exists() else "➰",
    layout="centered",
)

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
    /* BOTON DE SIDEBAR */
    [data-testid="stSidebarCollapseButton"] button span[aria-hidden="true"],
    [data-testid="stExpandSidebarButton"] span[aria-hidden="true"] {
        font-size: 0 !important;          /* oculta el texto "keyboard_double_arrow_..." */
    }
    [data-testid="stSidebarCollapseButton"] button span[aria-hidden="true"]::before,
    [data-testid="stExpandSidebarButton"] span[aria-hidden="true"]::before {
        content: "☰";
        font-size: 22px;
        line-height: 1;
        font-family: sans-serif !important;   /* Impact no tiene este símbolo */
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
        "es": (palabras_path/"Palabras_es.txt", None),
        "en": (palabras_path/"Palabras_en.txt", None),
        "kr": (palabras_path/"Palabras_kr.txt", palabras_path/"Ayudas_kr.txt"),
        "jp": (palabras_path/"Palabras_jp.txt", palabras_path/"Ayudas_jp.txt"),
        "ch": (palabras_path/"Palabras_ch.txt", palabras_path/"Ayudas_ch.txt")
    }

    palabras_file, ayuda_file = archivos.get(idioma, (palabras_path/"Palabras_es.txt", None))
    
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
    st.session_state.idioma_config = "es"
if "vidas_config" not in st.session_state:
    st.session_state.vidas_config = 6
if "modo_config" not in st.session_state:
    st.session_state.modo_config = "clasico"


st.sidebar.title(textos_juego["menu_titulo"])
opcion = st.sidebar.radio(
    textos_juego["menu_label"],
    ["jugar", "config"],                      # valores reales (no cambian con el idioma)
    format_func=lambda k: textos_juego["menu"][k],       # lo que se muestra (traducido)
)


if opcion == "jugar":
    if st.session_state.modo_config == "clasico":
        st.title(textos_juego["titulo_clasico"])
        
        palabras, ayudas = cargar_datos(st.session_state.idioma_config)
        
        if "juego" not in st.session_state or st.session_state.juego.max_intentos != st.session_state.vidas_config or len(st.session_state.juego.palabras) != len(palabras):
            st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)

        juego = st.session_state.juego

        indice_dibujo = min(len(juego.falladas), len(AHORCADO) - 1)
        st.text(AHORCADO[indice_dibujo])
        
        st.markdown(textos_juego["palabra"].format(palabra=juego.estado()))
        st.write(textos_juego["modo_idioma"].format(idioma=textos_juego["idiomas"][st.session_state.idioma_config], modo=textos_juego["modos"]["clasico"]))
        st.write(textos_juego["falladas"].format(letras=' '.join(sorted(juego.falladas)) or '-'))
        st.write(textos_juego["intentos"].format(n=juego.intentos_restantes))


        ayuda_actual = juego.ayuda_actual
        if ayuda_actual:
            st.info(textos_juego["pista"].format(idioma=textos_juego["idiomas"][st.session_state.idioma_config], ayuda=ayuda_actual))

        if juego.gano():
            st.success(textos_juego["gano"].format(palabra=juego.palabra))
            if st.button(textos_juego["btn_gano"]):
                st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
                st.rerun()
        elif juego.perdio():
            st.error(textos_juego["perdio"].format(palabra=juego.palabra))
            if st.button(textos_juego["btn_perdio"]):
                st.session_state.juego = AhorcadoLogica(palabras, ayudas, max_intentos=st.session_state.vidas_config)
                st.rerun()
        else:
            letra = st.text_input(textos_juego["input_letra"], max_chars=1, key="input_clasico")
            
            if st.button(textos_juego["btn_probar"], key="btn_clasico"):
                if letra:
                    resultado = juego.intentar(letra)
                    if resultado == "invalido":
                        st.warning(textos_juego["invalido"])
                    elif resultado == "repetida":
                        st.info(textos_juego["repetida"])
                    elif resultado == "acierto":
                        st.success(textos_juego["acierto"])
                    elif resultado == "fallo":
                        st.error(textos_juego["fallo"])
                    st.rerun()
                    
    elif st.session_state.modo_config == "supervivencia":
        st.title(textos_juego["titulo_super"])
        
        palabras, ayudas = cargar_datos(st.session_state.idioma_config)
        
        if "juego_supervivencia" not in st.session_state or st.session_state.juego_supervivencia.max_vidas != st.session_state.vidas_config or len(st.session_state.juego_supervivencia.palabras) != len(palabras):
            st.session_state.juego_supervivencia = AhorcadoSupervivencia(palabras, ayudas, max_vidas=st.session_state.vidas_config)

        juego = st.session_state.juego_supervivencia

        intentos_fallidos = juego.max_vidas - juego.vidas_restantes
        indice_dibujo = min(int((intentos_fallidos / juego.max_vidas) * (len(AHORCADO) - 1)), len(AHORCADO) - 1)
        st.text(AHORCADO[indice_dibujo])
        
        st.markdown(textos_juego["palabra"].format(palabra=juego.estado()))
        st.markdown(textos_juego["super_racha"].format(n=juego.palabras_adivinadas))
        st.write(textos_juego["modo_idioma"].format(idioma=textos_juego["idiomas"][st.session_state.idioma_config],modo=textos_juego["modos"]["supervivencia"]))
        st.write(textos_juego["super_falladas"].format(letras=' '.join(sorted(juego.falladas_palabra)) or '-'))
        st.write(textos_juego["super_vidas"].format(vidas=juego.vidas_restantes,max=juego.max_vidas))

        ayuda_actual = juego.ayuda_actual
        if ayuda_actual:
            st.info(textos_juego["pista"].format(idioma=textos_juego["idiomas"][st.session_state.idioma_config], ayuda=ayuda_actual))

        if juego.perdio():
            st.error(textos_juego["super_perdio"].format(n=juego.palabras_adivinadas))
            if st.button(textos_juego["super_reintentar"]):
                st.session_state.juego_supervivencia = AhorcadoSupervivencia(palabras, ayudas, max_vidas=st.session_state.vidas_config)
                st.rerun()
        else:
            if juego.gano():
                st.success(textos_juego["super_gano"].format(palabra=juego.palabra))
                juego.siguiente_palabra()
                st.rerun()
            else:
                letra = st.text_input(textos_juego["input_letra"], max_chars=1, key="input_supervivencia")
                
                if st.button(textos_juego["btn_probar"], key="btn_supervivencia"):
                    if letra:
                        resultado = juego.intentar(letra)
                        if resultado == "invalido":
                            st.warning(textos_juego["invalido"])
                        elif resultado == "repetida":
                            st.info(textos_juego["repetida"])
                        elif resultado == "acierto":
                            st.success(textos_juego["acierto"])
                        elif resultado == "fallo":
                            st.error(textos_juego["super_fallo"])
                        st.rerun()

else:
    st.title(textos_juego["cfg_titulo"])
    st.write(textos_juego["cfg_desc"])
    
    modos_disponibles = ["clasico", "supervivencia"]
    nuevo_modo = st.selectbox(
        textos_juego["cfg_modo"],
        modos_disponibles,
        index=modos_disponibles.index(st.session_state.modo_config) if st.session_state.modo_config in modos_disponibles else 0,
        format_func=textos_juego["modos"].get
    )
    
    idiomas_disponibles = ["es", "en", "kr", "jp", "ch"]
    nuevo_idioma = st.selectbox(
        textos_juego["cfg_idioma"],
        idiomas_disponibles,
        index=idiomas_disponibles.index(st.session_state.idioma_config) if st.session_state.idioma_config in idiomas_disponibles else 0,
        format_func=textos_juego["idiomas"].get
    )
    
    nuevas_vidas = st.number_input(
        textos_juego["cfg_vidas"], 
        min_value=3, 
        max_value=20, 
        value=st.session_state.vidas_config, 
        step=1
    )
    
    if st.button(textos_juego["cfg_guardar"]):
        st.session_state.modo_config = nuevo_modo
        st.session_state.idioma_config = nuevo_idioma
        st.session_state.vidas_config = nuevas_vidas
        if "juego" in st.session_state:
            del st.session_state.juego
        if "juego_supervivencia" in st.session_state:
            del st.session_state.juego_supervivencia
        st.success(textos_juego["cfg_ok"].format(modo=textos_juego["modos"][nuevo_modo],idioma=textos_juego["idiomas"][nuevo_idioma],vidas=nuevas_vidas))