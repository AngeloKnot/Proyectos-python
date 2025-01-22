import tkinter as tk
from tkinter import messagebox
from collections import Counter
import re

# Función para analizar el texto
def analizar_texto():
    texto = text_area.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Advertencia", "El área de texto está vacía. Por favor, ingresa algún texto.")
        return

    # Cálculos básicos
    num_caracteres = len(texto)
    palabras = re.findall(r'\b\w+\b', texto.lower())
    num_palabras = len(palabras)
    oraciones = re.split(r'[.!?]', texto)
    num_oraciones = sum(1 for oracion in oraciones if oracion.strip())

    # Palabras más y menos comunes
    conteo_palabras = Counter(palabras)
    palabra_mas_comun = max(conteo_palabras, key=conteo_palabras.get)
    palabra_menos_comun = min(conteo_palabras, key=conteo_palabras.get)

    # Mostrar resultados
    resultados = (
        f"Número de caracteres: {num_caracteres}\n"
        f"Número de palabras: {num_palabras}\n"
        f"Número de oraciones: {num_oraciones}\n"
        f"Palabra más común: {palabra_mas_comun} (x{conteo_palabras[palabra_mas_comun]})\n"
        f"Palabra menos común: {palabra_menos_comun} (x{conteo_palabras[palabra_menos_comun]})"
    )
    resultado_texto.config(state="normal")
    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, resultados)
    resultado_texto.config(state="disabled")

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador de Texto")
root.geometry("600x400")
root.configure(bg="#2b2b2b")

# Fuente y colores
fuente_titulo = ("Arial", 16, "bold")
fuente_texto = ("Arial", 12)
color_fondo = "#2b2b2b"
color_texto = "#ffffff"
color_boton = "#4caf50"
color_boton_texto = "#ffffff"

# Título
label_titulo = tk.Label(root, text="Analizador de Texto", font=fuente_titulo, bg=color_fondo, fg=color_texto)
label_titulo.pack(pady=10)

# Área de texto para ingreso
text_area = tk.Text(root, height=10, width=70, font=fuente_texto, wrap="word")
text_area.pack(pady=10)

# Botón para analizar
btn_analizar = tk.Button(root, text="Analizar Texto", font=fuente_texto, bg=color_boton, fg=color_boton_texto, command=analizar_texto)
btn_analizar.pack(pady=10)

# Área de texto para mostrar resultados
resultado_texto = tk.Text(root, height=10, width=70, font=fuente_texto, bg="#e0e0e0", state="disabled", wrap="word")
resultado_texto.pack(pady=10)

# Pie de página
label_footer = tk.Label(root, text="Creado con ♥ en Python", font=("Arial", 10), bg=color_fondo, fg="#777777")
label_footer.pack(side="bottom", pady=5)

# Iniciar la interfaz
root.mainloop()
