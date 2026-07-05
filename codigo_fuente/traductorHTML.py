from pathlib import Path

# DATOS DEL GRUPO
PROFESOR = "Vigil, Rodrigo"

GRUPO = [
    "Aguirre, Agustina Belen - 30082",
    "Alberto, Angelina Lucia - 30088",
    "Leiva, Sofia Victoria - 30059",
    "Mujica, Ana Laura - 30071",
    "Rodríguez, María Florencia - 30642",
    "Verón, Milagros Luciana - 30782"
]

NOMBRE_GRUPO = "PINKXEL"

CATEDRA = "Sintaxis y Semántica de los Lenguajes"

ANNO = "2026"

# ESTILOS

ESTILO_SENSOR = """
border:1px solid green;
padding:20px;
margin:15px;
border-radius:8px;
background:#ecfff0;
"""

ESTILO_ACTUADOR = """
border:1px solid gray;
padding:20px;
margin:15px;
border-radius:8px;
background:#f8f8f8;
"""


# UTILIDADES


def limpiar(linea):

    return linea.strip()


def comentario(linea):

    return linea.startswith("//")


def es_when(linea):

    return linea.upper().startswith("WHEN")


def es_if(linea):

    return linea.upper().startswith("IF")


def es_every(linea):

    return linea.upper().startswith("EVERY")


def es_end(linea):

    return linea.upper() == "END"


def es_else(linea):

    return linea.upper() == "ELSE"


# SENSORES

def obtener_sensor(linea):

    partes = linea.split()

    if len(partes) < 4:

        return None

    nombre = partes[1]
    operador = partes[2]
    valor = partes[3]

    return {

        "nombre": nombre,
        "operador": operador,
        "valor": valor

    }

# ACTUADORES

def obtener_actuador(linea):

    if "=" not in linea:

        return None

    izquierda, derecha = linea.split("=", 1)

    izquierda = izquierda.strip()

    derecha = derecha.strip()

    if "." not in izquierda:

        return None

    actuador, atributo = izquierda.split(".", 1)

    return {

        "nombre": actuador.strip(),
        "atributo": atributo.strip(),
        "valor": derecha

    }

# EMAIL

def html_email(email):

    usuario = email.split("@")[0]

    return (
        f'<a href="mailto:{email}">'
        f'Contactar a {usuario}'
        f'</a>'
    )


# GENERACIÓN DE HTML

def agregar_encabezado(html, nombre_archivo):

    html.append("<!DOCTYPE html>")
    html.append("<html>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append(f"<title>{nombre_archivo}</title>")

    html.append("""

<style>

body{

    font-family:Arial,Helvetica,sans-serif;
    background:#fff3f8;
    margin:30px;

}

.header{

    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:40px;

}

.titulo{

    flex:1;
    text-align:center;

}

.titulo h1{

    color:#c2185b;
    font-size:60px;
    margin-bottom:5px;

}

.titulo h2{

    color:#c2185b;
    margin-top:0;

}

.logoPINXEL{

    width:150px;
    height:auto;

}

.info{
    width: 400px;
    
    background:white;

    padding:20px;

    border-radius:15px;

    box-shadow:0px 0px 10px rgba(0,0,0,0.08);

}

.info li{

    white-space:nowrap;

}                

.contenido{

    display:flex;
    gap:35px;
    align-items:flex-start;
    justify-content:space-between;

}


.info h2{

    color:#c2185b;

}
                
.actuadores{

    display:flex;
    flex-wrap:wrap;
    gap:20px;

    align-content:flex-start;

}

</style>

""")

    html.append("</head>")
    html.append("<body>")

    html.append('<div class="header">')

    html.append('<div class="titulo">')

    html.append("<h1>SMART HOME</h1>")
    html.append("<h2>Sintaxis y Semántica de los Lenguajes</h2>")

    html.append("</div>")


    html.append('<img class="logoPINXEL" src="../logoHTML/logoPINKXEL.png">')

    html.append("</div>")

    html.append('<div class="info">')

    html.append(f"<h2>{NOMBRE_GRUPO}</h2>")

    html.append("<h3>Integrantes</h3>")
    html.append("<ul>")

    for integrante in GRUPO:

        html.append(f"<li>{integrante}</li>")

    html.append("</ul>")

    html.append(f"<h3>Profesor asignado</h3>")
    html.append(f"<p>{PROFESOR}</p>")

    html.append(f"<h3>Año</h3>")
    html.append(f"<p>{ANNO}</p>")

    html.append("</div>")


def agregar_sensores(html, sensores):

    html.append(f'<div style="{ESTILO_SENSOR} min-width:480px; max-width:480px;">')

    html.append("<h1>Sensores</h1>")

    if len(sensores) == 0:

        html.append("<p>No se encontraron sensores.</p>")

    for sensor in sensores:

        nombre = sensor["nombre"].replace("_", " ").title()

        html.append(f"<h2>{nombre}</h2>")

        html.append(
            f"<p>{sensor['operador']} {sensor['valor']}</p>"
        )

    html.append("</div>")


def agregar_actuadores(html, actuadores):

    html.append('<div class="actuadores">')

    for nombre in actuadores:

        html.append(f'<div style="{ESTILO_ACTUADOR} width:300px;">')

        titulo = nombre.replace("_", " ").title()

        html.append(f"<h1>{titulo}</h1>")

        html.append("<ul>")

        for atributo, valor in actuadores[nombre].items():

            atributo = atributo.replace("_", " ").title()

            if atributo.lower() == "email notif":

                html.append(
                    f"<li>{html_email(valor)}</li>"
                )

            else:

                html.append(
                    f"<li><b>{atributo}:</b> {valor}</li>"
                )

        html.append("</ul>")

        html.append("</div>")

    html.append("</div>")


# TRADUCCIÓN PRINCIPAL
def traducir(lineas, nombre_archivo):

    sensores = []

    actuadores = {}

    for linea in lineas:

        linea = limpiar(linea)

        if linea == "":
            continue

        if comentario(linea):
            continue

        if (
            es_when(linea)
            or es_if(linea)
            or es_every(linea)
            or es_end(linea)
            or es_else(linea)
        ):

            if es_when(linea) or es_if(linea):

                sensor = obtener_sensor(linea)

                if sensor is not None:

                    sensores.append(sensor)

            continue


        actuador = obtener_actuador(linea)

        if actuador is None:

            continue

        nombre = actuador["nombre"]

        atributo = actuador["atributo"]

        valor = actuador["valor"]

        if nombre not in actuadores:

            actuadores[nombre] = {}

        actuadores[nombre][atributo] = valor


    html = []

    agregar_encabezado(html, nombre_archivo)

    html.append('<div class="contenido">')

    agregar_sensores(html, sensores)

    agregar_actuadores(html, actuadores)

    html.append("</div>")
    html.append("</body>")
    html.append("</html>")


    BASE = Path(__file__).parent.parent

    ruta = BASE / "pruebas" / Path(nombre_archivo).with_suffix(".html")

    with open(ruta, "w", encoding="utf-8") as archivo:

        archivo.write("\n".join(html))

    print(f"\nArchivo HTML generado: {ruta}")