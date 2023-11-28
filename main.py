import json
import keyboard
import threading
import os
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
from funciones import hablar, ejecutar_app, reproducir_audio, reproducir_cancion_spotify, abrir_imagen

Instruccion = list[list[str]]

teclas_presionadas = set()
ejecutando = False

# Cargar la configuración
def cargar_configuracion():
    with open("prueba_config.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
config = cargar_configuracion()

# Decorador que recibe dos listas y las une para pasarlas a main()
def unir_listas(func):
    def wrapper(funciones, parametros):
        instrucciones = [[funciones[i], parametros[i]] for i in range(len(funciones))]
        return func(instrucciones)
    return wrapper

@unir_listas
def ejecutar_comando(instrucciones: Instruccion) -> None:
    global ejecutando
    if ejecutando: # Si ya se está ejecutando un comando, no se ejecuta otro
        return

    ejecutando = True

    for funcion, parametros in instrucciones:
        if funcion == "hablar":
            try:
                hablar(parametros)
            except:
                pass

        elif funcion == "ejecutar_app":
            ejecutar_app(parametros)

        elif funcion == "reproducir_audio":
            reproducir_audio(parametros[0], parametros[1])

        elif funcion == "reproducir_spotify":
            reproducir_cancion_spotify(parametros)

        elif funcion == "mostrar_foto":
            abrir_imagen(parametros)
    
    ejecutando = False

# Se ejecuta al presionar una tecla
def on_key_event(e, conf):
    global ejecutando
    if ejecutando: # Si ya se está ejecutando un comando, no se ejecuta otro
        return
    
    if e.event_type == keyboard.KEY_DOWN:
        print(e.name)
        if e.name not in teclas_presionadas:
            #teclas_presionadas.add(e.name)
            if e.name in conf.get('config', {}):
                print(conf['config'][e.name])
                try:
                    # Se crea un hilo para salir del hook de keyboard
                    hilo_ejecutar = threading.Thread(target=ejecutar_comando, args=(conf['config'][e.name][0], conf['config'][e.name][1],))
                    hilo_ejecutar.start()
                except:
                    print("Espera un momento, ya se está ejecutando un comando")

    # Evita que se ejecute el comando varias veces si se mantiene presionada la tecla
    # elif e.event_type == keyboard.KEY_UP:
    #     if e.name in teclas_presionadas:
    #         teclas_presionadas.remove(e.name)


def on_exit(icon, item):
    icon.stop()
    despedida = threading.Thread(target=hablar, args=("Hasta luego",))
    despedida.start()
    despedida.join()
    os._exit(0) 
    #sys.exit()


def configurar_icono():
    image = Image.open(r"E:\Guido\Descargas\icon-512x512.png")

    menu = (Menu(MenuItem('Salir', on_exit),))

    icon = Icon("SOFIA", image, "SOFIA", menu=menu)
    icon.run()
    print("Saliendo...")
    return sys.exit()

def main():
    global config

    print(config)

    icono_thread = threading.Thread(target=configurar_icono)
    icono_thread.start()

    keyboard.hook(lambda e: on_key_event(e, config))
    keyboard.wait()

if __name__ == '__main__':
    #ejecutar_comando(["hablar", "hablar"], ["Hola, buen día", "Chau, buenas tardes"])
    main()