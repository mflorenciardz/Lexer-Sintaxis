#Definición de tokens.

#Contiene la lista de tokens que reconoce el lenguaje, como palabras reservadas, sensores, 
# actuadores, operadores, literales, etc.

#Permite mantener organizada la clasificación de todos los componentes léxicos.

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
SIMBOLOS ={
    "@",
    ":",
    "%",
    "!",
    "/",
    '"',
}

SENSORES = {
    "sensor_temp",
    "sensor_humo",
    "sensor_humedad",
    "sensor_luz",
    "sensor_movimiento",
}

BOOLEANOS = {
    "TRUE",
    "FALSE",
    "ON",
    "OFF",
}

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
    "EMAIL"
}