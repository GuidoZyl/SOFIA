import subprocess
import speech_recognition as sr
import keyboard
import pyttsx3 as tts
import threading
import time
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk

def hablar(texto: str) -> None:
    engine = tts.init()
    engine.setProperty('rate', 145)
    engine.setProperty('voice', 'spanish')
    engine.say(texto)
    engine.runAndWait()

def ejecutar_app(ruta_ejecutable: str) -> None:
    subprocess.run([ruta_ejecutable])

def reproducir_audio(audio, duracion: float) -> None:
    pass

def mostrar_foto(ruta_foto: str) -> None:
    subprocess.run(['start', '', ruta_foto], shell=True)
    time.sleep(0.7)
    pyautogui.hotkey('f11')

def reproducir_cancion_spotify(nombre_cancion: str) -> None:
    ### CAMBIAR PARA QUE SEA LA RUTA DE CADA USUARIO ###
    ruta_spotify = r"C:\Users\guido\AppData\Local\Microsoft\WindowsApps\Spotify.exe"

    ejecutar_app(ruta_spotify)

    # Esperar unos segundos para que Spotify se abra completamente
    time.sleep(5)

    pyautogui.hotkey('ctrl', 'l')  # Seleccionar la barra de búsqueda
    time.sleep(1)

    # Nota: el nombre de la canción debe ser tal que la primera canción que aparezca en los resultados de búsqueda sea la que se quiere reproducir
    pyautogui.write(nombre_cancion) 
 
    time.sleep(2)  # Esperar a que se carguen los resultados de búsqueda

    ### CAMBIAR PARA QUE NO DEPENDA DE COORDENADAS ###
    # Clickear el botón de reproducir
    #pyautogui.click(x=490, y=400)

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
    # Crear una ventana de Tkinter
    ventana = tk.Tk()

    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Abrir la imagen con Pillow
    imagen = Image.open(ruta_imagen)

    # Redimensionar la imagen para que se ajuste a la pantalla
    imagen = imagen.resize((ancho_pantalla, alto_pantalla), Image.ANTIALIAS)

    # Convertir la imagen a un formato que Tkinter pueda manejar
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta en la ventana y mostrar la imagen
    etiqueta = tk.Label(ventana, image=imagen_tk)
    etiqueta.pack(fill=tk.BOTH, expand=True)

    # Configurar la ventana para que ocupe toda la pantalla
    ventana.attributes('-fullscreen', True)

    # Ocultar el cursor
    ventana.config(cursor='none')

    # Salir de la aplicación al hacer clic en la imagen
    etiqueta.bind('<Button-1>', lambda event: ventana.destroy())

    # Mostrar la ventana en primer plano
    ventana.update_idletasks()
    ventana.lift()
    ventana.attributes('-topmost', True)
    ventana.after_idle(ventana.attributes, '-topmost', False)

    # Iniciar el bucle de la interfaz gráfica de usuario
    ventana.mainloop()


if __name__ == '__main__':
    #ejecutar_app("C:\Riot Games\Riot Client\RiotClientServices.exe")
    hilo_hablar = threading.Thread(target=hablar, args=("Hola, soy tu asistente virtual, ¿en qué te puedo ayudar?",))
    hilo_hablar.start()
    reproducir_cancion_spotify("Necesito")