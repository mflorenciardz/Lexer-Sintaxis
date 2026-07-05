# Definición de tokens.
# Contiene la lista de tokens que reconoce el lenguaje, como palabras reservadas, sensores, etc.
# Permite mantener organizada la clasificación de todos los componentes léxicos.

PALABRAS_RESERVADAS = {
    "WHEN",
    "IF",
    "ELSE",
    "THEN",
    "DO",
    "END",
    "EVERY",
    "AND",
    "OR",
    "NOT",
}

OPERADORES = {
    "==",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "=",
}

SIMBOLOS = {
    "@",
    ":",
    "%",
    "!",
    "/",
    '"',
    '.',
    '=',
    "-",
    "°",
    ">",
    "<",
}

# Sensores numéricos: admiten operadores de comparación (<, >, <=, >=, ==, !=)
# Se usan en expresion_num → sensor_num operador_comp valor
SENSORES_NUM = {
    "sensor_temp",
    "sensor_humedad",
    "sensor_luz",
    "sensor_temp_int",
}

# Sensores booleanos: solo admiten operadores de igualdad (==, !=)
# Se usan en expresion_bool → sensor_bool operador_bool bool
SENSORES_BOOL = {
    "sensor_humo",
    "sensor_movimiento",
}

BOOLEANOS = {
    "TRUE",
    "FALSE",
    "ON",
    "OFF",
}

# Prefijos válidos de actuadores.
# El lexer los usa para reconocer la parte fija del nombre (ej: "reloj_" en "reloj_cocina").
PREFIJO_ACTUADORES = {
    "foco_",
    "aire_",
    "persiana_",
    "cerradura_",
    "reloj_",
    "altavoz_",
    "alarma_",
}

ATRIBUTOS = {
    "ESTADO",
    "BRILLO",
    "COLOR",
    "MODO",
    "TEMP_OBJ",
    "TEMP_ACT",
    "POSICION",
    "ACTIVADA",
    "HORA",
    "FECHA",
    "VOLUMEN",
    "MUTE",
    "MENSAJE",
    "EMAIL",
    "EMAIL_NOTIF",
}

COLORES = {
    "rojo",
    "verde",
    "azul",
    "amarillo",
    "naranja",
    "violeta",
    "rosa",
    "celeste",
    "marron",
    "blanco",
}

MODOS = {
    "frio",
    "calor",
    "ventilador",
    "automatico",
    "seco",
}