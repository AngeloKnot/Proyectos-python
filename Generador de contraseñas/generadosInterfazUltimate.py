import tkinter as tk
from tkinter import messagebox
import random
import string

# Función para generar contraseña
def generar_contraseña():
    try:
        longitud = int(entry_longitud.get())
        if longitud < 6:
            messagebox.showwarning("Advertencia", "La longitud debe ser al menos de 6 caracteres.")
            return
        
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(0, contraseña)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para la longitud.")

# Función para copiar contraseña al portapapeles
def copiar_contraseña():
    contraseña = entry_resultado.get()
    if contraseña:
        root.clipboard_clear()
        root.clipboard_append(contraseña)
        root.update()
        messagebox.showinfo("Éxito", "¡Contraseña copiada al portapapeles!")
    else:
        messagebox.showwarning("Advertencia", "No hay ninguna contraseña generada para copiar.")

# Crear ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#2b2b2b")

# Estilo general
fuente_titulo = ("Arial", 16, "bold")
fuente_texto = ("Arial", 12)
color_fondo = "#2b2b2b"
color_texto = "#ffffff"
color_boton = "#4caf50"
color_boton_texto = "#ffffff"

# Título
label_titulo = tk.Label(root, text="Generador de Contraseñas", font=fuente_titulo, bg=color_fondo, fg=color_texto)
label_titulo.pack(pady=10)

# Etiqueta y campo de entrada para longitud
label_longitud = tk.Label(root, text="Longitud de la contraseña:", font=fuente_texto, bg=color_fondo, fg=color_texto)
label_longitud.pack(pady=5)
entry_longitud = tk.Entry(root, width=15, font=fuente_texto, justify="center")
entry_longitud.pack(pady=5)

# Botón para generar contraseña
btn_generar = tk.Button(root, text="Generar Contraseña", font=fuente_texto, bg=color_boton, fg=color_boton_texto, command=generar_contraseña)
btn_generar.pack(pady=10)

# Campo de texto para mostrar la contraseña generada
entry_resultado = tk.Entry(root, width=40, font=fuente_texto, justify="center", state="normal")
entry_resultado.pack(pady=5)

# Botón para copiar contraseña
btn_copiar = tk.Button(root, text="Copiar Contraseña", font=fuente_texto, bg=color_boton, fg=color_boton_texto, command=copiar_contraseña)
btn_copiar.pack(pady=10)

# Pie de página
label_footer = tk.Label(root, text="Creado con ♥ en Python", font=("Arial", 10), bg=color_fondo, fg="#777777")
label_footer.pack(side="bottom", pady=5)

# Iniciar bucle de la interfaz
root.mainloop()
