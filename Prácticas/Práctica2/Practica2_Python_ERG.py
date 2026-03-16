#ENEKO RODRÍGUEZ GARCIA#
#SISTEMAS WEB - GO2#
#FECHA ENTREGA# --- TO DO
#PRÁCTICA 2#
#DESCRIPCIÓN# -- TO DO


import requests, getpass, sys
from bs4 import BeautifulSoup

def main():
    username=sys.argv[1]
    full_name=sys.argv[2]
    password=getpass.getpass(f'Introduce la contraseña para el usuario {username}: ')

    # SOLICITUD 1 - GET
    uri='https://egela.ehu.eus/login/index.php'
    headers={'Host': 'egela.ehu.eus'}
    print(f'SOLICITUD 1: {uri}')
    try:
        response=requests.get(uri,headers=headers)
        code=response.status_code
        if code != 200:
            print(code + response.reason)
    except Exception as e:
        print(f'Excepción: {e}')
        sys.exit(1)

    cookie = response.headers.get('Set-Cookie',[]).split(';')[0]
    if not cookie:
        print("Error al capturar la cookie")
        sys.exit(1)

    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    token_input=soup.find('input',{'name':'logintoken'})
    if not token_input:
        print('[!] Error al extraer el logintoken.')
        sys.exit(1)
    else:
        logintoken=token_input('value')

    print(f'RESPUESTA 1:\n{code} {response.reason}')
    print(f'Location:{response.headers.get("Location",[])}\nSet-Cookie: {cookie}')

    # SOLICITUD 2 - POST
    headers={'Host': 'egela.ehu.eus',
             'Cookie': cookie,
             'Content-Type': 'application/x-www-form-urlencoded'}
    response=requests.post(uri, headers=headers, data={'logintoken': logintoken, 'username': username, 'password': password})
    code=response.status_code
    description=response.reason


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("[!] USO: python3 Practica2_Python_ERG.py [nombre de usuario] ['NOMBRE COMPLETO']")
        sys.exit(1)
    main()


