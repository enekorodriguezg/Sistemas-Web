#-*- coding: UTF-8 -*-
import sys
import urllib
from pydoc import describe

import requests

method='POST'
uri='https://ws-sendata.appspot.com/dni/letra'
cabeceras={'Host': 'ws-sendata.appspot.com',
           'Content-Type': 'application/x-www-form-urlencoded'}
cuerpo={'dni':sys.argv[1]}

cuerpo_encoded=urllib.parse.urlencode(cuerpo)

cabeceras['Content-Lenght'] = str(len(cuerpo_encoded))

respuesta=requests.request(method,uri,data=cuerpo_encoded,headers=cabeceras,allow_redirects=False)

codigo=respuesta.status_code
descripcion=respuesta.reason

print(str(codigo)+' '+descripcion)

print('Tu DNI con letra es: '+sys.argv[1]+respuesta.content.decode('utf-8'))
