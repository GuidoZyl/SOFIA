"Archivo main"

import json
import threading
import os
import keyboard
import subprocess
import psutil
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image
import funciones as fn

Instruccion = list[list[str]]

teclas_presionadas = set()
ejecutando = False

# Cargar la configuración
def cargar_configuracion():
    """Carga la configuración desde el archivo json."""
    with open("prueba_config2.json", "r", encoding="utf-8") as archivo:
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
        if funcion == "Hablar":
            try:
                fn.hablar(parametros)
            except:
                pass

        elif funcion == "Ejecutar App":
            fn.ejecutar_app(parametros)

        elif funcion == "Reproducir audio":
            fn.reproducir_audio(parametros[0], parametros[1])

        elif funcion == "Reproducir Spotify":
            fn.reproducir_cancion_spotify(parametros)

        elif funcion == "Mostrar foto":
            fn.abrir_imagen(parametros)

    ejecutando = False

def on_key_event(e, conf):
    """Se ejecuta al presionar una tecla"""
    if ejecutando or cli_esta_abierto: # Si ya se está ejecutando un comando o está abierta la CLI, no se ejecuta otro
        return

    if e.event_type == keyboard.KEY_DOWN:
        print(e.name)
        if e.name not in teclas_presionadas:
            #teclas_presionadas.add(e.name)
            if e.name in conf.get('comandos', {}):
                instruccion = conf['comandos'][e.name]
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

cli_proceso = None
cli_esta_abierto = False
def abrir_cli():
    global cli_proceso
    global cli_esta_abierto

    if not cli_esta_abierto:
        cli_proceso = subprocess.Popen('start "Comandos - SOFIA" cmd.exe /k "abrir_cli.bat"', shell=True) 
        cli_esta_abierto = True
        checkear_cli = threading.Thread(target=checkear_cli_en_ejecucion)
        checkear_cli.start()

def cli_en_ejecucion() -> bool:
    """Verifica si está abierto el CMD que ejecuta el CLI"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'cmd.exe' in proc.info['name'] and 'abrir_cli.bat' in proc.cmdline():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def checkear_cli_en_ejecucion():
    global cli_esta_abierto
    while cli_esta_abierto:
        time.sleep(2)       
        if not cli_en_ejecucion():
            cli_esta_abierto = False

def on_exit(icon):
    """Cierra el programa."""
    icon.stop()

    # Cierra la CLI en caso de estar abierta
    if cli_esta_abierto:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] == 'cmd.exe' and 'abrir_cli.bat' in proc.cmdline():
                os.system(f'taskkill /PID {proc.info["pid"]} /T /F')
                break
 

    despedida = threading.Thread(target=fn.hablar, args=("Hasta luego",))
    despedida.start()
    despedida.join()

    # El comando para cerrar el programa está en configurar_icono() para evitar bugs
    #sys.exit()

def configurar_icono():
    """Configura el ícono en la barra de tareas."""
    image = Image.open(r"E:\Guido\Descargas\icon-512x512.png")

    menu = Menu(
        MenuItem('Modificar comandos', abrir_cli),
        Menu.SEPARATOR,
        MenuItem('Salir', on_exit)
        )
        

    icon = Icon("SOFIA", image, "SOFIA", menu=menu)
    icon.run()
    os._exit(0)

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
