# Aseguramos que el script apunte a la carpeta del proyecto
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Libreria GUI
from tkinter import *
#Libreriamos custom de configuracion
from Assets import assets
import config

# Cargamos configuracion
configuracion = config.cargar()
idioma = configuracion["idioma"]
# Root de la ventana
root = Tk()
# Configuracion de ventana principal
root.title(assets.VENTANA_TITULO[idioma]["titulo"])
root.config(bg=assets.VENTANA_BG)
root.geometry(configuracion["tamano"])
# Bloqueamos el ratio de tamaño
root.resizable(False, False)

# Creamos titulo menu
lbl = Label(root, text = assets.MENU_TITULO)
# Mostramos titulo
lbl.grid()

# Funcion boton jugar
def seleccionJugar():
    lbl.configure(text = assets.BOTON_TEXTOS[idioma]["lbl_jugar"])
# Funcion boton configuracion
def seleccionConfiguracion():
    lbl.configure(text = assets.BOTON_TEXTOS[idioma]["lbl_config"])

# Crear botones
btn_jugar = Button(root, text = assets.BOTON_TEXTOS[idioma]["btn_jugar"], command=seleccionJugar)
btn_config = Button(root, text = assets.BOTON_TEXTOS[idioma]["btn_config"], command=seleccionConfiguracion)
btn_salir = Button(root, text = assets.BOTON_TEXTOS[idioma]["btn_salir"], command=root.destroy)
# Mostrar botones
btn_jugar.grid(column=0, row=1)
btn_config.grid(column=0, row=2)
btn_salir.grid(column=0, row=3)

# Ejecuta libreria Tkinter
# Siempre al final
root.mainloop()