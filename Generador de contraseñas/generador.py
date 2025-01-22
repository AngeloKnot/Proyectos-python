import random
import string

def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def main():
    print("¡Bienvenido al generador de contraseñas!")
    try:
        longitud = int(input("¿De cuántos caracteres deseas tu contraseña? (Recomendado: 12): "))
        if longitud < 6:
            print("La contraseña debe tener al menos 6 caracteres. Usaremos 6 por defecto.")
            longitud = 6
        contraseña = generar_contraseña(longitud)
        print(f"Tu contraseña generada es: {contraseña}")
    except ValueError:
        print("Por favor, ingresa un número válido.")

if __name__ == "__main__":
    main()