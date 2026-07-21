# Contiene la lógica principal del proyecto. Se encarga de recorrer el código fuente del lenguaje Smart Home
# y reconocer los distintos tokens definidos por la gramática.
# Su función es transformar una secuencia de caracteres en una secuencia de tokens.

import tokens

# Busca si la palabra es una reservada del Lenguaje
# si la encuentra, devuelve TOKEN_X
def reservada(palabra):
    palabra = palabra.upper()
    if palabra in tokens.PALABRAS_RESERVADAS:
        return f"TOKEN_{palabra}"
    return None

def es_booleano(token):
    return token.upper() in tokens.BOOLEANOS

def es_operador(token):
    return token in tokens.OPERADORES

def es_numero(token):
    return token.isdigit()

# Sensores numéricos: temperatura, humedad, luz.
# Admiten cualquier operador de comparación (incluye <, >, <=, >=).
def es_sensor_num(token):
    return token.lower() in tokens.SENSORES_NUM

# Sensores booleanos: humo, movimiento.
# Solo admiten operadores de igualdad (== y !=).
def es_sensor_bool(token):
    return token.lower() in tokens.SENSORES_BOOL

# Colores en español 
def es_color(token):
    return token.lower() in tokens.COLORES

# Modos del aire acondicionado
def es_modo(token):
    return token.lower() in tokens.MODOS

# Devuelve el prefijo que tiene el token, o None si no es un actuador.
def prefijo_actuador(token):
    token_lower = token.lower()
    for prefijo in tokens.PREFIJO_ACTUADORES:
        if token_lower.startswith(prefijo):
            return prefijo
    return None

# Verifica que el token sea un actuador con ID válido.
# Forma esperada: PREFIJO + ID, donde ID es al menos un carácter alfanumérico o guion bajo.
def es_actuador(token):
    prefijo = prefijo_actuador(token)
    if prefijo is None:
        return False
    id_parte = token[len(prefijo):]
    return len(id_parte) > 0 and es_id_valido(id_parte)

# El ID solo puede contener letras, dígitos y guiones bajos.
# No puede estar vacío ni empezar con dígito.
def es_id_valido(texto):
    if not texto:
        return False
    for c in texto:
        if not (c.isalpha() or c.isdigit() or c == "_"):
            return False
    return True

# Dado un token actuador válido, extrae solo la parte del ID.
def extraer_id(token):
    prefijo = prefijo_actuador(token)
    if prefijo is None:
        return None
    return token[len(prefijo):]

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

    for i, caracter in enumerate(texto):
        if caracter == '"':
            dentro_cadena = not dentro_cadena
            continue
        if dentro_cadena:
            continue
        # A partir de un comentario, el resto de la línea es texto libre y no debe validarse contra el alfabeto del lenguaje
        if caracter == "/" and i + 1 < len(texto) and texto[i + 1] == "/":
            break
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
    analizar = email.split("@")
    usuario = analizar[0]
    dominio = analizar[1]
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
    analizar = hora.split(":")
    horas = analizar[0]
    minutos = analizar[1]
    if not horas.isdigit():
        return False
    if not minutos.isdigit():
        return False
    horas = int(horas)
    minutos = int(minutos)
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
    analizar = fecha.split("/")
    dia = analizar[0]
    mes = analizar[1]
    anno = analizar[2]
    if not dia.isdigit():
        return False
    if not mes.isdigit():
        return False
    if not anno.isdigit():
        return False
    dia = int(dia)
    mes = int(mes)
    anno = int(anno)
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
    grados = temp[:-2]
    negativo = grados.startswith("-")
    if negativo:
        grados = grados[1:]
    if not grados.isdigit():
        return False 
    valor = int(grados)
    if negativo:
        valor = -valor
    if (valor < -10) or (valor > 50): 
        return False 
    return True 

# Un porcentaje tiene que terminar en % y estar entre 0 y 100.
def validar_porcentaje(percent):
    if not percent.endswith("%"):
        return False
    percent = percent[:-1]
    if not percent.isdigit():
        return False
    percent = int(percent)
    if (percent > 100) or (percent < 0):
        return False
    return True

# El tiempo (usado en EVERY) se expresa como un número seguido de una única unidad (s, m, h)
def validar_tiempo(tiempo):
    if not tiempo: 
        return False 
    unidad = tiempo[-1]
    if unidad not in ("s", "m", "h"):
        return False 
    cantidad = tiempo[:-1]
    if not cantidad.isdigit():
        return False
    return True

# Determina si un token son dígitos seguidos de letras
def es_tiempo(token):
    i = 0 
    while i < len(token) and token[i].isdigit():
        i += 1 
    if i == 0:
        return False 
    resto = token[i:]
    if resto == "":
        return False
    return resto.isalpha()

