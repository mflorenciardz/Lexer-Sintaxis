from tokens import PREFIJO_ACTUADORES

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens      # lista de tokens que produjo el lexer
        self.posicion = 0         # empezamos leyendo el primer token

    def token_actual(self):
        if self.posicion > len(self.tokens): #Para evitar errores de posiciones fuera de listado
            return self.tokens[self.posicion]
        return None

    def avanzar(self):
        self.posicion += 1

    #ve si el token actual es el esperado
    def coincidir(self, esperado):
        if self.token_actual == esperado:
            self.avanzar()
        else:
            raise SyntaxError(f"Se esperaba {esperado} y se encontró {self.token_actual()}")
    #Raise es detener el programa por un error

    def programa(self):
        self.bloque() #pinkxel → bloque 

        if self.token_actual is not None:
            raise SyntaxError(f"Hay más tokens fuera del bloque.")
    
    def comienza_instruccion(self):

        token = self.token_actual()

        if token == "TOKEN_WHEN":
            return True

        if token == "TOKEN_IF":
            return True

        if token == "TOKEN_EVERY":
            return True

        if (
            token.startswith("TOKEN_FOCO_")
            or token.startswith("TOKEN_AIRE_")
            or token.startswith("TOKEN_PERSIANA_")
            or token.startswith("TOKEN_CERRADURA_")
            or token.startswith("TOKEN_RELOJ_")
            or token.startswith("TOKEN_ALTAVOZ_")
            or token.startswith("TOKEN_ALARMA_")
        ):
            return True

        return False

    def bloque(self):
        self.instruccion() #bloque → instruccion 

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

        elif self.es_actuador():
            self.asignacion()

        else:
            raise SyntaxError(f"No se puede comenzar una instrucción con {self.token_actual()}")

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

        self.bloque()

        self.coincidir("TOKEN_END")

    def every(self):

        self.coincidir("TOKEN_EVERY")

        self.tiempo()

        self.coincidir("TOKEN_DO")

        self.bloque()

        self.coincidir("TOKEN_END")

    def condicion(self):

        ...

    def expresion(self):

        ...

    def expresion_num(self):

        ...

    def expresion_bool(self):

        ...

    def sensor_num(self):

        ...

    def sensor_bool(self):

        ...

    def valor(self):

        ...

    def asignacion(self):

        ...