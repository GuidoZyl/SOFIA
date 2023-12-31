"Archivo main"

import json
import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image
import funciones as fn

Instruccion = list[list[str]]

teclas_presionadas = set()
ejecutando = False

# Cargar la configuración
def cargar_configuracion():
    """Carga la configuración desde el archivo json."""
    with open("prueba_config.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

config = cargar_configuracion()

# Decorador que recibe dos listas y las une para pasarlas a main()
def unir_listas(func):
    """Recibe dos listas y las une para pasarlas a main()"""
    def wrapper(funciones, parametros):
        instrucciones = [[funciones[i], parametros[i]] for i in range(len(funciones))]
        return func(instrucciones)
    return wrapper

@unir_listas
def ejecutar_comando(instrucciones: Instruccion) -> None:
    """Ejecuta el comando especificado."""
    global ejecutando
    if ejecutando: # Si ya se está ejecutando un comando, no se ejecuta otro
        return

    ejecutando = True

    for funcion, parametros in instrucciones:
        if funcion == "hablar":
            try:
                fn.hablar(parametros)
            except:
                pass

        elif funcion == "ejecutar_app":
            fn.ejecutar_app(parametros)

        elif funcion == "reproducir_audio":
            fn.reproducir_audio(parametros[0], parametros[1])

        elif funcion == "reproducir_spotify":
            fn.reproducir_cancion_spotify(parametros)

        elif funcion == "mostrar_foto":
            fn.abrir_imagen(parametros)

    ejecutando = False

# Se ejecuta al presionar una tecla
def on_key_event(e, conf):
    """Se ejecuta al presionar una tecla"""
    if ejecutando: # Si ya se está ejecutando un comando, no se ejecuta otro
        return

    if e.event_type == keyboard.KEY_DOWN:
        print(e.name)
        if e.name not in teclas_presionadas:
            #teclas_presionadas.add(e.name)
            if e.name in conf.get('config', {}):
                instruccion = conf['config'][e.name]
                print(instruccion)
                try:
                    # Se crea un hilo para salir del hook de keyboard
                    hilo_ejecutar = threading.Thread(target=ejecutar_comando,
                                                     args=(instruccion[0], instruccion[1],))
                    hilo_ejecutar.start()
                except:
                    print("Espera un momento, ya se está ejecutando un comando")

    # Evita que se ejecute el comando varias veces si se mantiene presionada la tecla
    # elif e.event_type == keyboard.KEY_UP:
    #     if e.name in teclas_presionadas:
    #         teclas_presionadas.remove(e.name)


def on_exit(icon):
    """Cierra el programa."""
    icon.stop()
    despedida = threading.Thread(target=fn.hablar, args=("Hasta luego",))
    despedida.start()
    despedida.join()
    os._exit(0)
    #sys.exit()


def configurar_icono():
    """Configura el ícono en la barra de tareas."""
    image = Image.open(r"E:\Guido\Descargas\icon-512x512.png")

    menu = (Menu(MenuItem('Salir', on_exit),))

    icon = Icon("SOFIA", image, "SOFIA", menu=menu)
    icon.run()
    print("Saliendo...")
    return sys.exit()

def main():
    """Función principal del programa. Escucha eventos de teclado y 
    realiza las configuraciones iniciales"""
    print(config)

    icono_thread = threading.Thread(target=configurar_icono)
    icono_thread.start()

    keyboard.hook(lambda e: on_key_event(e, config))
    keyboard.wait()

if __name__ == '__main__':
    #ejecutar_comando(["hablar", "hablar"], ["Hola, buen día", "Chau, buenas tardes"])
    main()
