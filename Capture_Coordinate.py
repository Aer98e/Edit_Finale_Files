from pynput import mouse
import time

# Lista de palabras
Coordiante_Requerement = ["Selection", "Lyrics", "Text"]

# Lista para guardar las coordenadas
coordenadas = []

Elemento='Funcion'

# Función para detectar el clic del mouse
def on_click(x, y, button, pressed):
    if pressed:
        # Agregar las coordenadas a la lista
        coordenadas.append((x, y))
        print(f"Coordenadas guardadas: {x}, {y}")
        return False

# Iterar sobre la lista de palabras
    print(f"Haga click en {Elemento}...")
    # Escuchar el clic del mouse
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    time.sleep(1)  # Esperar un segundo antes de preguntar por la siguiente palabra

# Imprimir la lista de coordenadas
File_Coordinates = open("Finale_Coordinate.coor", "w")
for i in coordenadas:
    File_Coordinates.write(f"{i}\n")
File_Coordinates.close()