# Una cadena tiene que empezar y terminar con comillas.
def validar_cadena(cadena):
    if not cadena.startswith('"'):
        return False
    if not cadena.endswith('"'):
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
    cantidad = int(cantidad)
    if (cantidad > 1000) or (cantidad < 0):
        return False
    return True

# Va recorriendo la línea carácter por carácter y armando los tokens
# acá resolvemos cosas que un split() no puede manejar
# separarla en tokens respetando cadenas entre comillas, comentarios y atributos.
def tokenizar(linea):
    lista_tokens = []
    actual = ""
    i = 0

    while i < len(linea):
        caracter = linea[i]

        # Cadenas tipo "Hola mundo"
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

        # Comentarios que empiezan con //
        if caracter == "/" and i + 1 < len(linea) and linea[i + 1] == "/":
            if actual != "":
                lista_tokens.append(actual)
            lista_tokens.append(linea[i:])
            break

        # Espacios separan tokens
        if caracter == " ":
            if actual != "":
                lista_tokens.append(actual)
                actual = ""
            i += 1
            continue

        # El punto separa el nombre del actuador de su atributo
        if caracter == "." and "@" not in actual:
            if actual != "":
                lista_tokens.append(actual)
                actual = ""
            lista_tokens.append(".")
            i += 1
            continue

        # Los operadores separan tokens aunque estén pegados al valor/identificador
        if caracter in ("=", "<", ">", "!"):
            if actual != "":
                lista_tokens.append(actual)
                actual = ""
            operador = caracter 
            if i + 1 < len(linea) and linea[i + 1] == "=":
                operador += "="
                i += 1 
            lista_tokens.append(operador)
            i += 1
            continue
        
        actual += caracter
        i += 1

    # Agrega el último token si quedó algo pendiente
    if actual != "":
        lista_tokens.append(actual)

    return lista_tokens

def es_comentario(token):
    return token.startswith("//")

def es_atributo(token):
    return token.upper() in tokens.ATRIBUTOS

# es para saber qué es cada token.
# Va probando categoría por categoría hasta encontrar la que es igual
def clasificar_token(token):

    # Palabras reservadas (WHEN, IF, DO, etc.)
    reservado = reservada(token)

    if reservado is not None:
        
        return reservado

    # Booleanos (TRUE, FALSE, ON, OFF)
    if es_booleano(token):

        return f"TOKEN_{token.upper()}"

    # Sensores numéricos (sensor_temp, sensor_humedad, sensor_luz)
    if es_sensor_num(token):

        return f"TOKEN_SENSOR_NUM({token.upper()})"
    
    # Colores en español 
    if es_color(token):
        return f"TOKEN_COLOR_VALOR({token.upper()})"
    
    if es_modo(token):
        return f"TOKEN_MODO_VALOR({token.upper()})"

    # Sensores booleanos (sensor_humo, sensor_movimiento)
    if es_sensor_bool(token):

        return f"TOKEN_SENSOR_BOOL({token.upper()})"

    # Actuadores con ID 
    # Si el ID falta o es inválido se devuelve None para que main lo trate como error.
    prefijo = prefijo_actuador(token)

    if prefijo is not None:

        id_parte = token[len(prefijo):]

        if id_parte == "":

            # Solo el prefijo sin ID → error ACTUADOR_SIN_ID
            return None
        
        elif es_id_valido(id_parte):

            return f"TOKEN_{token.upper()}"
        
        else:

            # Prefijo válido pero ID con caracteres inválidos → error ID_INVALIDO
            return None

    # Operadores compuestos (orden importa: >= antes que >)
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

    # Literales numéricos
    if es_numero(token):
        return "TOKEN_NUMERO"

    # Tipos de datos especiales
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
    if validar_tiempo(token):
        return "TOKEN_TIEMPO"
    if validar_cadena(token):
        return "TOKEN_CADENA"
    if validar_luz(token):
        return "TOKEN_LUZ"

    # Comentario
    if es_comentario(token):

        return "TOKEN_COMENTARIO"

    # Punto separador
    if token == ".":

        return "TOKEN_PUNTO"

    # Atributos de actuadores (ESTADO, BRILLO, COLOR, etc.)
    if es_atributo(token):

        return f"TOKEN_ATRIBUTO_{token.upper()}"

    return None

# si no se clasificó el tkn, vemos qué prodría haber sido
# así mostramos un mensaje de error más específico
def tipo_error(token):

    # Actuador con prefijo válido pero ID inválido
    prefijo = prefijo_actuador(token)

    if prefijo is not None:

        id_parte = token[len(prefijo):]

        if id_parte == "":

            return "ACTUADOR_SIN_ID"
        
        else:

            return "ID_INVALIDO"

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
    
    if token.endswith("lux"):
        return "LUZ"

    if es_tiempo(token):
        return "TIEMPO"

    return "TOKEN"
