import datetime
import json
import pickle
import urllib
import requests
import csv
import re
import os
from bs4 import BeautifulSoup

j_link_enviado = {}

j_pag_ne = {}

mugre = ["xmlns=http://www.w3.org/1999/>", "<\n", "\n>", "<<p>", "<p>", "</p", "xmlns=http://www.w3.org/1999/>",
         "xmlns=http://www.w3.org/1999/>", "<br />", "CDATA", "</div>>", "<div>", "</div>", "%>", "<iframe>",
         "</iframe>", "100%", "<div", "http://w3.org/", "xmlms", "xhtml", ";>", "<", ">", "'", '"', "\/", "]", "["]
def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m, "")
    return texto
def link_enviado(l):
    l = limpiar(l, mugre)
    if not l in j_link_enviado.keys():
        print(" Enviando a telegram :", l)
        j_link_enviado[l] = 1
        return False
    else:
        print(" !!!!!!!!!!!!!!! ENCONTRO DUPLICADO !!!!!!!!!!!!!!!!!! ")
        return True
def log(texto):
    l = open("log.csv", "a")
    l.write(texto + "\n")
    l.close()
def save_persist(elem):
    try:
        vpath = "./persist/"

        varchivo = vpath + elem + ".bin"
        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:

        print("Except de save_persist", e)
def load_persist(elem):
    try:

        vpath = "./persist/"
        varchivo = vpath + elem + ".bin"

        with open(varchivo, "br") as archivo:
            # #print(pickle.load(archivo))
            return pickle.load(archivo)

    except Exception as e:

        print("269 - Except load_persit ", e)
def replaceBase(texto):
    texto = texto.replace("http:", " ").replace("//", " ").replace(".", " ").replace("www", " ").replace(
            "https:", " ").replace("/", " ").replace("\n", " ").replace("-", " ")
    return  texto
def replaceURL(texto):
    texto = texto.replace("http:", "").replace("//", "").replace(".", "").replace("www", "").replace(
            "https:", "").replace("/", "").replace("\n", "").replace("-", "")
    return  texto


class RSSParser(object):
    def parse(self,confiTagPage, urlytag, tema):
        ListaDeLinks = []
        items = []
        Noticia = []
        RedesSociales = ["facebook", "twitter", "whatsapp"]
        url = urlytag
        urlCortada = replaceURL(urlytag)
        TAGS = open("./TAGS/" + urlCortada + ".txt", "a", encoding='utf-8')
        LINKS = open("./LINKS/" + urlCortada + ".txt", "a", encoding='utf-8')
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            response = requests.get(url, headers=headers).text
        except Exception as e:
            print(" 58 - response ", e)
        try:
            for Noti in confiTagPage[0]["BuscarNoticia"]:

                try:
                    Noticias = eval(Noti)
                    if eval(Noti) != []:
                        Noticia.extend(Noticias)
                        TAGS.write(Noti + '\n')
                except Exception as e:
                    print(e)
        except Exception as e:
            print(" 58 - Obtener noticias ", e)
        TAGS.close()
        temp9 = ""
        try:
            for i in Noticia:
                texto = filtroReplace(i.get_text())
                if filtro_tema2(texto, tema):
                    ListaDeLinks = set(eval(confiTagPage[0]["path"]))
                    url2 = url
                    if len(ListaDeLinks) == 1:
                        temp9 = list(ListaDeLinks)
                        temp9 = str(temp9[0])
                        LINKS.write((temp9) + '\n')
                    else:
                        palabras = texto.split()
                        palabras.append(tema)
                        if ListaDeLinks != "":
                            try:
                                for l in ListaDeLinks:
                                    linkCortado = replaceBase(l).split()
                                    totalPalabras = len([palabra for palabra in palabras if palabra in linkCortado])
                                    if 2 <= totalPalabras <= 20:
                                        totalRedes = len([redSocial for redSocial in RedesSociales if redSocial in l.lower()])
                                        if not totalRedes >= 1:
                                            temp9 = l
                                            LINKS.write((temp9) + '\n')
                            except Exception as e:
                                print(" 58 - Obtener noticias ", e)
                                print(" ********* URL no parseada correctamente: \n", url, "\n")
                                print(i)
                                print("**********************************************************")

                                if not i.text in j_pag_ne.keys():
                                    j_pag_ne[i.text] = 1
                                    log("***** \n No scrapeó esta página: \n" + url + '\n' + str(i) + '\n ********')

                            """
                            print("- url: ", url)
                            print("- temp9:" , temp9)
                            print("--------------------------------")
        
                            """
                    if temp9[:1] == "/":
                        temp9 = temp9[1:]
                    if temp9[:8] == "noticias":
                        temp9 = temp9[8:]
                    if "http" in temp9:
                        url2 = temp9
                        temp9 = ""

                            # print(" url final:  ", url +  temp9 + temp10 + temp11, "\n temp9: ", temp9, "\n temp10: ",temp10, "\n temp11: ",temp11, "\n temp12: ",temp12)

                    j_i = {"link": url2 + temp9,
                           "desc": filtroReplace(i.get_text()),
                           "tmpItems": i}
                    if not filtro_repetida(j_i):
                        archivoCSV = []
                        link_noticia = j_i["link"]
                        link_web = url
                        FechaHoraScrapeo = str(datetime.datetime.now())
                        archivoCSV.append(link_noticia)
                        archivoCSV.append(link_web)
                        archivoCSV.append(FechaHoraScrapeo)
                        items.append(link_noticia)

                        with open("out.csv", "w") as f:
                            wr = csv.writer(f, delimiter="\n")
                            for ele in items:
                                wr.writerow([ele + ","])

            return items
        except Exception as e:
            print(" 100 - Obtener links ", e)



