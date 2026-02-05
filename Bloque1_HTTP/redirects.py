#-*- coding: UTF-8 -*-

import requests


metodo='GET'
uri= 'https://ehu.eus'
cabeceras= {'Host': 'www.ehu.eus'}
cuerpo=''

respuesta=requests.request(metodo,uri,headers=cabeceras,data=cuerpo,allow_redirects=False)

codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo)+ ' '+descripcion)

cuerpo_respuesta=respuesta.content

uri=respuesta.headers['Location']
cabeceras={'Host': uri.split('/')[2]}
cuerpo=''

respuesta=requests.request(metodo,uri,headers=cabeceras,data=cuerpo,allow_redirects=False)
codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo)+ ' '+descripcion)

uri=respuesta.headers['Location']
cabeceras={'Host': uri.split('/')[2]}
cuerpo=''

respuesta=requests.request(metodo,uri,headers=cabeceras,data=cuerpo,allow_redirects=False)
codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo)+ ' '+descripcion)

if codigo==200:
    fichero=open('pagina.html', 'wb')
    fichero.write(respuesta.content)
    fichero.close()