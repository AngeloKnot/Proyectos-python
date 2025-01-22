import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from PIL import Image, ImageTk
import io
import random
import time

# Inicializar pygame para la reproducción de música
pygame.mixer.init()

class ReproductorMusica:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Reproductor de Música")
        self.ventana_principal.geometry("600x500")
        self.ventana_principal.config(bg="#1E1E1E")

        # Crear botón para abrir carpeta y seleccionar canciones
        self.boton_abrir_carpeta = tk.Button(self.ventana_principal, text="Abrir Carpeta", command=self.abrir_carpeta, 
                                              bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_abrir_carpeta.pack(pady=20)

        # Crear botón para abrir la ventana de reproducción
        self.boton_reproducir = tk.Button(self.ventana_principal, text="Reproducir Música", command=self.abrir_ventana_reproduccion, 
                                          state=tk.DISABLED, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_reproducir.pack(pady=10)

        # Lista de canciones seleccionadas
        self.archivos_canciones = []
        self.cancion_indice = 0
        self.aleatorio = False
        self.repetir = False
        self.volumen = 1.0

    def abrir_carpeta(self):
        # Abre un explorador de archivos para seleccionar una carpeta
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de música")
        if carpeta:
            # Buscar archivos de música en la carpeta seleccionada
            self.archivos_canciones = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith((".mp3", ".wav", ".flac"))]
            if self.archivos_canciones:
                self.boton_reproducir.config(state=tk.NORMAL)
                messagebox.showinfo("Éxito", f"Se encontraron {len(self.archivos_canciones)} canciones.")
            else:
                messagebox.showwarning("No se encontraron canciones", "No se encontraron archivos de música en la carpeta seleccionada.")

    def abrir_ventana_reproduccion(self):
        if self.archivos_canciones:
            ventana_reproduccion = tk.Toplevel(self.ventana_principal)
            ventana_reproduccion.title("Reproducción de Música")
            ventana_reproduccion.geometry("600x500")
            ventana_reproduccion.config(bg="#1E1E1E")

            # Mostrar canción actual
            self.cancion_actual = tk.StringVar()
            self.cancion_actual.set("Ninguna canción seleccionada")

            etiqueta_cancion = tk.Label(ventana_reproduccion, textvariable=self.cancion_actual, bg="#1E1E1E", fg="white", font=("Arial", 14))
            etiqueta_cancion.pack(pady=10)

            # Mostrar los metadatos de la canción
            self.metadatos_cancion = tk.StringVar()
            self.metadatos_cancion.set("Artista: \nÁlbum: \nGénero:")

            etiqueta_metadatos = tk.Label(ventana_reproduccion, textvariable=self.metadatos_cancion, bg="#1E1E1E", fg="white", font=("Arial", 12))
            etiqueta_metadatos.pack(pady=5)

            # Botones para controlar la música
            self.boton_play = tk.Button(ventana_reproduccion, text="Play", command=self.reproducir_musica, 
                                        bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
            self.boton_play.pack(pady=10)

            self.boton_pause = tk.Button(ventana_reproduccion, text="Pausar", command=self.pausar_musica, 
                                         bg="#FFC107", fg="white", font=("Arial", 12), padx=10, pady=5)
            self.boton_pause.pack(pady=10)

            self.boton_continue = tk.Button(ventana_reproduccion, text="Continuar", command=self.continuar_musica, 
                                            bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
            self.boton_continue.pack(pady=10)

            self.boton_stop = tk.Button(ventana_reproduccion, text="Detener", command=self.detener_musica, 
                                        bg="#F44336", fg="white", font=("Arial", 12), padx=10, pady=5)
            self.boton_stop.pack(pady=10)

            # Barra de progreso
            self.barra_progreso = tk.Scale(ventana_reproduccion, from_=0, to=100, orient="horizontal", length=400, 
                                           bg="#2d2d2d", fg="white", sliderlength=15, font=("Arial", 12))
            self.barra_progreso.pack(pady=10)

            # Visualizador de la carátula
            self.caratula_imagen = tk.Label(ventana_reproduccion, bg="#2d2d2d")
            self.caratula_imagen.pack(pady=10)

            # Lista de reproducción
            self.lista_reproduccion = tk.Listbox(ventana_reproduccion, selectmode=tk.SINGLE, height=8, width=40, font=("Arial", 12))
            for archivo in self.archivos_canciones:
                self.lista_reproduccion.insert(tk.END, os.path.basename(archivo))
            self.lista_reproduccion.pack(pady=10)

            self.boton_seleccionar = tk.Button(ventana_reproduccion, text="Seleccionar Canción", command=self.seleccionar_cancion, 
                                               bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
            self.boton_seleccionar.pack(pady=5)

            # Selección de canción
            self.cancion_indice = 0
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")

            # Mostrar datos de la canción
            self.mostrar_metadatos(self.archivos_canciones[self.cancion_indice])

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

    def continuar_musica(self):
        pygame.mixer.music.unpause()

    def detener_musica(self):
        pygame.mixer.music.stop()

    def mostrar_caratula(self, archivo_cancion):
        try:
            audio = None
            if archivo_cancion.endswith(".mp3"):
                audio = MP3(archivo_cancion, ID3=ID3)
            elif archivo_cancion.endswith(".flac"):
                audio = FLAC(archivo_cancion)

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
            self.caratula_imagen.config(image='')

    def mostrar_metadatos(self, archivo_cancion):
        try:
            audio = None
            if archivo_cancion.endswith(".mp3"):
                audio = MP3(archivo_cancion, ID3=ID3)
            elif archivo_cancion.endswith(".flac"):
                audio = FLAC(archivo_cancion)

            artista = audio.get('TPE1', 'Desconocido').text[0]
            album = audio.get('TALB', 'Desconocido').text[0]
            genero = audio.get('TCON', 'Desconocido').text[0]

            self.metadatos_cancion.set(f"Artista: {artista}\nÁlbum: {album}\nGénero: {genero}")
        except Exception as e:
            print(f"Error al obtener metadatos: {e}")
            self.metadatos_cancion.set("Artista: Desconocido\nÁlbum: Desconocido\nGénero: Desconocido")

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

    def seleccionar_cancion(self):
        # Obtener la canción seleccionada desde la lista
        seleccion = self.lista_reproduccion.curselection()
        if seleccion:
            self.cancion_indice = seleccion[0]
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")
            self.mostrar_metadatos(self.archivos_canciones[self.cancion_indice])
            self.reproducir_musica()

# Crear la ventana principal de la aplicación
ventana_principal = tk.Tk()
reproductor = ReproductorMusica(ventana_principal)

# Ejecutar la interfaz gráfica
ventana_principal.mainloop()
