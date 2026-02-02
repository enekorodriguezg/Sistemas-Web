#-*- coding: UTF-8 -*-
import socket
import ssl

HOST = "upload.wikimedia.org"
PORT = 443

# socket.AF_INET --- IPv4.
# socket.SOCK_STREAM --- protocolo TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Envolver el socket con SSL (HTTPS)
contexto = ssl.create_default_context()
sock_ssl = contexto.wrap_socket(sock, server_hostname=HOST)

# Conectar al servidor
sock_ssl.connect((HOST, PORT))
print("Local socket:", sock_ssl.getsockname())


metodo = 'GET'
camino = "/wikipedia/commons/7/75/Internet1.jpg"

#------- CREACIÓN DE LA CADENA DE ALA PETICIÓN -------------------
primera_linea = metodo + " "+ camino + " " + "HTTP/1.1\n"
print(primera_linea)

cabeceras = {'Host': "upload.wikimedia.org",
             'User-Agent': 'Mozilla/5.0 (compatible; Python requests)',
             'Connection':' close',}

cadena_cabeceras = ''
for each in cabeceras:
    linea_cabecera= each + ":" + cabeceras[each] + "\n"
    cadena_cabeceras += linea_cabecera
print(cadena_cabeceras)
cadena_peticion_http =primera_linea + cadena_cabeceras + "\r\n"

#-------------------------------------
cadena_peticion_http_bytes = bytes(cadena_peticion_http, 'utf-8')
print('##### HTTP peticion #####')
print(cadena_peticion_http_bytes)

sock_ssl.sendall(cadena_peticion_http_bytes)

print("#####Procesando  la respuesta HTTP#####")

# Recibir la respuesta completa
respuesta = b""
while True:
    datos = sock_ssl.recv(4096)
    if not datos:
        break
    respuesta += datos
sock_ssl.close()

#  Separar cabeceras y cuerpo
cabeceras, cuerpo = respuesta.split(b"\r\n\r\n", 1)

# Procesar cabeceras
cabeceras_texto = cabeceras.decode("utf-8", errors="ignore")
print("===== CABECERAS HTTP =====")
print(cabeceras_texto)
# Guardar la imagen en un archivo

fichero = open("imagen.jpg", 'wb')
fichero.write(cuerpo)
fichero.close()

