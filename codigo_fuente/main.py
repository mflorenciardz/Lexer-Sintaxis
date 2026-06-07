# acá no se analiza nada, sino que le va pasando el trabajo al lexer
# y se muestran los resultados

import json

from lexer import (
    tokenizar,
    clasificar_token,
    tipo_error,
    verificar_alfabeto
)

import errores

# relaciona cada tipo de error con la función que lo muestra
ERRORES = {
    "EMAIL": errores.error_email,
    "HORA": errores.error_hora,
    "FECHA": errores.error_fecha,
    "TEMPERATURA": errores.error_temp,
    "PORCENTAJE": errores.error_porcentaje,
    "CADENA": errores.error_cadena,
    "ACTUADOR_SIN_ID": errores.error_actuador_sin_id,
    "ID_INVALIDO": errores.error_id_invalido,
}


# lee un archivo json y devuelve la lista de casos de prueba
def leer_json(nombre_archivo):

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:

        datos = json.load(archivo)

    return datos["casos"]


# toda la lógica del análisis quedó acá para no repetir código
def analizar_linea(linea, linea_actual):

    # primero vemos si hay caracteres que no pertenecen al lenguaje
    simbolos_invalidos = verificar_alfabeto(linea)

    for simbolo in simbolos_invalidos:
        errores.error_simbolo(simbolo, linea_actual)

    # separamos la línea en tokens
    lista_tokens = tokenizar(linea)

    print("\nTokens encontrados:\n")

    for token_original in lista_tokens:

        token = clasificar_token(token_original)

        # si aparece un comentario, mostramos el token y dejamos de analizar
        if token == "TOKEN_COMENTARIO":

            print(f"• {token}  →  {token_original}")
            break

        elif token is not None:

            print(f"• {token}")

        else:

            # si no reconocimos el token intentamos averiguar el error
            tipo = tipo_error(token_original)

            funcion_error = ERRORES.get(tipo)

            if funcion_error is not None:

                funcion_error(token_original, linea_actual)

            else:

                errores.error_token(token_original, linea_actual)

    print()


# muestra el encabezado del programa
def encabezado():

    print("=" * 60)
    print("SMART HOME LEXER".center(60))
    print("Analizador Léxico".center(60))
    print("=" * 60)

    print()


# INICIO DEL PROGRAMA
encabezado()

print("1 - Modo interactivo")
print("2 - Ejecutar pruebas JSON")
print()

opcion = input("Opción: ")

linea_actual = 1

# modo normal: el usuario escribe línea por línea
if opcion == "1":

    print()
    print("Ingrese código Smart Home.")
    print("Escriba SALIR para finalizar.")
    print()

    while True:

        linea = input(f"[{linea_actual}] > ")

        if linea.upper() == "SALIR":

            print("\nFin del programa.")
            break

        analizar_linea(linea, linea_actual)

        linea_actual += 1


# modo pruebas: lee los ejemplos desde un json
elif opcion == "2":

    print("\nArchivos disponibles:")
    print("1 - pruebas_validas.json")
    print("2 - pruebas_invalidas.json")

    opcion_archivo = input("\nOpción: ")

    if opcion_archivo == "1":
        archivo = "../pruebas/pruebas_validas.json"

    elif opcion_archivo == "2":
        archivo = "../pruebas/pruebas_invalidas.json"

    else:
        print("Opción inválida.")
        exit()

    try:

        lineas = leer_json(archivo)

        for linea in lineas:

            print(f"\n[{linea_actual}] > {linea}")

            analizar_linea(linea, linea_actual)

            linea_actual += 1

        print("Fin de las pruebas.")

        input("\nPresione ENTER para cerrar...")

    except FileNotFoundError:

        print("No se encontró el archivo.")

        input("\nPresione ENTER para cerrar...")

    except Exception as error:

        print(f"Error al leer el JSON: {error}")


else:

    print("Opción inválida.")