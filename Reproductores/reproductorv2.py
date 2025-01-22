#Librerias para utilizar
#pip install mutagen
#pip install pygame

import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import io

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
            ventana_reproduccion.geometry("400x300")

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

            # Botones para avanzar y retroceder
            self.boton_anterior = tk.Button(ventana_reproduccion, text="Anterior", command=self.retroceder)
            self.boton_anterior.pack(side=tk.LEFT, padx=20)

            self.boton_siguiente = tk.Button(ventana_reproduccion, text="Siguiente", command=self.avanzar)
            self.boton_siguiente.pack(side=tk.RIGHT, padx=20)

            # Barra de progreso
            self.barra_progreso = tk.Scale(ventana_reproduccion, from_=0, to=100, orient="horizontal", length=300)
            self.barra_progreso.pack(pady=10)

            # Visualizador de la carátula
            self.caratula_imagen = tk.Label(ventana_reproduccion)
            self.caratula_imagen.pack(pady=10)

            # Selección de canción
            self.cancion_indice = 0
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")

    def reproducir_musica(self):
        if self.archivos_canciones:
            archivo_cancion = self.archivos_canciones[self.cancion_indice]
            pygame.mixer.music.load(archivo_cancion)
            pygame.mixer.music.play()

            # Actualizar carátula
            self.mostrar_caratula(archivo_cancion)

            # Actualizar barra de progreso
            self.actualizar_barra_progreso()

    def pausar_musica(self):
        pygame.mixer.music.pause()
    
    def detener_musica(self):
        pygame.mixer.music.stop()
    
    def avanzar(self):
        if self.cancion_indice < len(self.archivos_canciones) - 1:
            self.cancion_indice += 1
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")
            self.reproducir_musica()

    def retroceder(self):
        if self.cancion_indice > 0:
            self.cancion_indice -= 1
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")
            self.reproducir_musica()

    def mostrar_caratula(self, archivo_cancion):
        # Intentar obtener la carátula
        try:
            audio = MP3(archivo_cancion, ID3=ID3)
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC':
                    imagen = tag.data
                    imagen = Image.open(io.BytesIO(imagen))
                    imagen.thumbnail((100, 100))  # Redimensionar la imagen
                    self.caratula_imagen.config(image=ImageTk.PhotoImage(imagen))
                    self.caratula_imagen.image = ImageTk.PhotoImage(imagen)
                    break
        except Exception as e:
            print(f"Error al obtener la carátula: {e}")

    def actualizar_barra_progreso(self):
        # Obtener la duración total de la canción y actualizar la barra de progreso
        duracion = pygame.mixer.music.get_length()
        self.barra_progreso.config(to=duracion)

        # Actualizar la barra de progreso mientras se reproduce la canción
        def update_progress():
            if pygame.mixer.music.get_busy():
                progreso = pygame.mixer.music.get_pos() / 1000  # Convertir milisegundos a segundos
                self.barra_progreso.set(progreso)
                self.ventana_principal.after(1000, update_progress)
        
        update_progress()

# Crear la ventana principal de la aplicación
ventana_principal = tk.Tk()
reproductor = ReproductorMusica(ventana_principal)

# Ejecutar la interfaz gráfica
ventana_principal.mainloop()