def filtroReplace(object):
    object.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]","").replace("<","").replace(">", "").replace("!", "").replace(",", "")
    return " ".join(object.split())
def filtro_repetida(j_i):
    dd = j_i['link'].replace("\n", "")[1:250]

    if "reconquista" in dd:
        print("parar")

    dd = limpiar(dd, mugre)
    # dd = dd.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<", "").replace(">", "").replace("!", "").replace("\n","")

    # print(dd)
    r = False
    if dd in db_noticias2.keys():
        if (db_noticias2[dd] == 1):
            r = True
        else:
            r = False
    if not r:
        db_noticias2[dd] = 1
        save_persist('db_noticias2')
    return r
def filtro_tema(j_i, tema):
    c1 = tema.upper() in j_i['desc'].upper()
    for j in tema.split(","):
        print((j, j_i['desc']))
        c2 = j.upper() in j_i['desc'].upper()
        c1 = c1 or c2
    if c1:
        r = True
    else:
        r = False
    return r
def filtro_tema2(texto, tema):
    c1 = tema.upper() in texto.upper()
    for j in tema.split(","):
        print((j, texto))
        c2 = j.upper() in texto.upper()
        c1 = c1 or c2
    if c1:
        r = True
    else:
        r = False
    return r
a_url_temas = []
def init():
    global vtelegram
    vtelegram = True

    def get_config(vkey):
        c = vkey in j_config.keys()
        if c:
            return j_config[vkey]
        else:
            return '-1'
def enviar_noticias(arr):
    if not vtelegram:
        pass
        # return

    try:
        url_api = token + "/sendMessage"

        # print( "- tema \n", Tema, " \n ",  NombreGrupo )
        men_t = "✔ Noticias referidas al tema %s, enviadas al grupo de télegram %s: " % (Tema, NombreGrupo) + "\n"
        ta = False
        # recorro el arreglo de links y lo imprimos
        men = []
        # print("arr \n",  arr)
        # print( "men_t \n", men_t )
        for a in arr:
            # print("3- ",a)
            # men += "- " + a + "\n\n"

            # armo la linea
            l = "- " + a + "\n\n"
            men.append(l)
            if a != "" and not (link_enviado(a)):
                ta = True
        if ta:
            # Si tiene información, mando el título.
            requests.post('https://api.telegram.org/' + url_api, data={'chat_id': idchat, 'text': men_t})
            for m in men:
                requests.post('https://api.telegram.org/' + url_api,
                              data={'chat_id': idchat, 'text': '\n [' + NombreGrupo + ']\n' + m})
                print(requests.status_codes)
    except Exception as e:
        print(" 279 - enviar ", e)
def configuracion():
    f = open("configParametrosGenerico.json", "r")

    global j_config
    j_config = {}
    j_config = json.loads(f.read())

    global vtelegram

    try:
        vtelegram = j_config["telegram"]
    except:
        vtelegram = True

    global token
    token = j_config["token"]
    global idchat
    idchat = j_config["id_chat"]
    global Tema
    Tema = j_config["Tema"]
    global NombreGrupo
    NombreGrupo = j_config["NombreGrupo"]
    global directorio
    directorio = j_config["directorio"]
    try:
        global db_noticias2

        db_noticias2 = {}

        if os.path.isfile(directorio + 'persist/db_noticias2.bin'):
            db_noticias2 = load_persist("db_noticias2")
        else:
            db_noticias2 = {}


    except:

        db_noticias2 = {}

if __name__ == "__main__":
    configuracion()
    j = open("configGenerico.json", "r")
    confiTagPage = {}
    confiTagPage = json.loads(j.read())["j"]
    while True:
        try:
            for url in confiTagPage[0]["link"]:
                if url != "":
                    print(" Procesando la url:  ", url)
                    r = RSSParser().parse(confiTagPage, url, Tema)
                    if r != []:
                        enviar_noticias(r)
        except Exception as e:
            print("207 - problema en el for general ", e)
    LINKS.close()
    fic.close()
