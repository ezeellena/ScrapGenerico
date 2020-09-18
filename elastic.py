import requests
#connect to our cluster
#from elasticsearch import Elasticsearch
import pprint



import json
import requests

vhost = "http://167.86.120.98:81/"
url = vhost


class els():


    def get(selft, vindex, vdoc, vparam, vcomando):


        intro = vindex + "/" + vdoc + "/" + vcomando

        # GET
        url = vhost + intro
        r = requests.get( url ).text
        return r

    def post(self, vindex, vdoc, vparam):

        try:
            vdata = json.dumps(vparam)

            vheaders = {'content-type': 'application/json'}

            intro = vindex + "/" + vdoc
            url = vhost + intro


            # lo uso para dar servicios
            self.permitir()

            r = requests.post( url, data = vdata, headers = vheaders )

            return r
        except Exception as e:
            print("elastic post exept ",e)


    def put(self, vindex, vdoc, vparam, vcomando):
        pass


    def permitir(self):
        vheaders = {'content-type': 'application/json'}
        dd1 = json.dumps( {"index.blocks.read_only_allow_delete": None} )
        url2 = vhost + "_all/_settings"
        r = requests.put( url2, data=dd1, headers=vheaders )


e = els()

"""
for i in range(100):
    j = {
        "id":i*10,
        "name":str(i)+'C'
    }

    r = e.post("i3","p2",j)
    print(i)
"""


# creo el obejto elastic
#e = els()

# hago un get
#r = e.get("test44","product","","_search")
#print(r)

"""
r = e.post("test444","product4",{"id":877,"name":"777777"},"")

r = e.get("test444","product4","","_search?pretty")

"""

#r = e.get("i2","p2","","_search?size=1000")
#pprint.pprint(r)
r = e.post("noticias","politica",{"location200":"-32.123, -60.3232"})
