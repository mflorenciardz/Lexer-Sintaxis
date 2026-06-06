# Manejo de errores léxicos.
# Muestra:
#   - Tipo de error.
#   - Línea donde ocurrió.

def encabezado_error(linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>")
    print(f"Línea: {linea}")

def error_token(token, linea):
    encabezado_error(linea)
    print(f"Token desconocido: {token}\n")

def error_simbolo(simbolo, linea):
    encabezado_error(linea)
    print(f"Símbolo inválido: {simbolo}\n")

def error_hora(hora, linea):
    encabezado_error(linea)
    print(f"Hora no válida: {hora}\n")

def error_fecha(fecha, linea):
    encabezado_error(linea)
    print(f"Fecha no válida: {fecha}\n")

def error_temp(temp, linea):
    encabezado_error(linea)
    print(f"Temperatura inválida: {temp}\n")

def error_email(mail, linea):
    encabezado_error(linea)
    print(f"Email inválido: {mail}\n")

def error_cadena(cadena, linea):
    encabezado_error(linea)
    print(f"Cadena sin cerrar: {cadena}\n")

def error_porcentaje(percent, linea):
    encabezado_error(linea)
    print(f"Porcentaje inválido: {percent}\n")

def error_actuador_sin_id(token, linea):
    encabezado_error(linea)
    print(f"Actuador sin identificador: '{token}'")
    print(f"  Se esperaba un nombre después del prefijo. Ej: reloj_cocina\n")

def error_id_invalido(token, linea):
    encabezado_error(linea)
    print(f"Identificador inválido en actuador: '{token}'")
    print(f"  El ID solo puede contener letras, dígitos y guiones bajos,")
    print(f"  y no puede comenzar con un dígito. Ej: foco_patio, reloj_1er_piso\n")
