import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading


def actualizar_barra(current, total, barra):
    """Actualiza la barra de progreso."""
    progreso = int((current / total) * 100)
    barra['value'] = progreso


def descargar():
    """Ejecuta la descarga en un hilo separado."""
    threading.Thread(target=descargar_video).start()


def descargar_video():
    """Descarga el video o la lista de reproducción usando yt-dlp."""
    url = entrada_url.get()
    carpeta = entrada_carpeta.get()
    formato = formato_seleccionado.get()
    progreso['value'] = 0

    if not url.strip():
        messagebox.showwarning("Advertencia", "Por favor, ingresa la URL del video o lista de reproducción.")
        return

    if not carpeta.strip():
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta para guardar los archivos.")
        return

    try:
        # Configuración de formato
        if formato == "Audio (MP3)":
            opciones = {
                'format': 'bestaudio/best',
                'outtmpl': f"{carpeta}/%(title)s.%(ext)s",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        else:  # Video
            opciones = {
                'format': 'best',
                'outtmpl': f"{carpeta}/%(title)s.%(ext)s"
            }

        # Llamada a yt-dlp
        with yt_dlp.YoutubeDL(opciones) as ydl:
            messagebox.showinfo("Descargando", "La descarga ha comenzado. Por favor, espera...")
            ydl.add_progress_hook(lambda d: actualizar_barra(d['downloaded_bytes'], d['total_bytes'], progreso))
            ydl.download([url])

        # Actualizar historial
        historial_listbox.insert(tk.END, f"{yt_dlp.YoutubeDL().extract_info(url, download=False)['title']} - {carpeta}")
        messagebox.showinfo("Éxito", f"¡Descarga completada con éxito en:\n{carpeta}!")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descargar:\n{e}")


def seleccionar_carpeta():
    """Abre un cuadro de diálogo para seleccionar la carpeta de destino."""
    carpeta = filedialog.askdirectory()
    if carpeta:
        entrada_carpeta.delete(0, tk.END)
        entrada_carpeta.insert(0, carpeta)


# Crear ventana principal
root = tk.Tk()
root.title("Descargador de Videos y Listas de Reproducción")
root.geometry("500x500")
root.resizable(False, False)

# Título
titulo = tk.Label(root, text="Descargador de Videos y Audio con yt-dlp", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# URL del video o lista de reproducción
frame_url = ttk.LabelFrame(root, text="URL del Video o Lista de Reproducción")
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

# Opciones de formato
frame_formato = ttk.LabelFrame(root, text="Selecciona el Formato")
frame_formato.pack(padx=10, pady=5, fill="x")

formato_seleccionado = tk.StringVar(value="Video")
ttk.Radiobutton(frame_formato, text="Video", variable=formato_seleccionado, value="Video").pack(side="left", padx=10, pady=5)
ttk.Radiobutton(frame_formato, text="Audio (MP3)", variable=formato_seleccionado, value="Audio (MP3)").pack(side="left", padx=10, pady=5)

# Barra de progreso
frame_progreso = ttk.LabelFrame(root, text="Progreso de Descarga")
frame_progreso.pack(padx=10, pady=5, fill="x")

progreso = ttk.Progressbar(frame_progreso, orient="horizontal", length=400, mode="determinate")
progreso.pack(padx=10, pady=10)

# Botón de descarga
btn_descargar = ttk.Button(root, text="Descargar", command=descargar)
btn_descargar.pack(pady=10)

# Pestaña de historial
frame_historial = ttk.LabelFrame(root, text="Historial de Descargas")
frame_historial.pack(padx=10, pady=10, fill="both", expand=True)

historial_listbox = tk.Listbox(frame_historial, width=60, height=10)
historial_listbox.pack(padx=10, pady=10, fill="both", expand=True)

# Iniciar bucle de la aplicación
root.mainloop()
