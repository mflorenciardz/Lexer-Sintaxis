# Contiene la lógica principal del proyecto. Se encarga de recorrer el código fuente del lenguaje Smart Home 
# y reconocer los distintos tokens definidos por la gramática.

#Su función es transformar una secuencia de caracteres en una secuencia de tokens.

from tokens import PALABRAS_RESERVADAS, SIMBOLOS, BOOLEANOS, OPERADORES, SENSORES, PREFIJO_ACUTADORES

#la función reservada devuelve cada palabra con el token_ delante o none
def reservada(palabra):
    palabra = palabra.upper()

    if palabra in PALABRAS_RESERVADAS:
        return f"TOKEN_{palabra}"
    return None

def es_booleano(token):
    token = token.upper()

    if token in BOOLEANOS:
        return True
    return False

def es_operador(token):
    if token in OPERADORES:
        return True
    return False 

def es_numero(token):
    if token.isdigit():
        return True
    return False

def es_sensor(token):
    if token in SENSORES:
        return True
    return False

def es_actuador(token):
    for prefijo in PREFIJO_ACUTADORES:
        if token.startswith(prefijo):
            return True
    return False

def es_comentario(token):
    if token.startswith("//"):
        return True
    return False

#la función simbolo_valido devuelve verdadero o falso si, caraccter por caracte, es valido.
#ve si es una letra, un número, o si es parte de los operadores
def simbolo_valido(caracter):
    if caracter.isalpha():
        return True
    if caracter.isdigit():
        return True
    if caracter in SIMBOLOS:
        return True
    if caracter == " ":
        return True
    return False

#aca verificamos si está bien cada palabra en donde está
def verificar_alfabeto(texto):
    for caracter in texto: 
        if not simbolo_valido(caracter):
            return caracter
    return None

def validar_email(email):
    if email.count("@") != 1:
        return False
    
    analizar = email.split("@");
    usuario = analizar[0];
    dominio = analizar[1];

    if usuario == "":
        return False
    if dominio == "":
        return False
    
    if "." not in dominio:
        return False 
    if dominio.startswith("."):
        return False
    if dominio.endswith("."):
        return False 
    return True
    
def validar_hora(hora):
    if hora.count(":") != 1:
        return False
    
    analizar = hora.split(":");
    horas = analizar[0];
    minutos = analizar[1];

    if not horas.isdigit():
        return False
    if not minutos.isdigit():
        return False 
    
    horas = int(horas);
    minutos = int(minutos);

    if (horas < 0) or (horas > 23):
        return False
    if (minutos > 59) or (minutos < 0):
        return False
    
    return True

def validar_fecha(fecha):
    if fecha.count("/") != 2:
        return False
    
    analizar = fecha.split("/");
    dia = analizar[0];
    mes = analizar[1];
    anno = analizar[2];

    if not dia.isdigit():
        return False 
    if not mes.isdigit():
        return False 
    if not anno.isdigit():
        return False 
    
    dia = int(dia);
    mes = int(mes);
    anno = int(anno);

    if (dia > 31) or (dia < 1):
        return False
    if (mes > 12) or (mes < 1):
        return False
    if (anno > 2099) or (anno < 1990):
        return False 
    
    return True

def validar_temperatura(temp):
    if not temp.endswith("°C"):
        return False 
    
    grados = temp[:-2];

    if grados.startswith("-"):
        grados = grados[1:]
    
    if not grados.isdigit():
        return False 
    
    return True

def validar_porcentaje(percent):
    if not percent.endswith("%"):
        return False
    
    percent = percent[:-1];

    if not percent.isdigit():
        return False 
    
    percent = int(percent)

    if (percent > 100) or (percent < 0):
        return False
    
    return True

def validar_cadena(cadena):
    if not cadena.endswith('"'):
        return False
    if not cadena.startswith('"'):
        return False
    
    return True

def validar_luz(luz):

    if not luz.endswith("lux"):
        return False

    cantidad = luz[:-3]

    if not cantidad.isdigit():
        return False

    return True


def clasificar_token(token):

    reservado = reservada(token)

    if reservado is not None:
        return reservado

    if es_booleano(token):
        return f"TOKEN_{token.upper()}"

    if es_sensor(token):
        return f"TOKEN_{token.upper()}"

    if es_actuador(token):
        return "TOKEN_ACTUADOR"
    
    if es_comentario(token):
        return "TOKEN_COMENTARIO"

    if token == ">=":
        return "TOKEN_MAYOR_IGUAL"

    if token == "<=":
        return "TOKEN_MENOR_IGUAL"

    if token == "==":
        return "TOKEN_IGUALDAD"

    if token == "!=":
        return "TOKEN_DISTINTO"

    if token == ">":
        return "TOKEN_MAYOR"

    if token == "<":
        return "TOKEN_MENOR"

    if token == "=":
        return "TOKEN_ASIGNACION"

    if es_numero(token):
        return "TOKEN_NUMERO"

    if validar_email(token):
        return "TOKEN_EMAIL"

    if validar_hora(token):
        return "TOKEN_HORA"

    if validar_fecha(token):
        return "TOKEN_FECHA"

    if validar_temperatura(token):
        return "TOKEN_TEMPERATURA"

    if validar_porcentaje(token):
        return "TOKEN_PORCENTAJE"

    if validar_cadena(token):
        return "TOKEN_CADENA"
    
    if validar_luz(token):
        return "TOKEN_LUZ"

    return None

def tipo_error(token):

    if "@" in token:
        return "EMAIL"

    if ":" in token:
        return "HORA"

    if "/" in token:
        return "FECHA"

    if token.endswith("°C"):
        return "TEMPERATURA"

    if token.endswith("%"):
        return "PORCENTAJE"

    if token.startswith('"') or token.endswith('"'):
        return "CADENA"

    return "TOKEN"