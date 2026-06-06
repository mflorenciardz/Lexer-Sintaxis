# acá no se analiza nada, sino que le va pasando el trabajo por lexer y se muestra el rtdo

from lexer import (
    tokenizar,
    clasificar_token,
    tipo_error,
    verificar_alfabeto
)

import errores

# acá hice como un diccionario para relacionar digamos cada tipo de error
# con la función que lo muestra por pantalla.
ERRORES = {
    "EMAIL":           errores.error_email,
    "HORA":            errores.error_hora,
    "FECHA":           errores.error_fecha,
    "TEMPERATURA":     errores.error_temp,
    "PORCENTAJE":      errores.error_porcentaje,
    "CADENA":          errores.error_cadena,
    "ACTUADOR_SIN_ID": errores.error_actuador_sin_id,
    "ID_INVALIDO":     errores.error_id_invalido,
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

# mostramos menú
encabezado()

# empezamos un contador así vamos contando las líneas para poder
# saber dónde está cada error
linea_actual = 1

# no termina el programa hasta que se ponga SALIR
while True:

    linea = input(f"[{linea_actual}] > ")

    if linea.upper() == "SALIR":
        print("\nFin del programa.")
        break

    # primero vemos si no hay algun caracter que no pertenezca
    simbolos_invalidos = verificar_alfabeto(linea)

    # si aparece un simbolo no valido, mostramos el error
    for simbolo in simbolos_invalidos:
        errores.error_simbolo(simbolo, linea_actual)

    # es más que nada por los casos con los actuadores.atributo
    # esto los separa así vemos si está bien escrito el actuador y el atributo
    lista_tokens = tokenizar(linea)

    print("\nTokens encontrados:\n")

    for token_original in lista_tokens:

        token = clasificar_token(token_original)

        # si encontramos un comentario, lo mostramos y dejamos de analizar
        # porque el resto de la línea ya forma parte del comentario
        if token == "TOKEN_COMENTARIO":
            print(f"• {token}  →  {token_original}")
            break

        elif token is not None:
            print(f"• {token}")

        else:
            # si no pudimos clasificar el token, intentamos averiguar qué tipo de error es
            tipo = tipo_error(token_original)
            funcion_error = ERRORES.get(tipo)

            if funcion_error is not None:
                funcion_error(token_original, linea_actual)
            else:
                errores.error_token(token_original, linea_actual)

    print()
    
    # pasamos a la siguiente línea ingresada por el usuario
    linea_actual += 1
