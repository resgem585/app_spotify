import tkinter as tk
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import CLIENT_ID, CLIENT_SECRET
import spotipy

def buscar_canciones():
    artista = entry.get()
    
    results = sp.search(q=f'artist:{artista}', type='artist')
    
    if not results['artists']['items']:
        resultado_label.config(text=f"No se encontró información para el artista {artista}.")
        return None
    
    artist_id = results['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)

    # Almacenar las canciones populares en la variable global
    global canciones_populares
    canciones_populares = top_tracks['tracks']

    mostrar_canciones_populares()

def mostrar_canciones_populares():
    resultado_label.config(text="\nLas 10 canciones más populares:")
    for i, cancion in enumerate(canciones_populares):
        resultado_label.config(text=f"{resultado_label.cget('text')}\n{i + 1}. {cancion['name']} - Popularidad: {cancion['popularity']}")

def agregar_cancion():
    try:
        seleccion = int(entry_seleccion.get())
        if 1 <= seleccion <= len(canciones_populares):
            cancion_seleccionada = canciones_populares[seleccion - 1]

            # Añadir una línea divisoria antes de agregar la primera canción
            if not playlist:
                resultado_label.config(text=f"{resultado_label.cget('text')}\n{'='*40}")

            playlist.append(cancion_seleccionada)
            resultado_label.config(text=f"{resultado_label.cget('text')}\n{cancion_seleccionada['name']} agregada a la lista de reproducción.")
        else:
            resultado_label.config(text="Por favor, ingrese un número válido (1-10).")
    except ValueError:
        resultado_label.config(text="Por favor, ingrese un número válido (1-10).")


def mostrar_lista_reproduccion():
    duracion_total = sum([cancion['duration_ms'] for cancion in playlist])
    duracion_total_minutos = duracion_total / 60000

    resultado_label.config(text=f"{resultado_label.cget('text')}\n\n{'='*40}\nLista de reproducción:")

    if not playlist:
        resultado_label.config(text=f"{resultado_label.cget('text')}\nNo hay canciones en la lista de reproducción.")
    else:
        for i, cancion in enumerate(playlist):
            resultado_label.config(text=f"{resultado_label.cget('text')}\n{i + 1}. {cancion['name']} - Duración: {cancion['duration_ms']} ms")

        resultado_label.config(text=f"{resultado_label.cget('text')}\n{'='*40}\nDuración total de la lista de reproducción: {duracion_total_minutos:.2f} minutos.")

# Configuración de Spotify con las credenciales
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))

# Crear la ventana principal
root = tk.Tk()
root.title("Spotify App")

# Crear y posicionar widgets en la ventana
label = tk.Label(root, text="Ingrese el nombre del artista:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

buscar_button = tk.Button(root, text="Buscar Canciones", command=buscar_canciones)
buscar_button.pack(pady=10)

resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=20)

label_seleccion = tk.Label(root, text="Seleccione una canción (1-10):")
label_seleccion.pack(pady=10)

entry_seleccion = tk.Entry(root, width=5)
entry_seleccion.pack(pady=10)

agregar_button = tk.Button(root, text="Agregar a la Lista", command=agregar_cancion)
agregar_button.pack(pady=10)

mostrar_lista_button = tk.Button(root, text="Mostrar Lista de Reproducción", command=mostrar_lista_reproduccion)
mostrar_lista_button.pack(pady=10)

# Lista de reproducción y canciones populares
playlist = []
canciones_populares = []

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
