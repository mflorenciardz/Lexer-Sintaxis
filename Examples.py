import re
TIPOS = {
    "PALABRA RESERVADA": ["WHEN", "IF", "EVERY", "DO", "END", "ELSE", "THEN"],
    "OPERADOR": ["==", "!=", ">", "<", ">=", "<="],
    "LÓGICO": ["OR", "AND", "NOT"],
    "ASIGNACIÓN": ["="],
    "DELIMITADOR": ["."],
    "BOOLEANOS": ["ON", "OFF", "TRUE", "FALSE"],
}
PATRON = {
    "TEMP": re.compile(r"\d+°C"),
    "PERCENT": re.compile(r"\d+%"),
    "ID": re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*"), #atributos, actuadores y sensores
}
