import subprocess
import speech_recognition as sr
import keyboard
import pyttsx3 as tts
import threading
import time
import pyautogui

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
    pyautogui.click(x=490, y=400)

if __name__ == '__main__':
    #ejecutar_app("C:\Riot Games\Riot Client\RiotClientServices.exe")
    hilo_hablar = threading.Thread(target=hablar, args=("Hola, soy tu asistente virtual, ¿en qué te puedo ayudar?",))
    hilo_hablar.start()
    reproducir_cancion_spotify("Necesito")