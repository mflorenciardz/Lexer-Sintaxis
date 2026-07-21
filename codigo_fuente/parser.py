ATRIBUTOS_POR_TIPO_ACTUADOR = {
    "TOKEN_FOCO_":      ("TOKEN_ATRIBUTO_ESTADO", "TOKEN_ATRIBUTO_BRILLO", "TOKEN_ATRIBUTO_COLOR"),
    "TOKEN_AIRE_":      ("TOKEN_ATRIBUTO_ESTADO", "TOKEN_ATRIBUTO_MODO", "TOKEN_ATRIBUTO_TEMP_OBJ", "TOKEN_ATRIBUTO_TEMP_ACT"),
    "TOKEN_PERSIANA_":  ("TOKEN_ATRIBUTO_POSICION",),
    "TOKEN_CERRADURA_": ("TOKEN_ATRIBUTO_ESTADO",),
    "TOKEN_RELOJ_":     ("TOKEN_ATRIBUTO_HORA", "TOKEN_ATRIBUTO_FECHA"),
    "TOKEN_ALTAVOZ_":   ("TOKEN_ATRIBUTO_ESTADO", "TOKEN_ATRIBUTO_VOLUMEN", "TOKEN_ATRIBUTO_MUTE",
                         "TOKEN_ATRIBUTO_MENSAJE", "TOKEN_ATRIBUTO_EMAIL_NOTIF"),
    "TOKEN_ALARMA_":    ("TOKEN_ATRIBUTO_ESTADO", "TOKEN_ATRIBUTO_ACTIVADA"),
}

ATRIBUTOS_SOLO_LECTURA = ("TOKEN_ATRIBUTO_TEMP_ACT", "TOKEN_ATRIBUTO_HORA", "TOKEN_ATRIBUTO_FECHA")

