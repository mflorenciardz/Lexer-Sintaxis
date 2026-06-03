# Archivo principal del programa.

#Es el encargado de iniciar la ejecución del lexer. 
#Lee el texto ingresado por el usuario o el archivo de prueba y muestra los tokens reconocidos 
# o los errores encontrados.

from lexer import (
    tokenizar,
    clasificar_token,
    tipo_error,
    verificar_alfabeto
)

import errores


ERRORES = {
    "EMAIL": errores.error_email,
    "HORA": errores.error_hora,
    "FECHA": errores.error_fecha,
    "TEMPERATURA": errores.error_temp,
    "PORCENTAJE": errores.error_porcentaje,
    "CADENA": errores.error_cadena
}


def encabezado():

    print("=" * 60)
    print("SMART HOME LEXER".center(60))
    print("Analizador Léxico".center(60))
    print("=" * 60)

    print()
    print("Ingrese código Smart Home.")
    print("Escriba SALIR para finalizar.")
    print()


encabezado()

linea_actual = 1

while True:

    linea = input(f"[{linea_actual}] > ")

    if linea.upper() == "SALIR":
        print("\nFin del programa.")
        break

    simbolo = verificar_alfabeto(linea)

    if simbolo is not None:

        errores.error_simbolo(simbolo, linea_actual)

        linea_actual += 1
        continue

    lista_tokens = tokenizar(linea)

    print("\nTokens encontrados:\n")

    for token_original in lista_tokens:

        token = clasificar_token(token_original)

        if token == "TOKEN_COMENTARIO":

            print(f"• {token}")
            break

        elif token is not None:

            print(f"• {token}")

        else:

            tipo = tipo_error(token_original)

            funcion_error = ERRORES.get(tipo)

            if funcion_error is not None:

                funcion_error(token_original, linea_actual)

            else:

                errores.error_token(token_original, linea_actual)

    print()

    linea_actual += 1