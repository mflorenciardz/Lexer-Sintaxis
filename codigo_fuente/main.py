# Archivo principal del programa.

#Es el encargado de iniciar la ejecución del lexer. 
#Lee el texto ingresado por el usuario o el archivo de prueba y muestra los tokens reconocidos 
# o los errores encontrados.

from lexer import reservada
from errores import error_token

linea = input("Ingrese bla bla bla:")

palabras = linea.split()

for palabra in palabras:
    token = reservada(palabra)

    if token: 
        print(token)
    else:
        error_token(palabra)