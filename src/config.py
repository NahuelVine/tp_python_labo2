import os
# Nos aseguramos que el siempre busque el archivo en la direccion del proyecto
from pathlib import Path
archivo =  Path(__file__).parent / "config.txt"
default = {"idioma": "es", "tamano": "640x800"}

def cargar():
    config = default.copy()
    # Nos aseguramos que el archivo a buscar exista, sino, usamos los valores predeterminados
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="UTF-8") as file:
            for linea in file:
                if "=" in linea:
                    key, valor = linea.strip().split("=", 1)
                    if key in config:
                        config[key] = valor
    return config

def guardar(config):
    with open(archivo, "w", encoding="UTF-8") as file:
        for key, valor in config.items():
            file.write(f"{key}={valor}\n")