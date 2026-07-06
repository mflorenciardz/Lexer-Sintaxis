# buscamos automáticamente la carpeta principal del proyecto para que
# el programa encuentre los archivos aunque se ejecute desde otro lugar
from pathlib import Path
from traductorHTML import traducir

import sys

if getattr(sys, "frozen", False):
    BASE = Path(sys.executable).parent.parent
else:
    BASE = Path(__file__).parent.parent

from lexer import (
    tokenizar,
    clasificar_token,
    tipo_error,
    verificar_alfabeto
)

from parser import Parser

import errores

# relaciona cada tipo de error con la función que lo muestra
ERRORES = {
    "EMAIL": errores.error_email,
    "HORA": errores.error_hora,
    "FECHA": errores.error_fecha,
    "TEMPERATURA": errores.error_temp,
    "PORCENTAJE": errores.error_porcentaje,
    "TIEMPO": errores.error_tiempo,
    "LUZ": errores.error_luz,
    "CADENA": errores.error_cadena,
    "ACTUADOR_SIN_ID": errores.error_actuador_sin_id,
    "ID_INVALIDO": errores.error_id_invalido,
}

# lee un archivo .smart y devuelve todas sus líneas
def leer_archivo(nombre_archivo):

    if not nombre_archivo.endswith(".smart"):
        nombre_archivo += ".smart"

    ruta = BASE / "pruebas" / nombre_archivo

    lineas = []

    with open(ruta, "r", encoding="utf-8") as archivo:

        for linea in archivo:

            linea = linea.strip()

            if linea != "":

                lineas.append(linea)

    return lineas

def listar_archivos():

    carpeta = BASE / "pruebas"

    archivos = sorted(carpeta.glob("*.smart"))

    if len(archivos) == 0:

        print("\nNo hay archivos .smart en la carpeta pruebas.")

        return None

    print("\nArchivos disponibles:\n")

    for i, archivo in enumerate(archivos, start=1):

        print(f"{i} - {archivo.stem}")

    while True:

        try:

            opcion = int(input("\nSeleccione un archivo: "))

            if 1 <= opcion <= len(archivos):

                return archivos[opcion - 1].name

            print("Opción inválida.")

        except ValueError:

            print("Ingrese un número.")

# toda la lógica del análisis quedó acá para no repetir código
def analizar_linea(linea, linea_actual):

    # primero vemos si hay caracteres que no pertenecen al lenguaje
    simbolos_invalidos = verificar_alfabeto(linea)

    hubo_error = False

    for simbolo in simbolos_invalidos:

        errores.error_simbolo(simbolo, linea_actual)
        hubo_error = True

    # separamos la línea en tokens
    lista_tokens = tokenizar(linea)

    tokens_parser = []

    print("\nTokens encontrados:\n")

    for token_original in lista_tokens:

        token = clasificar_token(token_original)

        # comentario
        if token == "TOKEN_COMENTARIO":

            print(f"• {token}  →  {token_original}")
            break

        elif token is not None:

            tokens_parser.append((token, linea_actual))

            print(f"• {token}")

        else:

            hubo_error = True

            tipo = tipo_error(token_original)

            funcion_error = ERRORES.get(tipo)

            if funcion_error is not None:

                funcion_error(token_original, linea_actual)

            else:

                errores.error_token(token_original, linea_actual)

    print()

    return tokens_parser, hubo_error

# muestra el encabezado del programa
def encabezado():

    print("=" * 60)
    print("SMART HOME".center(60))
    print("Analizador Léxico".center(60))
    print("=" * 60)

    print()


# INICIO DEL PROGRAMA
encabezado()

print("1 - Modo interactivo")
print("2 - Leer archivo .smart ")
print()

opcion = input("Opción: ")

linea_actual = 1

# modo normal: el usuario escribe línea por línea
if opcion == "1":

    print()
    print("Ingrese código Smart Home.")
    print("Escriba SALIR para finalizar.")
    print()

    tokens_programa = []

    while True:

        linea = input(f"[{linea_actual}] > ")

        if linea.upper() == "SALIR":

            print("\nFin del programa.")
            break

        tokens, hubo_error = analizar_linea(linea, linea_actual)

        if not hubo_error:

            tokens_programa.extend(tokens)

            parser = Parser(tokens_programa)

            parser.programa()

        linea_actual += 1
#modo con archivo
elif opcion == "2":

    nombre = listar_archivos()

    if nombre is None:

        input("\nPresione ENTER para continuar...")

        exit()

    try:

        lineas = leer_archivo(nombre)

        tokens_programa = []

        for linea in lineas:

            print(f"\n[{linea_actual}] > {linea}")

            tokens, hubo_error = analizar_linea(linea, linea_actual)

            if not hubo_error:

                tokens_programa.extend(tokens)

            linea_actual += 1

        parser = Parser(tokens_programa)

        if parser.programa():

            traducir(lineas, nombre)

        print("\nFin del archivo.")

        input("\nPresione ENTER para cerrar...")

    except Exception as error:

        print(f"\nError al leer el archivo: {error}")

        input("\nPresione ENTER para continuar...")

else:

    print("Opción inválida.")
    input("\nPresione ENTER para cerrar...")
