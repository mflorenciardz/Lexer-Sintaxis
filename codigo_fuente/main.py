# Archivo principal del programa.

#Es el encargado de iniciar la ejecución del lexer. 
#Lee el texto ingresado por el usuario o el archivo de prueba y muestra los tokens reconocidos 
# o los errores encontrados.

from lexer import clasificar_token, verificar_alfabeto

#es para centrar en la terminal y para que se muestre el menú
def encabezado():

    print("=" * 60)
    print("SMART HOME LEXER".center(60))
    print("Analizador Léxico".center(60))
    print("=" * 60)

    print()
    print("Ingrese líneas de código Smart Home.")
    print("Escriba SALIR para finalizar.")
    print()


encabezado()

while True:

    linea = input("> ")

    simbolo_invalido = verificar_alfabeto(linea)

    if simbolo_invalido is not None:
        print(f"Error léxico: símbolo inválido '{simbolo_invalido}'")
        continue

    if linea.upper() == "SALIR":
        print("\nFin del programa.")
        break

    palabras = linea.split()

    print("\nTokens encontrados:\n")

    for palabra in palabras:

        token = clasificar_token(palabra)

        if token:
            print(f"• {token}")

        else:
            print(f"• ERROR: {palabra}")

    print()