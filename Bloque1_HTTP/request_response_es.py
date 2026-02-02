#-*- coding: UTF-8 -*-

import requests


metodo="GET"
uri="https://upload.wikimedia.org/wikipedia/commons/7/75/Internet1.jpg"
cabecera={'Host':"upload.wikimedia.org",
          'User-Agent':'Mozilla/5.0 (compatible; Python requests)'}
cuerpo=''

respuesta=requests.request(metodo,uri,headers=cabecera,data=cuerpo)

codigo=respuesta.status_code
descripcion=respuesta.reason
print(str(codigo)+ " "+descripcion)

for r_cabecera in respuesta.headers:
    print(r_cabecera + ": "+respuesta.headers[r_cabecera])

if codigo==200:
    fichero=open("imagen2.jpg", "wb")
    fichero.write(respuesta.content)
    fichero.close()
else:
    print("Error al descargar la imagen")


