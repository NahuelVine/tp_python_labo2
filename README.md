# Ahorcado: Adivina la palabra

## Repositorio para el proyecto de Python: Ahorcado

### Desarrolladores

- Nahuel Iovine
- Marcos Zurita Tropea

### Descripcion

Juego del ahorcado creado en Python, donde se tendrá que descubrir la palabra secreta.
El juego tendrá soporte multilingüe, para seleccionar el idioma preferido.
Se almacenan las palabras en archivos .txt, y si es un idioma asiatico, contara con una ayuda para descubrir.
Por el lado del idioma de interfaz, los estaremos almacenando en el navegador como cookie de forma local para cada usuario, para que se mantenga entre sesiones.

### Diagramas

- [Diagrama de flujo](https://www.figma.com/board/AJw4LHpZxG0cLZvB0lLh7a/Python--Ahorcado---DdF?node-id=0-1&p=f&t=nl4ETWnoer0KStWP-0)
- [Componentes](https://www.figma.com/design/OzTVKNx9EzMjHEE3mPloyz/Python--Ahorcado---Componentes?node-id=0-1&p=f&m=draw)

### Librerias externas

- [streamlit](https://docs.streamlit.io/)
- [pillow](https://pypi.org/project/pillow/)

### Instalacion

1. Abrimos una terminal en la ruta del proyecto
2. Creamos un entorno virtual con el comando `python -m venv venv`
3. Iniciamos el entorno virtual con el comando `venv\Scripts\activate`
4. Instalamos las librerias necesarias con `python -m pip install -r requirements.txt`

### Ejecucion

- Ejecutamos la app con `streamlit run src/main.py` de forma local.
- Ingresamos a la [url del proyecto](https://tppythonlabo2-cz5yp8yfklqbr5qmhrwrba.streamlit.app/) hosteado por streamlit.
