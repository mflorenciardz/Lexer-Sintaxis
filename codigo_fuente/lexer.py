# Contiene la lógica principal del proyecto. Se encarga de recorrer el código fuente del lenguaje Smart Home 
# y reconocer los distintos tokens definidos por la gramática.

#Su función es transformar una secuencia de caracteres en una secuencia de tokens.

from tokens import PALABRAS_RESERVADAS, OPERADORES

#la función reservada devuelve cada palabra con el token_ delante o none
def reservada(palabra):
    palabra = palabra.upper()

    if palabra in PALABRAS_RESERVADAS:
        return f"TOKEN_{palabra}"
    return None

#la función simbolo_valido devuelve verdadero o falso si, caraccter por caracte, es valido.
#ve si es una letra, un número, o si es parte de los operadores
def simbolo_valido(caracter):
    if caracter.isalpha():
        return True
    if caracter.isdigit():
        return True
    if caracter in OPERADORES:
        return True
    if caracter == " ":
        return True
    return False

#aca verificamos si está bien cada palabra en donde está
def verificar_valido_contexto(texto):
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

    if grados.startswitch("-"):
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
