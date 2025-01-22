import tkinter as tk
from tkinter import ttk, messagebox
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

# Crear ventana principal
root = tk.Tk()
root.title("Analizador de Texto")
root.geometry("700x500")
root.iconbitmap("Contadores/icono.ico")  # Cambia "icono.ico" por la ruta de tu archivo .ico
root.resizable(False, False)

# Crear pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Pestaña de análisis
tab_analisis = ttk.Frame(notebook)
notebook.add(tab_analisis, text="Analizador de Texto")

# Pestaña de instrucciones
tab_instrucciones = ttk.Frame(notebook)
notebook.add(tab_instrucciones, text="Instrucciones")

# Diseño de la pestaña de análisis
frame_texto = ttk.LabelFrame(tab_analisis, text="Texto de Entrada")
frame_texto.pack(padx=10, pady=10, fill="both", expand=True)

text_area = tk.Text(frame_texto, height=10, wrap="word")
text_area.pack(padx=10, pady=10, fill="both", expand=True)

btn_analizar = ttk.Button(tab_analisis, text="Analizar Texto", command=analizar_texto)
btn_analizar.pack(pady=10)

frame_resultado = ttk.LabelFrame(tab_analisis, text="Resultados")
frame_resultado.pack(padx=10, pady=10, fill="both", expand=True)

resultado_texto = tk.Text(frame_resultado, height=10, state="disabled", wrap="word", bg="#f0f0f0")
resultado_texto.pack(padx=10, pady=10, fill="both", expand=True)

# Diseño de la pestaña de instrucciones
label_instrucciones = tk.Label(
    tab_instrucciones,
    text=(
        "Bienvenido al Analizador de Texto.\n\n"
        "1. Ingresa o pega un texto en el área de texto.\n"
        "2. Haz clic en 'Analizar Texto' para obtener estadísticas:\n"
        "   - Número de caracteres.\n"
        "   - Número de palabras.\n"
        "   - Número de oraciones.\n"
        "   - Palabra más y menos común.\n"
        "3. Los resultados aparecerán en la sección de resultados."
    ),
    justify="left",
    font=("Arial", 12),
    wraplength=650
)
label_instrucciones.pack(padx=20, pady=20)

# Iniciar bucle de la interfaz
root.mainloop()
