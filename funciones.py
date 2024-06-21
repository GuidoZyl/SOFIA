"""
Funciones del asistente virtual
"""
import subprocess
import threading
import time
import tkinter as tk
#import keyboard
import pyttsx3 as tts
import pyautogui
#import speech_recognition as sr
from PIL import Image, ImageTk
#from pydub import AudioSegment
#from pydub.playback import play
import json

def hablar(texto: str) -> None:
    """Utiliza el text to speech para decir un texto."""
    engine = tts.init()
    engine.setProperty('rate', 145)
    engine.setProperty('voice', 'spanish')
    engine.say(texto)
    engine.runAndWait()

def ejecutar_app(ruta_ejecutable: str) -> None:
    """Abre la aplicación especificada."""
    subprocess.run([ruta_ejecutable], check=False)

def reproducir_audio(audio, duracion: float) -> None:
    """Reproduce un audio"""
    pass

def reproducir_cancion_spotify(nombre_cancion: str) -> None:
    """Reproduce la canción especificada en Spotify."""
    ### CAMBIAR PARA QUE SEA LA RUTA DE CADA USUARIO ###
    ruta_spotify = r"C:\Users\guido\AppData\Local\Microsoft\WindowsApps\Spotify.exe"

    ejecutar_app(ruta_spotify)

    # Esperar unos segundos para que Spotify se abra completamente
    time.sleep(5)

    pyautogui.hotkey('ctrl', 'l')  # Seleccionar la barra de búsqueda
    time.sleep(1)

    # Nota: el nombre de la canción debe ser tal que la primera canción que aparezca en
    # los resultados de búsqueda sea la que se quiere reproducir
    pyautogui.write(nombre_cancion)

    time.sleep(2)  # Esperar a que se carguen los resultados de búsqueda

    # Seleccionar el botón de reproducir
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(0.8)
    pyautogui.press('enter')

def abrir_imagen(ruta_imagen: str) -> None:
    """Abre la imagen de la ruta especificada en pantalla completa. Se cierra al hacer click."""
    ventana = tk.Tk()
    imagen = Image.open(ruta_imagen)

    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Redimensionar la imagen para cubrir toda la pantalla
    imagen = imagen.resize((ancho_pantalla, alto_pantalla), Image.ANTIALIAS)

    # Convertir la imagen a un formato que Tkinter pueda manejar
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta en la ventana y mostrar la imagen
    etiqueta = tk.Label(ventana, image=imagen_tk)
    etiqueta.pack(fill=tk.BOTH, expand=True)

    ventana.attributes('-fullscreen', True)

    # Ocultar el cursor
    ventana.config(cursor='none')

    # Salir de la aplicación al hacer click
    etiqueta.bind('<Button-1>', lambda event: ventana.destroy())

    # Mostrar la ventana en primer plano
    ventana.update_idletasks()
    ventana.lift()
    ventana.attributes('-topmost', True)
    ventana.after_idle(ventana.attributes, '-topmost', False)

    ventana.mainloop()

def agregar_comando(tecla: str) -> None:
    """Agrega un comando al JSON"""
    with open("prueba_config.json", "r+", encoding="utf-8") as archivo:
        config = json.load(archivo)

if __name__ == '__main__':
    #ejecutar_app("C:\Riot Games\Riot Client\RiotClientServices.exe")
    hilo_hablar = threading.Thread(target=hablar, args=("Hola, soy tu asistente virtual",))
    hilo_hablar.start()
    reproducir_cancion_spotify("Necesito")
