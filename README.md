# Ahorcado: Adivina la palabra

## Repositorio para el proyecto de Python: Ahorcado

### Descripcion

Juego del ahorcado creado en Python, donde se tendrá que descubrir la palabra secreta.
El juego tendrá soporte multilingüe, para seleccionar el idioma preferido.
Se almacenan todos los datos principales de gameplay dentro de archivos binarios ".dat", con la idea de que el jugador no pueda hacer trampa.
Por el lado de la configuración, los estaremos almacenando dentro de un archivo ".txt".

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
5. Ejecutamos la app con `pstreamlit run src/main.py`
