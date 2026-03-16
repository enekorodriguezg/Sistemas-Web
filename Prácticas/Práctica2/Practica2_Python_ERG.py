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
    print(f'\nSOLICITUD 1: {uri}\n')
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
        logintoken=token_input.get('value')

    print(f'RESPUESTA 1:\n{code} {response.reason}')
    print(f'Location:{response.headers.get("Location",[])}\nSet-Cookie: {cookie}\n')

    # SOLICITUD 2 - POST
    headers={'Host': 'egela.ehu.eus',
             'Cookie': cookie,
             'Content-Type': 'application/x-www-form-urlencoded'}
    print(f'SOLICITUD 2: {uri}\nLoginToken: {logintoken}\nUsuario: {username}\nContraseña: {password}\n')
    response=requests.post(uri, headers=headers, data={'logintoken': logintoken, 'username': username, 'password': password})
    code=response.status_code
    if code != 200:
        print('[!] Error al realizar la solicitud')

    uri=response.headers.get("Location",[])

    print(f'RESPUESTA 2:\n{code} {response.reason}')
    print(f'Location:{response.headers.get("Location",[])}\nSet-Cookie: {cookie}')

    # SOLICITUD 3 - GET
    cookie=response.headers.get('Set-Cookie',[]).split(';')[0]
    headers={'Host': 'egela.ehu.eus',
             'Cookie': cookie}
    response=requests.get(uri, headers=headers)
    print(f'SOLICITUD 3: {uri}\nCookie: {cookie}\n')
    code=response.status_code
    if code != 200:
        print('[!] Error al realizar la solicitud')

    print(f'RESPUESTA 3:\n{code} {response.reason}\n')
    print(f'Location:{response.headers.get("Location",[])}\nSet-Cookie: {cookie}')

    #SOLICITUD 4 - GET


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("[!] USO: python3 Practica2_Python_ERG.py [nombre de usuario] ['NOMBRE COMPLETO']")
        sys.exit(1)
    main()


