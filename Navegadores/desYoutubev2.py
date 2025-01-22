# Nota: instalar la siguiente libreria en el cmd del equipo   
# pip install yt-dlp

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp

def descargar_video():
    """Descarga el video usando yt-dlp."""
    url = entrada_url.get()
    carpeta = entrada_carpeta.get()

    if not url.strip():
        messagebox.showwarning("Advertencia", "Por favor, ingresa la URL del video.")
        return

    if not carpeta.strip():
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta para guardar el video.")
        return

    try:
        opciones = {
            'format': 'best',  # Mejor calidad disponible
            'outtmpl': f"{carpeta}/%(title)s.%(ext)s"  # Ruta de salida personalizada
        }
        with yt_dlp.YoutubeDL(opciones) as ydl:
            messagebox.showinfo("Descargando", "La descarga ha comenzado. Por favor, espera...")
            ydl.download([url])
        messagebox.showinfo("Éxito", f"¡Video descargado con éxito en:\n{carpeta}!")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar el video:\n{e}")

def seleccionar_carpeta():
    """Abre un cuadro de diálogo para seleccionar la carpeta de destino."""
    carpeta = filedialog.askdirectory()
    if carpeta:
        entrada_carpeta.delete(0, tk.END)
        entrada_carpeta.insert(0, carpeta)

# Crear ventana principal
root = tk.Tk()
root.title("Descargador de Videos")
root.geometry("500x300")
root.resizable(False, False)

# Título
titulo = tk.Label(root, text="Descargador de Videos con yt-dlp", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# URL del video
frame_url = ttk.LabelFrame(root, text="URL del Video")
frame_url.pack(padx=10, pady=5, fill="x")

entrada_url = ttk.Entry(frame_url, width=60)
entrada_url.pack(padx=10, pady=5)

# Carpeta de descarga
frame_carpeta = ttk.LabelFrame(root, text="Carpeta de Destino")
frame_carpeta.pack(padx=10, pady=5, fill="x")

entrada_carpeta = ttk.Entry(frame_carpeta, width=50)
entrada_carpeta.pack(side="left", padx=10, pady=5)

btn_carpeta = ttk.Button(frame_carpeta, text="Seleccionar", command=seleccionar_carpeta)
btn_carpeta.pack(side="left", padx=5, pady=5)

# Botón de descarga
btn_descargar = ttk.Button(root, text="Descargar Video", command=descargar_video)
btn_descargar.pack(pady=10)

# Iniciar bucle de la aplicación
root.mainloop()
