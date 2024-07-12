import json
import os
import keyboard
import threading


def cargar_comandos():
    with open("prueba_config2.json", "r", encoding="utf-8") as archivo:
        comandos = json.load(archivo)["comandos"]
    return comandos

def limpiar_entrada():
    """Limpia la entrada de texto en la consola."""
    def empezar_limpieza():
        """Simula presionar Ctrl + A y Supr para limpiar la entrada."""
        import pyautogui
        import time
        time.sleep(0.005)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.press('backspace')

    import termios
    import sys
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    thread = threading.Thread(target=empezar_limpieza)
    thread.start()

def mostrar_comandos():
    config = cargar_comandos()
    for clave in config:
        texto_a_mostrar = f"{config[clave][2]} ({clave}) - "
        for i in range(len(config[clave][0])):
            valor = config[clave][1][i]
            comando = config[clave][0][i]
            if comando in ["Hablar", "Reproducir Spotify"]:
                valor = "'" + valor + "'"
            texto_a_mostrar += f"{comando}: {valor}, "
        texto_a_mostrar = texto_a_mostrar[:-2]
        print(texto_a_mostrar)
    print("") # Espacio vacío para que no se pegue con el selector de opciones

def escuchar_tecla():
    # while True:  # POR AHORA LEER EL TECLADO ESTÁ SUSPENDIDO POR PROVOCAR BUGS
    #     event = keyboard.read_event()
    #     if event.event_type == keyboard.KEY_DOWN:
    #         return event.name
    return input()

def editar_comandos(tecla):
    os.system('cls')
    comando_a_editar = cargar_comandos()[tecla]
    print(f"Comando a editar: {comando_a_editar[2]} ({tecla})\n")
    texto_a_mostrar = ""
    for i in range(len(comando_a_editar[0])):
        valor = comando_a_editar[1][i]
        comando = comando_a_editar[0][i]
        if comando in ["Hablar", "Reproducir Spotify"]:
            valor = "'" + valor + "'"
        texto_a_mostrar += f"{comando}: {valor}, "
    print(texto_a_mostrar[:-2])

    while True:  
        try:
            accion = int(input("Elija una opción\n1. Agregar instrucción  2. Eliminar instrucción  3. Cambiar nombre  4. Cambiar tecla\n"))       
        except:
            os.system('cls')
            print("Ingrese una opción válida.\n")
            continue

        # Agregar instrucción
        if accion == 1:
            os.system('cls')
            print("Elija en qué posición agregar la instrucción:\n")
            for i in range(len(comando_a_editar[0])):
                print(f"{i + 1}. {comando_a_editar[0][i]}: {comando_a_editar[1][i]}")
            
            while True:
                try:
                    posicion = int(input())
                    if posicion < 1 or posicion > len(comando_a_editar[0]) + 1:
                        os.system('cls')
                        print("Ingrese una opción válida.\n")
                    else:
                        break
                except:
                    os.system('cls')
                    print("Ingrese una opción válida.\n")
            
            os.system('cls')
            print("Elija la instrucción a agregar:\n")
            print("1. Hablar  2. Reproducir Spotify 3. Mostrar foto 4. Reproducir audio\n")
            while True:
                try:
                    instruccion = int(input())
                    if instruccion < 1 or instruccion > 4:
                        os.system('cls')
                        print("Ingrese una opción válida.\n")
                    else:
                        break
                except:
                    os.system('cls')
                    print("Ingrese una opción válida.\n")
            
            if instruccion == 1:
                valor = input("Ingrese el texto a hablar: ")
            elif instruccion == 2:
                valor = input("Ingrese el nombre de la canción: ")
            elif instruccion == 3:
                valor = input("Ingrese la ruta de la imagen: ")
            elif instruccion == 4:
                pass
            
        # Eliminar instrucción
        elif accion == 2:
            pass
        # Cambiar nombre
        elif accion == 3:
            pass
        # Cambiar tecla
        elif accion == 4:
            pass
        else:
            os.system('cls')
            print("Ingrese una opción válida.\n")

while True:  
    try:
        accion = int(input("Elija una opción (o cierre esta ventana para continuar)\n1. Ver comandos  2. Editar comando  3. Agregar comando  4. Eliminar comando\n"))       
    except:
        os.system('cls')
        print("Ingrese una opción válida.\n")
        continue
    # Ver comandos
    if accion == 1:
        os.system('cls')
        print("Lista de comandos:\n")
        mostrar_comandos()
    # Editar comando
    elif accion == 2:
        try: # A veces tira error y no sé por qué
            os.system('cls')
            print("Comandos disponibles:\n")
            mostrar_comandos()
            comandos = cargar_comandos()
            tecla_elegida = False
            sale = False
            tecla = ""
            while not tecla_elegida:    
                print("Escriba la tecla a editar (o 'c' para cancelar): ")
                tecla = escuchar_tecla()
                if tecla == "c":
                    sale = True
                    os.system('cls')
                    #limpiar_entrada()
                    break
                if tecla not in comandos:
                    print("No existe ese comando, ¿desea agregarlo? (S/N): ")
                    # MANDAR A LA FUNCION DE AGREGAR COMANDO EN CASO DE "SI"
                else:
                    #limpiar_entrada()
                    opcion = input(f"¿Quiere editar la tecla '{tecla}'? (S/N): ")
                    while opcion not in ["S", "s", "N", "n"]:
                        print("Ingrese una opción válida.")
                        #limpiar_entrada()
                        opcion = input(f"¿Quiere editar la tecla '{tecla}'? (S/N): ")
                    if opcion in ["S", "s"]:
                        tecla_elegida = True
                    else:
                        os.system('cls')
                        print("Comandos disponibles:\n")
                        mostrar_comandos()
            if not sale:
                editar_comandos(tecla)
        except Exception as e:
            print(e)

                
    # Agregar comando
    elif accion == 3:
        pass
    # Eliminar comando
    elif accion == 4:
        pass

    else:
        os.system('cls')
        print("Ingrese una opción válida.\n")