import json

def mostrar_comandos():
    with open("prueba_config2.json", "r", encoding="utf-8") as archivo:
        config = json.load(archivo)["comandos"]
    for clave in config:
        texto_a_mostrar = f"{config[clave][2]} ({clave}) - "
        for i in range(len(config[clave][0])):
            valor = config[clave][1][i]
            comando = config[clave][0][i]
            if comando in ["Hablar", "Reproducir Spotify"]:
                valor = "'" + valor + "'"
            texto_a_mostrar += f"{config[clave][0][i]}: {valor}, "
        texto_a_mostrar = texto_a_mostrar[:-2]
        print(texto_a_mostrar)
    print("") # Espacio vacío para que no se pegue con el selector de opciones

def editar_comandos():
    pass

while True:
    accion = int(input("Elija una opción (o cierre esta ventana para continuar)\n1. Ver comandos  2. Editar comando  3. Agregar comando  4. Eliminar comando\n"))

    if accion == 1:
        mostrar_comandos()
    elif accion == 2:
        mostrar_comandos()
        print("Presione la tecla a editar")
    elif accion == 3:
        pass