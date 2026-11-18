# VENTANA
VENTANA_TITULO = {
    "es": {
        "titulo": "Ahorcado: Adivina la palabra",
    },
    "en": {
        "titulo": "Hangman: Guess the word"
    }
}
VENTANA_BG = "#570F1C"
MENU_ENCABEZADO = {"es": "TU PRÓXIMA MALA IDEA", "en": "YOUR NEXT BAD IDEA"}
MENU_TARJETAS = {
    "es": {"jugar": "Descubre la palabra, si puedes.", "idioma": "Todo bajo control. Casi."},
    "en": {"jugar": "Discover the word, if you can.", "idioma": "Everything under control. Almost."},
}
# BOTON
BOTON_ANCHO = 360
BOTON_ALTO = 105
BOTON_SEPARACION = 25
BOTON_COLOR = "#B8B8B8"
BOTON_TEXTOS = {
    "es": {
        "btn_jugar": "Jugar",
        "lbl_jugar": "Jugar fue seleccionado",
        "btn_idioma": "Idioma",
        "lbl_idioma": "Idioma cambiado a español"
    },
    "en": {
        "btn_jugar": "Play",
        "lbl_jugar": "Play was selected",
        "btn_idioma": "Language",
        "lbl_idioma": "Language changed to english"
    }
}
# MENU
TITULO = {
    "es": {"genero": "EL CLÁSICO DE PALABRAS. CON CERO PIEDAD.", "nombre": "AHORCADO",
           "promesa": "Una letra menos. Un problema más."},
    "en": {"genero": "THE WORD CLASSIC. NO MERCY.", "nombre": "HANGMAN",
           "promesa": "One letter less. One more problem."},
}
VERSION = "v1.0"
FOOTER = {
    "es": {"creditos": "Realizado por Nahuel Iovine y Marcos Zurita Tropea", "idioma": "ESPAÑOL"},
    "en": {"creditos": "Made by Nahuel Iovine and Marcos Zurita Tropea", "idioma": "ENGLISH"},
}
# Juego
JUEGO_TEXTOS = {
    "es": {
        "menu_titulo": "📌 Menú Principal",
        "menu_label": "Selecciona una opción:",
        "menu": {"jugar": "Jugar", "config": "Configuración"},
        "volver": "⬅ Volver al menú principal",
        "modos": {"clasico": "Clásico", "supervivencia": "Supervivencia"},
        "idiomas": {"es": "Español", "en": "Inglés", "kr": "Coreano", "jp": "Japonés", "ch": "Chino"},
        # General
        "titulo_clasico": "AHORCADO, la película, solo en Labo 2",
        "titulo_super": "🔥 AHORCADO: MODO SUPERVIVENCIA 🔥",
        "palabra": "### Palabra: `{palabra}`",
        "modo_idioma": "**Modo / Idioma:** {idioma} ({modo})",
        "pista": "💡 **Etimología / Pista ({idioma}):**\n\n{ayuda}",
        "input_letra": "Ingresa una letra:",
        "btn_probar": "Ver si está en la palabra.",
        "invalido": "No podés con esa letra.",
        "repetida": "Ya usaste la letra...",
        "acierto": "✅ CORRECTO ✅",
        # Clásico
        "falladas": "**Falladas:** {letras}",
        "intentos": "**Intentos restantes:** {n}",
        "fallo": "❌ EPIC FAIL ❌",
        "gano": "🎉 ¡GRANDE! Le pegaste a la palabra, la cual por cierto era: {palabra}",
        "perdio": "Una pena, perdiste. La palabra era: {palabra}",
        "btn_gano": "¿Querés volver a jugar?",
        "btn_perdio": "Por favor, volvé a jugar así te superás a vos mismo.",
        # Supervivencia
        "super_racha": "🏆 **Palabras adivinadas en la sesión:** `{n}`",
        "super_falladas": "**Letras falladas en esta palabra:** {letras}",
        "super_vidas": "❤️ **Vidas restantes (Globales):** {vidas} / {max}",
        "super_fallo": "❌ ¡VIDA GLOBAL PERDIDA! ❌",
        "super_gano": "🎉 ¡PALABRA SUPERADA! Era: **{palabra}**. Pasando a la siguiente...",
        "super_perdio": "💀 ¡SE ACABÓ EL JUEGO! Te quedaste sin vidas. Lograste adivinar **{n}** palabras. ¡JAAAAA!",
        "super_reintentar": "🔄 Volver a intentar Supervivencia",
        # Configuración
        "cfg_titulo": "⚙️ CONFIGURACIÓN ⚙️",
        "cfg_desc": "Cambiar parámetros de la partida.",
        "cfg_modo": "Selecciona el modo de juego:",
        "cfg_idioma": "Selecciona el idioma de las palabras:",
        "cfg_vidas": "Cantidad de vidas (Escribir entre el 3 y 20):",
        "cfg_guardar": "Guardar configuración",
        "cfg_ok": "¡Confirmado! Modo: {modo} | Idioma: {idioma} | Vidas: {vidas}.",
    },
    "en": {
        "menu_titulo": "📌 Main Menu",
        "menu_label": "Select an option:",
        "menu": {"jugar": "Play", "config": "Settings"},
        "volver": "⬅ Back to main menu",
        "modos": {"clasico": "Classic", "supervivencia": "Survival"},
        "idiomas": {"es": "Spanish", "en": "English", "kr": "Korean", "jp": "Japanese", "ch": "Chinese"},
        "titulo_clasico": "HANGMAN, the movie, only in Lab 2",
        "titulo_super": "🔥 HANGMAN: SURVIVAL MODE 🔥",
        "palabra": "### Word: `{palabra}`",
        "modo_idioma": "**Mode / Language:** {idioma} ({modo})",
        "pista": "💡 **Etymology / Hint ({idioma}):**\n\n{ayuda}",
        "input_letra": "Enter a letter:",
        "btn_probar": "Check if it's in the word.",
        "invalido": "You can't use that letter.",
        "repetida": "You already used that letter...",
        "acierto": "✅ CORRECT ✅",
        "falladas": "**Missed:** {letras}",
        "intentos": "**Attempts left:** {n}",
        "fallo": "❌ EPIC FAIL ❌",
        "gano": "🎉 NICE! You nailed the word, which by the way was: {palabra}",
        "perdio": "Too bad, you lost. The word was: {palabra}",
        "btn_gano": "Want to play again?",
        "btn_perdio": "Please play again so you can beat yourself.",
        "super_racha": "🏆 **Words guessed this session:** `{n}`",
        "super_falladas": "**Letters missed in this word:** {letras}",
        "super_vidas": "❤️ **Lives left (Global):** {vidas} / {max}",
        "super_fallo": "❌ GLOBAL LIFE LOST! ❌",
        "super_gano": "🎉 WORD CLEARED! It was: **{palabra}**. Moving on to the next one...",
        "super_perdio": "💀 GAME OVER! You ran out of lives. You guessed **{n}** words. HAHAHA!",
        "super_reintentar": "🔄 Try Survival again",
        "cfg_titulo": "⚙️ SETTINGS ⚙️",
        "cfg_desc": "Change the game parameters.",
        "cfg_modo": "Select the game mode:",
        "cfg_idioma": "Select the language of the words:",
        "cfg_vidas": "Number of lives (enter a value from 3 to 20):",
        "cfg_guardar": "Save settings",
        "cfg_ok": "Confirmed! Mode: {modo} | Language: {idioma} | Lives: {vidas}.",
    },
}