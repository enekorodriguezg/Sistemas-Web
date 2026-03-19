# ENEKO RODRÍGUEZ GARCIA#
# SISTEMAS WEB - GO2#
# FECHA ENTREGA# --- TO DO
# PRÁCTICA 2#
# DESCRIPCIÓN# -- TO DO

import requests, getpass, sys
from bs4 import BeautifulSoup
from colored import fg, attr


def log_info(mensaje):
    print(f"{fg('cyan')}[INFO] {mensaje}{attr('reset')}")


def log_exito(mensaje):
    print(f"{fg('green')}[+] {mensaje}{attr('reset')}")


def log_error(mensaje):
    print(f"{fg('red')}[!] ERROR: {mensaje}{attr('reset')}")


def log_data(mensaje):
    print(f"{fg('yellow_1')}{mensaje}{attr('reset')}")


def extraer_cookie(headers):
    cookie_raw = headers.get('Set-Cookie')
    if cookie_raw:
        return cookie_raw.split(';')[0]
    return None


def main():
    username = sys.argv[1]
    full_name = sys.argv[2]
    password = getpass.getpass(f'Introduce la contraseña para el usuario {username}: ')

    # SOLICITUD 1 - GET
    uri = 'https://egela.ehu.eus/login/index.php'
    headers = {'Host': 'egela.ehu.eus'}
    log_info(f'\nSOLICITUD 1: {uri}')

    try:
        response = requests.get(uri, headers=headers)
    except Exception as e:
        log_error(f'Excepción: {e}')
        sys.exit(1)

    code = response.status_code
    if code != 200:
        log_error(f'{code} {response.reason}')
        sys.exit(1)

    cookie = extraer_cookie(response.headers)
    if not cookie:
        log_error("Error al capturar la cookie")
        sys.exit(1)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    token_input = soup.find('input', {'name': 'logintoken'})
    if not token_input:
        log_error('Error al extraer el logintoken.')
        sys.exit(1)
    else:
        logintoken = token_input.get('value')

    log_data(f'\nRESPUESTA 1:\n{code} {response.reason}')
    log_data(f'Location: {response.headers.get('Location', '')}\nSet-Cookie: {cookie}\n')

    # SOLICITUD 2 - POST
    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    log_info(f'SOLICITUD 2: {uri}\nLoginToken: {logintoken}\nUsuario: {username}\nContraseña: ***\n')

    try:
        response = requests.post(uri, headers=headers,
                                 data={'logintoken': logintoken, 'username': username, 'password': password},
                                 allow_redirects=False)
    except Exception as e:
        log_error(f'Excepción: {e}')
        sys.exit(1)

    code = response.status_code
    if code != 303:
        log_error('Error al realizar la solicitud')
        sys.exit(1)

    uri_destino = response.headers.get("Location")
    if not uri_destino or uri_destino == 'https://egela.ehu.eus/login/index.php':
        log_error('Login incorrecto')
        sys.exit(1)

    nueva_cookie = extraer_cookie(response.headers)
    if nueva_cookie:
        cookie = nueva_cookie

    log_data(f'RESPUESTA 2:\n{code} {response.reason}')
    log_data(f'Location: {uri_destino}\nSet-Cookie: {cookie}\n')

    # SOLICITUD 3 - GET
    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie
    }
    log_info(f'SOLICITUD 3: {uri_destino}\n')

    try:
        response = requests.get(uri_destino, headers=headers)
    except Exception as e:
        log_error(f'Excepción: {e}')
        sys.exit(1)

    code = response.status_code
    if code != 200:
        log_error('Error al realizar la solicitud')
        sys.exit(1)

    log_data(f'RESPUESTA 3:\n{code} {response.reason}')
    log_data(f'Location: {response.headers.get('Location', '')}\nSet-Cookie: {cookie}\n')

    # SOLICITUD 4 - GET
    uri_final = 'https://egela.ehu.eus/'
    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie
    }
    log_info(f'SOLICITUD 4: {uri_final}')

    try:
        response = requests.get(uri_final, headers=headers)
    except Exception as e:
        log_error(f'Excepción: {e}')
        sys.exit(1)

    code = response.status_code
    if code != 200:
        log_error('Error al realizar la solicitud')
        sys.exit(1)

    log_data(f'\nRESPUESTA 4:\n{code} {response.reason}')
    log_data(f'Location: {response.headers.get('Location', '')}\nSet-Cookie: {cookie}\n')

    html = response.text.lower()
    nombre_pila = full_name.split(' ')[0].lower()

    if nombre_pila in html and 'logout.php' in html:
        log_exito(f'Login correcto con el usuario {username}')
    else:
        log_error(f'Login incorrecto con el usuario {username}')
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("[!] USO: python3 Practica2_Python_ERG.py [nombre de usuario] ['NOMBRE COMPLETO']")
        sys.exit(1)
    main()