# temp_obj solo admite 16°C a 30°C. Esta validación es semántica y no léxica, porque recién en el parser sabemos a qué atributo corresponde el valor asignado
RANGOS_ATRIBUTO = {
    "TOKEN_ATRIBUTO_TEMP_OBJ": (16, 30),
}

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens      # lista de tokens que produjo el lexer
        self.posicion = 0         # empezamos leyendo el primer token

        self.errores = []
        self.datos_sensores = {}
        self.datos_actuadores = {}

    def token_actual(self):
        if self.posicion < len(self.tokens): #Para evitar errores de posiciones fuera de listado
            return self.tokens[self.posicion][0]
        return None

    def linea_actual(self):

        if self.posicion < len(self.tokens):

            return self.tokens[self.posicion][1]

        return "desconocida"

    def avanzar(self):
        self.posicion += 1

    def error(self, mensaje):

        self.errores.append(mensaje)

    def recuperar(self):

        sincronizacion = (
            "TOKEN_END",
            "TOKEN_ELSE",
            "TOKEN_WHEN",
            "TOKEN_IF",
            "TOKEN_EVERY",
        )

        while (
            self.token_actual() is not None
            and self.token_actual() not in sincronizacion
        ):
            self.avanzar()

    # Ve si el token actual es el esperado
    def coincidir(self, esperado):

        if self.token_actual() == esperado:

            self.avanzar()

        else:

            self.error(
                f"Línea {self.linea_actual()}: "
                f"se esperaba {esperado} y se encontró {self.token_actual()}."
            )

            self.avanzar()

            self.recuperar()

    def programa(self):
        # Mientras queden tokens en el archivo, intentamos procesar
        while self.token_actual() is not None:
            if self.comienza_instruccion():
                self.instruccion()
            else:
                # Si se topa con algo que no sabe qué es, tira el error,
                # activa la recuperación para saltar al próximo bloque seguro y CONTINÚA
                self.error(
                    f"Línea {self.linea_actual()}: Componente inesperado o fuera de estructura: {self.token_actual()}."
                )
                self.recuperar()
                
                # Si después de recuperar sigue trabado en el mismo token, avanzamos uno a la fuerza
                if self.token_actual() is not None:
                    self.avanzar()

        if self.errores:
            print("\nErrores sintácticos/semánticos encontrados:\n")
            for error in self.errores:
                print("•", error)
            return False
        else:
            print("\n✓ Análisis sintáctico y semántico exitoso.")
            return True
    
    def comienza_instruccion(self):

        token = self.token_actual()

        if token is None:
            return False

        # Ignorar comentarios
        if token == "TOKEN_COMENTARIO":

            self.avanzar()

            return self.comienza_instruccion()

        if token == "TOKEN_ERROR_LEXICO":
            return True

        if token in (
            "TOKEN_WHEN",
            "TOKEN_IF",
            "TOKEN_EVERY",
        ):
            return True

        return self.es_actuador()

    def bloque(self):
        if not self.comienza_instruccion():
            self.error(
                f"Línea {self.linea_actual()}: "
                f"se esperaba al menos una instrucción en el bloque y se encontró {self.token_actual()}."
            )
            return
        
        while self.comienza_instruccion():
            self.instruccion()

    def instruccion(self):

        token = self.token_actual()

        if token == "TOKEN_WHEN":
            self.when()

        elif token == "TOKEN_IF":
            self.if_()

        elif token == "TOKEN_EVERY":
            self.every()

        elif token == "TOKEN_ERROR_LEXICO":
            self.avanzar()

        elif self.es_actuador():
            self.asignacion()

        else:
            self.error(
                f"Línea {self.linea_actual()}: "
                f"no se puede comenzar una instrucción con {token}."
            )

            self.recuperar()

            if self.token_actual is not None:
                self.avanzar()

    def when(self):

        self.coincidir("TOKEN_WHEN")

        self.condicion()

        self.coincidir("TOKEN_DO")

        self.bloque()

        self.coincidir("TOKEN_END")

    def if_(self):
        self.coincidir("TOKEN_IF")

        self.condicion()

        self.coincidir("TOKEN_THEN")

        self.bloque()

        if self.token_actual() == "TOKEN_ELSE":

            self.coincidir("TOKEN_ELSE")

            self.bloque()

        self.coincidir("TOKEN_END")

    def every(self):

        self.coincidir("TOKEN_EVERY")

        self.tiempo() 

        self.coincidir("TOKEN_DO")

        self.bloque()

        self.coincidir("TOKEN_END")

    def condicion(self):

        if self.token_actual() == "TOKEN_NOT":

            self.coincidir("TOKEN_NOT")

            self.condicion()

        else:

            self.expresion()

            if self.token_actual() == "TOKEN_AND":

                self.coincidir("TOKEN_AND")

                self.condicion()

            elif self.token_actual() == "TOKEN_OR":

                self.coincidir("TOKEN_OR")

                self.condicion()

    def es_actuador(self):

        token = self.token_actual()

        return (
            token is not None and (
                token.startswith("TOKEN_FOCO_")
                or token.startswith("TOKEN_AIRE_")
                or token.startswith("TOKEN_PERSIANA_")
                or token.startswith("TOKEN_CERRADURA_")
                or token.startswith("TOKEN_RELOJ_")
                or token.startswith("TOKEN_ALTAVOZ_")
                or token.startswith("TOKEN_ALARMA_")
            )
        )
    def tipo_de_actuador(self, token_actuador): 
        
        if token_actuador is None: 
            return None 
        
        for prefijo in ATRIBUTOS_POR_TIPO_ACTUADOR:

            if token_actuador.startswith(prefijo):

                return prefijo 
        
        return None 

    def asignacion(self):
       token_actuador_completo = self.token_actual() 
       atributo: None | str = self.actuador()  
       if atributo is None:
            return
       
       if atributo in ATRIBUTOS_SOLO_LECTURA:
            self.error(f"Línea {self.linea_actual()}: el atributo {atributo} es de solo lectura y no puede asignarse")
            self.recuperar()
            return
       
       self.coincidir("TOKEN_ASIGNACION")
       info = self.informacion_atributo(atributo)
       
       if info is None:
            self.error(f"Línea {self.linea_actual()}: Atributo desconocido: {atributo}.")
            self.recuperar()
            return

        # Antes de esperar el valor, miramos cuál es para guardarlo
        
       valor_token = self.token_actual()
       linea_valor = self.linea_actual()
       self.esperar_valor(info["valor"])

        # Validación semántica: temp_obj tiene un rango más estricto que el que ya validó el lexer (16°C a 30°C)
       self.validar_rango_atributo(atributo, valor_token, linea_valor)

        # Si no hubo errores, guardamos los datos limpios para el HTML
       if token_actuador_completo and valor_token:
            # Limpiamos los nombres sacando el prefijo "TOKEN_"
            actuador_nombre = token_actuador_completo.replace("TOKEN_", "").lower()
            atrib_nombre = atributo.replace("TOKEN_ATRIBUTO_", "").lower()
            # Si el valor viene como TOKEN_NUMERO(25) o TOKEN_TRUE, extraemos lo de adentro o el estado
            if "(" in valor_token and valor_token.endswith(")"):
                val_limpio = valor_token[valor_token.index("(") + 1 : -1]
            else:
                val_limpio = valor_token.replace("TOKEN_", "")
            if actuador_nombre not in self.datos_actuadores:
                self.datos_actuadores[actuador_nombre] = {}
            if atrib_nombre not in self.datos_actuadores[actuador_nombre]:
                self.datos_actuadores[actuador_nombre][atrib_nombre] = []
            if val_limpio not in self.datos_actuadores[actuador_nombre][atrib_nombre]:
                self.datos_actuadores[actuador_nombre][atrib_nombre].append(val_limpio)

    def actuador(self):
        # guardamos el actuador antes de avanzar
        token_actuador = self.token_actual() 
        if not self.es_actuador():

            self.error(
                f"Línea {self.linea_actual()}: "
                f"Se esperaba un actuador y se encontró {self.token_actual()}."
            )

            self.recuperar()

            return None

        self.avanzar()

        self.coincidir("TOKEN_PUNTO")

        atributo = self.atributo()
        if atributo is None: 
            return None 

        tipo = self.tipo_de_actuador(token_actuador)
        permitidos = ATRIBUTOS_POR_TIPO_ACTUADOR.get(tipo, ())
        if atributo not in permitidos:
            self.error(f"Línea {self.linea_actual()}: el atributo {atributo} no corresponde al actuador {token_actuador}.")
            self.recuperar()
            return None

        return atributo

    def atributo(self):

        token = self.token_actual()

        atributos = (
            "TOKEN_ATRIBUTO_ESTADO",
            "TOKEN_ATRIBUTO_BRILLO",
            "TOKEN_ATRIBUTO_COLOR",
            "TOKEN_ATRIBUTO_MODO",
            "TOKEN_ATRIBUTO_TEMP_OBJ",
            "TOKEN_ATRIBUTO_TEMP_ACT",
            "TOKEN_ATRIBUTO_POSICION",
            "TOKEN_ATRIBUTO_ACTIVADA",
            "TOKEN_ATRIBUTO_HORA",
            "TOKEN_ATRIBUTO_FECHA",
            "TOKEN_ATRIBUTO_VOLUMEN",
            "TOKEN_ATRIBUTO_MUTE",
            "TOKEN_ATRIBUTO_MENSAJE",
            "TOKEN_ATRIBUTO_EMAIL_NOTIF",
        )

        if token in atributos:

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un atributo y se encontró {token}."
        )

        self.recuperar()

        return None
    
    def informacion_atributo(self, atributo):

        atributos = {

            "TOKEN_ATRIBUTO_ESTADO": {
                "operador": "bool",
                "valor": ("TOKEN_TRUE", "TOKEN_FALSE", "TOKEN_ON", "TOKEN_OFF"),
            },

            "TOKEN_ATRIBUTO_ACTIVADA": {
                "operador": "bool",
                "valor": ("TOKEN_TRUE", "TOKEN_FALSE", "TOKEN_ON", "TOKEN_OFF"),
            },

            "TOKEN_ATRIBUTO_MUTE": {
                "operador": "bool",
                "valor": ("TOKEN_TRUE", "TOKEN_FALSE", "TOKEN_ON", "TOKEN_OFF"),
            },

            "TOKEN_ATRIBUTO_TEMP_OBJ": {
                "operador": "comp",
                "valor": ("TOKEN_TEMPERATURA",),
            },

            "TOKEN_ATRIBUTO_TEMP_ACT": {
                "operador": "comp",
                "valor": ("TOKEN_TEMPERATURA",),
            },

            "TOKEN_ATRIBUTO_POSICION": {
                "operador": "comp",
                "valor": ("TOKEN_PORCENTAJE",),
            },

            "TOKEN_ATRIBUTO_BRILLO": {
                "operador": "comp",
                "valor": ("TOKEN_PORCENTAJE",),
            },

            "TOKEN_ATRIBUTO_VOLUMEN": {
                "operador": "comp",
                "valor": ("TOKEN_PORCENTAJE",),
            },

            "TOKEN_ATRIBUTO_COLOR": {
                "operador": "bool",
                "valor": ("TOKEN_COLOR_VALOR",),
            },

            "TOKEN_ATRIBUTO_MODO": {
                "operador": "bool",
                "valor": ("TOKEN_MODO_VALOR",),
            },

            "TOKEN_ATRIBUTO_EMAIL_NOTIF": {
                "operador": "bool",
                "valor": ("TOKEN_EMAIL",),
            },

            "TOKEN_ATRIBUTO_MENSAJE": {
                "operador": "bool",
                "valor": ("TOKEN_CADENA",),
            },

            "TOKEN_ATRIBUTO_HORA": {
                "operador": "comp",
                "valor": ("TOKEN_HORA",),
            },

            "TOKEN_ATRIBUTO_FECHA": {
                "operador": "comp",
                "valor": ("TOKEN_FECHA",),
            },

        }

        return atributos.get(atributo)
    
    def informacion_sensor(self, sensor):

        sensores = {

            "TOKEN_SENSOR_NUM(SENSOR_TEMP_INT)": {
                "valor": ("TOKEN_TEMPERATURA",),
            },

            "TOKEN_SENSOR_NUM(SENSOR_HUMEDAD)": {
                "valor": ("TOKEN_PORCENTAJE",),
            },

            "TOKEN_SENSOR_NUM(SENSOR_LUZ)": {
                "valor": ("TOKEN_LUZ",),
            },

        }

        return sensores.get(sensor)
    
    def booleano(self):

        token = self.token_actual()

        if token in (
            "TOKEN_TRUE",
            "TOKEN_FALSE",
            "TOKEN_ON",
            "TOKEN_OFF",
        ):

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un valor booleano y se encontró {token}."
        )

        self.recuperar()

        return None


    def operador_comp(self):

        token = self.token_actual()

        if token in (
            "TOKEN_IGUALDAD",
            "TOKEN_DISTINTO",
            "TOKEN_MAYOR",
            "TOKEN_MENOR",
            "TOKEN_MAYOR_IGUAL",
            "TOKEN_MENOR_IGUAL",
        ):

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un operador de comparación y se encontró {token}."
        )

        self.recuperar()

        return None


    def operador_bool(self):

        token = self.token_actual()

        if token in (
            "TOKEN_IGUALDAD",
            "TOKEN_DISTINTO",
        ):

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un operador booleano y se encontró {token}."
        )

        self.recuperar()

        return None


    def sensor_num(self):

        token = self.token_actual()

        if token is not None and token.startswith("TOKEN_SENSOR_NUM"):

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un sensor numérico y se encontró {token}."
        )

        self.recuperar()

        return None

    def sensor_bool(self):

        token = self.token_actual()

        if token is not None and token.startswith("TOKEN_SENSOR_BOOL"):

            self.avanzar()

            return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un sensor booleano y se encontró {token}."
        )

        self.recuperar()

        return None

    # Verifica que el valor asignado a un atributo respete su rango específico
    def validar_rango_atributo(self, atributo, valor_token, linea):
        rango = RANGOS_ATRIBUTO.get(atributo)
        if rango is None or valor_token is None:
            return
        if not (valor_token.startswith("TOKEN_TEMPERATURA(") and valor_token.endswith(")")):
            return 
        minimo, maximo = rango 
        valor_str = valor_token[len("TOKEN_TEMPERATURA("):-1]
        numero_str = valor_str.replace("°C", "")
        try:
            numero = int(numero_str)
        except ValueError:
            return
        if numero < minimo or numero > maximo: 
            self.error(
                f"Línea {linea}: el valor {valor_str} está fuera del rango permitido "
                f"para {atributo} ({minimo}°C a {maximo}°C)."
            )

    def esperar_valor(self, permitidos):

        token = self.token_actual()

        if token is None:

            self.error(
                f"Línea {self.linea_actual()}: Se esperaba un valor."
            )

            self.recuperar()

            return None

        for permitido in permitidos:

            if (
                token == permitido
                or token.startswith(permitido + "(")
            ):

                self.avanzar()

                return token

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba uno de {permitidos} y se encontró {token}."
        )

        self.recuperar()

        return None

    def tiempo(self):

        token = self.token_actual()
        if token == "TOKEN_TIEMPO" or (token is not None and token.startswith("TOKEN_TIEMPO")):
            self.avanzar()

            return

        self.error(
            f"Línea {self.linea_actual()}: "
            f"Se esperaba un tiempo y se encontró {self.token_actual()}."
        )

        self.recuperar()


    def expresion_num(self):

        sensor = self.sensor_num()

        if sensor is None:
            return

        if self.operador_comp() is None:
            return

        info = self.informacion_sensor(sensor)

        if info is None:

            self.error(
                f"Línea {self.linea_actual()}: "
                f"Sensor desconocido: {sensor}."
            )

            self.recuperar()

            return

        self.esperar_valor(info["valor"])


    def expresion_bool(self):

        if self.sensor_bool() is None:
            return

        if self.operador_bool() is None:
            return

        self.booleano()


    def expresion(self):
        token = self.token_actual()
        if token is None:
            self.error(f"Línea {self.linea_actual()}: Se esperaba una expresión.")
            self.recuperar()
            return

        # Si es un sensor, guardamos su estado de comparación
        if token.startswith("TOKEN_SENSOR_NUM") or token.startswith("TOKEN_SENSOR_BOOL"):
            sensor_nombre = token.replace("TOKEN_SENSOR_NUM(", "").replace("TOKEN_SENSOR_BOOL(", "").replace(")", "").lower()
            
            # Avanzamos temporalmente para mirar el operador y el valor
            self.avanzar() # consume el sensor
            operador_tok = self.token_actual()
            self.avanzar() # consume el operador
            valor_tok = self.token_actual()
            
            # Retrocedemos la posición para no romper la ejecución normal del parser
            self.posicion -= 2
            
            # Formateamos el operador y valor limpio
            op_limpio = "=="
            if operador_tok == "TOKEN_MAYOR": op_limpio = ">"
            elif operador_tok == "TOKEN_MENOR": op_limpio = "<"
            elif operador_tok == "TOKEN_MAYOR_IGUAL": op_limpio = ">="
            elif operador_tok == "TOKEN_MENOR_IGUAL": op_limpio = "<="
            elif operador_tok == "TOKEN_DISTINTO": op_limpio = "!="
            
            if valor_tok and "(" in valor_tok and valor_tok.endswith(")"):
                val_limpio = valor_tok[valor_tok.index("(") + 1 : -1]
            else:
                val_limpio = valor_tok.replace("TOKEN_", "") if valor_tok else ""
            texto_condicion = f"{op_limpio} {val_limpio}"
            
            if sensor_nombre not in self.datos_sensores:
                self.datos_sensores[sensor_nombre] = []
            if texto_condicion not in self.datos_sensores[sensor_nombre]:
                self.datos_sensores[sensor_nombre].append(texto_condicion)

        # Dejamos que el parser siga con su ejecución normal
        if token.startswith("TOKEN_SENSOR_NUM"):
            self.expresion_num()
            return
        elif token.startswith("TOKEN_SENSOR_BOOL"):
            self.expresion_bool()
            return
        elif self.es_actuador():
            atributo = self.actuador()
            if atributo is None: return
            info = self.informacion_atributo(atributo)
            if info is None: return
            if info["operador"] == "bool":
                self.operador_bool()
            else:
                self.operador_comp()
            self.esperar_valor(info["valor"])
            return

        self.error(f"Línea {self.linea_actual()}: Se esperaba una expresión y se encontró {token}.")
        self.recuperar()