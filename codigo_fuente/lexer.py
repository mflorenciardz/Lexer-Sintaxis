# Contiene la lógica principal del proyecto. Se encarga de recorrer el código fuente del lenguaje Smart Home 
# y reconocer los distintos tokens definidos por la gramática.

#Su función es transformar una secuencia de caracteres en una secuencia de tokens.

import tokens

# Busca si la palabra es una reservada del Lenguaje
#si la encuentra, devuelve TOKEN_X
def reservada(palabra):
    palabra = palabra.upper()

    if palabra in tokens.PALABRAS_RESERVADAS:
        return f"TOKEN_{palabra}"
    return None

# Esto es para ver a qué categoría pertenece cada token.

# Devuelven True o False según corresponda.
def es_booleano(token):
    token = token.upper()

    if token in tokens.BOOLEANOS:
        return True
    return False

def es_operador(token):
    if token in tokens.OPERADORES:
        return True
    return False 

def es_numero(token):
    if token.isdigit():
        return True
    return False

def es_sensor(token):
    if token in tokens.SENSORES:
        return True
    return False

# Como los actuadores pueden llamarse foco_, reloj_, etc.,
# alcanza con revisar que empiecen con alguno de los prefijos definidos.
def es_actuador(token):
    for prefijo in tokens.PREFIJO_ACTUADORES:
        if token.startswith(prefijo):
            return True
    return False


# Acá definimos qué caracteres están permitidos en el lenguaje.
# Esto se usa antes de clasificar tokens para detectar símbolos tipo $&|.
def simbolo_valido(caracter):
    if caracter.isalpha():
        return True
    if caracter.isdigit():
        return True
    if caracter in tokens.SIMBOLOS:
        return True
    if caracter == " ":
        return True
    if caracter == "_":
        return True
    return False

# Recorremos toda la línea buscando caracteres inválidos.
# Si estamos dentro de una cadena ignoramos lo que haya adentro
# porque forma parte del mensaje y no del código.
def verificar_alfabeto(texto):

    simbolos_invalidos = []

    dentro_cadena = False

    for caracter in texto:

        if caracter == '"':
            dentro_cadena = not dentro_cadena
            continue

        if dentro_cadena:
            continue

        if not simbolo_valido(caracter):
            simbolos_invalidos.append(caracter)

    return simbolos_invalidos


# A partir de acá empiezan las validaciones de cada tipo de dato.
# La idea es revisar que tengan el formato correcto.


# Un mail tiene que tener un solo @ y algo antes y después.
# También revisamos que el dominio tenga un punto.
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
    
# Revisamos que la hora tenga formato HH:MM y que los valores tengan sentido.
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

# Revisamos que la fecha tenga formato DD/MM/AAAA.
# Por ahora controlamos rangos generales, no meses específicos.
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

# La temperatura tiene que terminar en °C.
# También permitimos temperaturas negativas.
def validar_temperatura(temp):
    if not temp.endswith("°C"):
        return False 
    
    grados = temp[:-2];

    if grados.startswith("-"):
        grados = grados[1:]
    
    if not grados.isdigit():
        return False 
    
    return True

# Un porcentaje tiene que terminar en % y estar entre 0 y 100.
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

# Una cadena tiene que empezar y terminar con comillas.
def validar_cadena(cadena):
    if not cadena.endswith('"'):
        return False
    if not cadena.startswith('"'):
        return False
    
    return True

# Las mediciones de luz se expresan en lux.
# Revisamos que la parte numérica sea válida.
def validar_luz(luz):

    if not luz.endswith("lux"):
        return False

    cantidad = luz[:-3]

    if not cantidad.isdigit():
        return False

    return True


# Va recorriendo la línea carácter por carácter y armando los tokens
#acá resolvemos cosas que un split() no puede manejar
#separarla en tokens respetando cadenas entre comillas, comentarios y atributos.
def tokenizar(linea):

    lista_tokens = []
    actual = ""

    i = 0

    while i < len(linea):

        caracter = linea[i]

        #para cadenas tipo "Hola"
        if caracter == '"':

            if actual != "":
                lista_tokens.append(actual)
                actual = ""

            cadena = '"'

            i += 1

            while i < len(linea):

                cadena += linea[i]

                if linea[i] == '"':
                    break

                i += 1

            lista_tokens.append(cadena)

            i += 1

            continue

        #con los comentarios que son //
        if caracter == "/" and i + 1 < len(linea):

            if linea[i + 1] == "/":

                if actual != "":
                    lista_tokens.append(actual)

                comentario = linea[i:]

                lista_tokens.append(comentario)

                break

        #también tenemos que ver los espacios:
        if caracter == " ":

            if actual != "":
                lista_tokens.append(actual)
                actual = ""

            i += 1
            continue

        #hay que separa actuador y atributo con el puntoq tienen en el medio
        if caracter == ".":

            if actual != "":
                lista_tokens.append(actual)
                actual = ""

            lista_tokens.append(".")

            i += 1
            continue

        actual += caracter

        i += 1

    #agrega el último token si quedó algo pendiente
    if actual != "":
        lista_tokens.append(actual)

    return lista_tokens

# Un comentario empieza con // y se ignora hasta el final de la línea.
def es_comentario(token):
    if token.startswith("//"):
        return True
    return False

#ve si el texto corresponde a alguno de los atributos con los actuadores.
def es_atributo(token):

    token = token.upper()

    if token in tokens.ATRIBUTOS:
        return True

    return False


#es para saber qué es cada token.
#Va probando categoría por categoría hasta encontrar la que es igual
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
    
    if es_comentario(token):
        return "TOKEN_COMENTARIO"

    if token == ".":
        return "TOKEN_PUNTO"
 
    if es_atributo(token):
        return f"TOKEN_{token.upper()}"

    return None

#si no se clasificó el tkn, vemos qué prodría haber sido
#así mostramos un mensaje de error más específico
def tipo_error(token):

    if "@" in token:
        return "EMAIL"

    if ":" in token:
        return "HORA"
    
    if token.startswith("//"):
        return "COMENTARIO"

    if "/" in token:
        return "FECHA"

    if token.endswith("°C"):
        return "TEMPERATURA"

    if token.endswith("%"):
        return "PORCENTAJE"

    if token.startswith('"') or token.endswith('"'):
        return "CADENA"

    return "TOKEN"

