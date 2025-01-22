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
        root.update()  # Necesario para actualizar el portapapeles
        messagebox.showinfo("Éxito", "¡Contraseña copiada al portapapeles!")
    else:
        messagebox.showwarning("Advertencia", "No hay ninguna contraseña generada para copiar.")

# Crear ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas")
root.geometry("400x200")
root.resizable(False, False)

# Etiqueta y campo de entrada para longitud
label_longitud = tk.Label(root, text="Longitud de la contraseña:")
label_longitud.pack(pady=5)
entry_longitud = tk.Entry(root, width=15)
entry_longitud.pack(pady=5)

# Botón para generar contraseña
btn_generar = tk.Button(root, text="Generar Contraseña", command=generar_contraseña)
btn_generar.pack(pady=10)

# Campo de texto para mostrar la contraseña generada
entry_resultado = tk.Entry(root, width=40, state="normal", justify="center")
entry_resultado.pack(pady=5)

# Botón para copiar contraseña
btn_copiar = tk.Button(root, text="Copiar Contraseña", command=copiar_contraseña)
btn_copiar.pack(pady=10)

# Iniciar bucle de la interfaz
root.mainloop()