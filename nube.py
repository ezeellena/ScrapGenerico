
### pasar datos para que eleastic puea armar nube de palabras.
from elastic import els
import json

global vels
vels = els()

f = open("configParametrosGenerico.json", "r")

j_config = json.loads(f.read())


def get_config(vkey):
    c = vkey in j_config.keys()
    if c:
        return j_config[vkey]
    else:
        return '-1'


nube_palabras = get_config("palabra_nube")


def texto2els(texto, fecha, medio):
    if nube_palabras == "-1" or nube_palabras == False:
        return

    # ponfo todo el texto
    j = {
        "palabra": texto,
        "fecha": fecha,
        "medio": medio
    }

    r = vels.post("noticias_nube", "palabras", j)

    # ahoro pongo las palabras

    for e in texto.split(" "):
        if len(e) > 4:

            try:
                j = {
                    "palabra": e,
                    "fecha": fecha,
                    "medio": medio
                }
                r = vels.post("noticias_nube", "palabras", j)
            except Exception as e:
                print("19 - ", e)

