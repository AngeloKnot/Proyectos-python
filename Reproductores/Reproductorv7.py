import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import threading

# Inicializar pygame para la reproducción de música
pygame.mixer.init()

class ReproductorMusica:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Reproductor de Música Avanzado")
        self.ventana_principal.geometry("800x600")
        self.ventana_principal.config(bg="#1E1E1E")

        # Variables
        self.archivos_canciones = []
        self.cancion_indice = 0
        self.aleatorio = False
        self.repetir = False
        self.volumen = 1.0
        self.cancion_actual = tk.StringVar()
        self.cancion_actual.set("Ninguna canción seleccionada")
        self.mostrar_lyrics = False

        # Crear botones y controles
        self.boton_abrir_carpeta = tk.Button(self.ventana_principal, text="Abrir Carpeta", command=self.abrir_carpeta, 
                                              bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_abrir_carpeta.pack(pady=20)

        self.boton_reproducir = tk.Button(self.ventana_principal, text="Reproducir Música", command=self.reproducir_musica, 
                                          state=tk.DISABLED, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_reproducir.pack(pady=10)

        # Etiqueta para la canción
        self.etiqueta_cancion = tk.Label(self.ventana_principal, textvariable=self.cancion_actual, bg="#1E1E1E", fg="white", font=("Arial", 14))
        self.etiqueta_cancion.pack(pady=10)

        # Barra de volumen
        self.barra_volumen = tk.Scale(self.ventana_principal, from_=0, to=1, resolution=0.01, orient="horizontal", 
                                      length=300, bg="#2d2d2d", fg="white", sliderlength=15, font=("Arial", 12), label="Volumen")
        self.barra_volumen.set(self.volumen)
        self.barra_volumen.pack(pady=10)

        # Barra de progreso
        self.barra_progreso = tk.Scale(self.ventana_principal, from_=0, to=100, orient="horizontal", length=300, 
                                       bg="#2d2d2d", fg="white", sliderlength=15, font=("Arial", 12), label="Progreso")
        self.barra_progreso.pack(pady=10)

        # Botón para activar modo aleatorio
        self.boton_aleatorio = tk.Button(self.ventana_principal, text="Modo Aleatorio", command=self.toggle_aleatorio, 
                                         bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5)
        self.boton_aleatorio.pack(pady=10)

        # Botón para activar repetición
        self.boton_repetir = tk.Button(self.ventana_principal, text="Repetir Canción", command=self.toggle_repetir, 
                                       bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5)
        self.boton_repetir.pack(pady=10)

        # Botón para visualizar la onda
        self.boton_onda = tk.Button(self.ventana_principal, text="Mostrar Onda", command=self.mostrar_onda, 
                                     bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_onda.pack(pady=10)

        # Barra de búsqueda
        self.entrada_busqueda = tk.Entry(self.ventana_principal, font=("Arial", 12))
        self.entrada_busqueda.pack(pady=10)
        self.boton_buscar = tk.Button(self.ventana_principal, text="Buscar", command=self.buscar_cancion, 
                                      bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_buscar.pack(pady=10)

        # Lista de canciones
        self.lista_reproduccion = tk.Listbox(self.ventana_principal, height=10, width=50, font=("Arial", 12))
        self.lista_reproduccion.pack(pady=10)

        # Botón para seleccionar canción
        self.boton_seleccionar = tk.Button(self.ventana_principal, text="Seleccionar Canción", command=self.seleccionar_cancion, 
                                           bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.boton_seleccionar.pack(pady=10)

        # Variables para las ondas de sonido
        self.figura = None
        self.canvas = None

    def abrir_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de música")
        if carpeta:
            self.archivos_canciones = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith((".mp3", ".wav", ".flac", ".ogg"))]
            if self.archivos_canciones:
                self.boton_reproducir.config(state=tk.NORMAL)
                for archivo in self.archivos_canciones:
                    self.lista_reproduccion.insert(tk.END, os.path.basename(archivo))
                messagebox.showinfo("Éxito", f"Se encontraron {len(self.archivos_canciones)} canciones.")
            else:
                messagebox.showwarning("No se encontraron canciones", "No se encontraron archivos de música en la carpeta seleccionada.")

    def reproducir_musica(self):
        if self.archivos_canciones:
            archivo_cancion = self.archivos_canciones[self.cancion_indice]
            pygame.mixer.music.load(archivo_cancion)
            pygame.mixer.music.set_volume(self.barra_volumen.get())
            pygame.mixer.music.play(loops=-1 if self.repetir else 0)
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(archivo_cancion)}")
            self.mostrar_lyrics = False
            self.mostrar_onda()

    def mostrar_onda(self):
        if self.figura is not None:
            self.figura.clear()

        # Crear onda de sonido
        archivo_cancion = self.archivos_canciones[self.cancion_indice]
        if archivo_cancion.endswith(".mp3"):
            audio = MP3(archivo_cancion)
        else:
            audio = None

        duracion = pygame.mixer.music.get_length()
        samples = np.linspace(0, duracion, 5000)
        waveform = np.sin(2 * np.pi * 440 * samples)  # Ejemplo de onda (senoidal)

        self.figura = plt.Figure(figsize=(6, 2), dpi=100)
        eje = self.figura.add_subplot(111)
        eje.plot(samples, waveform)
        eje.set_title("Onda de Sonido")
        eje.set_xlabel("Tiempo (s)")
        eje.set_ylabel("Amplitud")

        self.canvas = FigureCanvasTkAgg(self.figura, self.ventana_principal)
        self.canvas.get_tk_widget().pack(pady=10)
        self.canvas.draw()

    def toggle_aleatorio(self):
        self.aleatorio = not self.aleatorio
        if self.aleatorio:
            self.boton_aleatorio.config(bg="#FF9800")
        else:
            self.boton_aleatorio.config(bg="#FFC107")

    def toggle_repetir(self):
        self.repetir = not self.repetir
        if self.repetir:
            self.boton_repetir.config(bg="#FF9800")
        else:
            self.boton_repetir.config(bg="#FFC107")

    def buscar_cancion(self):
        termino_busqueda = self.entrada_busqueda.get().lower()
        for i, archivo in enumerate(self.archivos_canciones):
            if termino_busqueda in os.path.basename(archivo).lower():
                self.lista_reproduccion.selection_clear(0, tk.END)
                self.lista_reproduccion.selection_set(i)
                self.cancion_indice = i
                break

    def seleccionar_cancion(self):
        seleccion = self.lista_reproduccion.curselection()
        if seleccion:
            self.cancion_indice = seleccion[0]
            self.cancion_actual.set(f"Reproduciendo: {os.path.basename(self.archivos_canciones[self.cancion_indice])}")
            self.reproducir_musica()

# Crear la ventana principal de la aplicación
ventana_principal = tk.Tk()
reproductor = ReproductorMusica(ventana_principal)

# Ejecutar la interfaz gráfica
ventana_principal.mainloop()
