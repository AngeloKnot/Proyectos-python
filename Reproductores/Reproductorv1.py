#Librerias para utilizar
#pip install mutagen
#pip install pygame



import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

# Inicializar pygame para la reproducción de música
pygame.mixer.init()

class ReproductorMusica:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Reproductor de Música")
        self.ventana_principal.geometry("400x200")

        # Crear botón para abrir carpeta y seleccionar canciones
        self.boton_abrir_carpeta = tk.Button(self.ventana_principal, text="Abrir Carpeta", command=self.abrir_carpeta)
        self.boton_abrir_carpeta.pack(pady=20)

        # Crear botón para abrir la ventana de reproducción
        self.boton_reproducir = tk.Button(self.ventana_principal, text="Reproducir Música", command=self.abrir_ventana_reproduccion, state=tk.DISABLED)
        self.boton_reproducir.pack(pady=10)

        # Lista de canciones seleccionadas
        self.archivos_canciones = []

    def abrir_carpeta(self):
        # Abre un explorador de archivos para seleccionar una carpeta
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de música")
        if carpeta:
            # Buscar archivos .mp3 en la carpeta seleccionada
            self.archivos_canciones = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith(".mp3")]
            if self.archivos_canciones:
                self.boton_reproducir.config(state=tk.NORMAL)
                messagebox.showinfo("Éxito", f"Se encontraron {len(self.archivos_canciones)} canciones.")
            else:
                messagebox.showwarning("No se encontraron canciones", "No se encontraron archivos MP3 en la carpeta seleccionada.")
    
    def abrir_ventana_reproduccion(self):
        if self.archivos_canciones:
            ventana_reproduccion = tk.Toplevel(self.ventana_principal)
            ventana_reproduccion.title("Reproducción de Música")
            ventana_reproduccion.geometry("300x200")

            # Mostrar canción actual
            self.cancion_actual = tk.StringVar()
            self.cancion_actual.set("Ninguna canción seleccionada")

            etiqueta_cancion = tk.Label(ventana_reproduccion, textvariable=self.cancion_actual)
            etiqueta_cancion.pack(pady=20)

            # Botones para controlar la música
            self.boton_play = tk.Button(ventana_reproduccion, text="Play", command=self.reproducir_musica)
            self.boton_play.pack(pady=5)

            self.boton_pause = tk.Button(ventana_reproduccion, text="Pausar", command=self.pausar_musica)
            self.boton_pause.pack(pady=5)

            self.boton_stop = tk.Button(ventana_reproduccion, text="Detener", command=self.detener_musica)
            self.boton_stop.pack(pady=5)

            # Selección de canción
            self.cancion_indice = 0
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")

    def reproducir_musica(self):
        if self.archivos_canciones:
            archivo_cancion = self.archivos_canciones[self.cancion_indice]
            pygame.mixer.music.load(archivo_cancion)
            pygame.mixer.music.play()
    
    def pausar_musica(self):
        pygame.mixer.music.pause()
    
    def detener_musica(self):
        pygame.mixer.music.stop()

# Crear la ventana principal de la aplicación
ventana_principal = tk.Tk()
reproductor = ReproductorMusica(ventana_principal)

# Ejecutar la interfaz gráfica
ventana_principal.mainloop()
