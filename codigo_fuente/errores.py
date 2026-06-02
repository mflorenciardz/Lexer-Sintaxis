#Manejo de errores léxicos.

#Contiene las funciones necesarias para detectar y reportar errores durante el análisis léxico.

#Debe indicar:

#Tipo de error.
#Línea donde ocurrió.
#Cadena o símbolo que produjo el error.

def error_token(token, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"token desonocido {token}\n")

def error_simbolo(operador, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"símbolo inválido {operador}\n")

def error_hora(hora, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"Hora no válida {hora}\n")

def error_fecha(fecha, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"Fecha no válida {fecha}\n")

def error_temp(temp, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"temperatura inválida {temp}\n")

def error_email(mail, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"error {mail}\n")

def erro_cadena(string, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"no cerró el string {string}\n")

def error_porcentaje(percent, linea):
    print("<<<<<<< ERROR LÉXICO >>>>>>>\n");
    print(f"Línea: {linea}\n");
    print(f"error en {percent}\n")

