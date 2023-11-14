import subprocess
import time
import pyautogui

def reproducir_cancion_en_spotify(nombre_cancion):
    # Ruta al ejecutable de Spotify
    ruta_spotify = r"C:\Users\guido\AppData\Local\Microsoft\WindowsApps\Spotify.exe"  # Reemplaza con tu ruta

    # Comando para abrir Spotify
    comando_spotify = [ruta_spotify]

    # Ejecutar el comando para abrir Spotify
    subprocess.run(comando_spotify)

    # Esperar unos segundos para que Spotify se abra completamente
    time.sleep(5)

    pyautogui.hotkey('ctrl', 'l')  # Seleccionar la barra de búsqueda
    time.sleep(1)
    pyautogui.write(nombre_cancion)
    pyautogui.press('enter')

    time.sleep(2)  # Esperar a que se carguen los resultados de búsqueda

    # Hacer clic en la primera canción en los resultados de búsqueda
    pyautogui.click(x=450, y=400)  # Ajusta las coordenadas según tu pantalla

if __name__ == '__main__':
    # Ejemplo de uso
    nombre_cancion_a_reproducir = "Azote"
    reproducir_cancion_en_spotify(nombre_cancion_a_reproducir)