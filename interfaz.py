"""Interfaz gráfica de la aplicación."""
import tkinter as tk
from tkinter import ttk
import json

def agregar_atajo():
    comando = entry_comando.get()
    parametro = entry_parametro.get()
    tecla = entry_tecla.get()

    if comando and tecla:
        atajo = {"comando": comando, "parametro": parametro}
        atajos[tecla] = atajo
        actualizar_lista_atajos()
        guardar_atajos_en_json()
    else:
        lbl_estado.config(text="Por favor, complete todos los campos.")

def actualizar_lista_atajos():
    lista_atajos.delete(0, tk.END)
    # instrucciones = atajos.get('config', {})
    # print(instrucciones)
    # for tecla, atajo in instrucciones:
    #     print("\n", atajo)
    #     lista_atajos.insert(tk.END, f"{tecla}: {atajo} - {atajo}")
    # itero entre todos los valores de mi diccionario {"f8": [["hablar"], ["hola"]]}
    for tecla, instrucciones in atajos["config"].items():
        instrucciones_str = ""
        for i in range(len(instrucciones[0])):
            comando = instrucciones[0][i]
            parametro = instrucciones[1][i]
            instrucciones_str += f"{comando}: {parametro} - "
        lista_atajos.insert(tk.END, f"{tecla}: {instrucciones_str}")


def guardar_atajos_en_json():
    with open("prueba_config.json", "w") as archivo:
        json.dump(atajos, archivo)

# Cargar atajos desde el archivo JSON
try:
    with open("prueba_config.json", "r") as archivo:
        atajos = json.load(archivo)
except FileNotFoundError:
    atajos = {}

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Atajos")
ventana.geometry("800x550")

# Widgets
lbl_comando = tk.Label(ventana, text="Comando:")
lbl_comando.grid(row=0, column=0, padx=10, pady=5)
entry_comando = tk.Entry(ventana)
entry_comando.grid(row=0, column=1, padx=10, pady=5)

lbl_parametro = tk.Label(ventana, text="Parámetro:")
lbl_parametro.grid(row=1, column=0, padx=10, pady=5)
entry_parametro = tk.Entry(ventana)
entry_parametro.grid(row=1, column=1, padx=10, pady=5)

lbl_tecla = tk.Label(ventana, text="Tecla:")
lbl_tecla.grid(row=2, column=0, padx=10, pady=5)
entry_tecla = tk.Entry(ventana)
entry_tecla.grid(row=2, column=1, padx=10, pady=5)

btn_agregar = tk.Button(ventana, text="Agregar Atajo", command=agregar_atajo)
btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

lbl_estado = tk.Label(ventana, text="")
lbl_estado.grid(row=4, column=0, columnspan=2, pady=5)

# Lista de atajos existentes
lista_atajos = tk.Listbox(ventana)
lista_atajos.grid(row=5, column=0, columnspan=2, pady=10)
actualizar_lista_atajos()

# Iniciar el bucle de eventos
ventana.mainloop()