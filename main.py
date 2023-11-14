import subprocess
import speech_recognition as sr
import keyboard
import pyttsx3 as tts
import threading
from prueba_spoti import reproducir_cancion_en_spotify

recognizer = sr.Recognizer()

def hablar(texto):
    engine = tts.init()
    engine.setProperty('rate', 145)
    engine.setProperty('voice', 'spanish')
    engine.say(texto)
    engine.runAndWait()

def ejecutar_comando(comando):
    if "sexo activado" in comando:      
        texto = "Modo sexo: activado"

        # Se crean dos hilos para que se ejecute el text to speech y el comando de spotify al mismo tiempo
        hilo_hablar = threading.Thread(target=hablar, args=(texto,))
        hilo_hablar.start()

        hilo_spotify = threading.Thread(target=reproducir_cancion_en_spotify, args=("Azote",))
        hilo_spotify.start()

        # Se espera a que terminen los hilos
        hilo_hablar.join()
        hilo_spotify.join()
        
        # Abre el League of Legends
        subprocess.run([r"C:\Riot Games\Riot Client\RiotClientServices.exe"])

    elif "alerta de intruso" in comando:
        texto = ""
        for _ in range(1000):
            texto += "Alerta de intruso "


    

def escuchar_comando():
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language='es-ES')
        print("Comando: " + comando)
        ejecutar_comando(comando)
    except sr.UnknownValueError:
        print("No se ha entendido el comando")
    except sr.RequestError as e:       
        print("No se ha podido obtener el resultado; {0}".format(e))

def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'f8':
        print('F8 pressed')
        escuchar_comando()

# Registra la función de manejo de eventos
keyboard.hook(on_key_event)

# Lo mantiene abierto
keyboard.wait('esc')