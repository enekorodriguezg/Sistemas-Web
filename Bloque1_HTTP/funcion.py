#-*- coding: UTF-8 -*-

import requests


def descargar_imagen(pUri,pArchivo):
    metodo = "GET"
    uri = pUri
    cabecera = {'Host': "upload.wikimedia.org",
                'User-Agent': 'Mozilla/5.0 (compatible; Python requests)'}
    cuerpo = ''

    respuesta = requests.request(metodo, uri, headers=cabecera, data=cuerpo)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)

    for r_cabecera in respuesta.headers:
        print(r_cabecera + ": " + respuesta.headers[r_cabecera])

    if codigo == 200:
        fichero = open(f"{pArchivo}.jpg", "wb")
        fichero.write(respuesta.content)
        fichero.close()
    else:
        print("Error al descargar la imagen")

if __name__=='__main__':
    uri=input("Introduce la ruta de la imagen a descargar: \n")
    archivo = input("Introduce el nombre del archivo que quieres crear: \n")
    descargar_imagen(uri,archivo)

