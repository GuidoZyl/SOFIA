import json
import keyboard
import threading
from funciones import hablar, ejecutar_app, reproducir_audio

Instruccion = list[list[str]]

teclas_presionadas = set()
ejecutando = False


# Cargar la configuración
def cargar_configuracion():
    with open("config.json", "r", encoding="utf-8") as archivo:
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
    
    ejecutando = False

# Se ejecuta al presionar una tecla
def on_key_event(e, conf):
    global ejecutando
    if ejecutando: # Si ya se está ejecutando un comando, no se ejecuta otro
        return
    
    if e.event_type == keyboard.KEY_DOWN:
        if e.name not in teclas_presionadas:
            teclas_presionadas.add(e.name)
            if e.name in conf.get('config', {}):
                print(conf['config'][e.name])
                try:
                    # Se crea un hilo para salir del hook de keyboard
                    hilo_ejecutar = threading.Thread(target=ejecutar_comando, args=(conf['config'][e.name][0], conf['config'][e.name][1],))
                    hilo_ejecutar.start()
                except:
                    print("Espera un momento, ya se está ejecutando un comando")

    # Evita que se ejecute el comando varias veces si se mantiene presionada la tecla
    elif e.event_type == keyboard.KEY_UP:
        if e.name in teclas_presionadas:
            teclas_presionadas.remove(e.name)

def main():
    global config

    print(config)

    keyboard.hook(lambda e: on_key_event(e, config))
    keyboard.wait()

if __name__ == '__main__':
    #ejecutar_comando(["hablar", "hablar"], ["Hola, buen día", "Chau, buenas tardes"])
    main()