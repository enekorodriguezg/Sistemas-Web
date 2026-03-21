# ENEKO RODRÍGUEZ GARCIA#
# SISTEMAS WEB - GO2#
# FECHA ENTREGA# --- 21/03/2026
# PRÁCTICA 2#
# DESCRIPCIÓN# -- Programa en python que inicia sesión en eGela, accede a la asignatura 'Sistemas Web', descarga todos los pdf y .py y genera un .csv con los entregables de la asignatura

import os, sys, getpass, re, csv, requests
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

    uri = 'https://egela.ehu.eus/login/index.php'
    headers = {'Host': 'egela.ehu.eus'}

    log_info(f'SOLICITUD 1: GET {uri}')
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

    logintoken = token_input.get('value')

    log_data(f'\nRESPUESTA 1:\n{code} {response.reason}')
    log_data(f'Location: {response.headers.get("Location", "")}\nSet-Cookie: {cookie}\n')

    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    log_info(f'SOLICITUD 2: POST {uri}\nLoginToken: {logintoken}\nUsuario: {username}\nContraseña: ***\n')

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

    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie
    }
    log_info(f'SOLICITUD 3: GET {uri_destino}\n')

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
    log_data(f'Location: {response.headers.get("Location", "")}\nSet-Cookie: {cookie}\n')

    uri_final = 'https://egela.ehu.eus/user/profile.php'
    headers = {
        'Host': 'egela.ehu.eus',
        'Cookie': cookie
    }
    log_info(f'SOLICITUD 4: GET {uri_final}')

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
    log_data(f'Location: {response.headers.get("Location", "")}\nSet-Cookie: {cookie}\n')

    html = response.text

    if full_name.lower() in html.lower():
        log_exito(f'Login correcto con el usuario {username}\n')
        os.system('pause')
    else:
        log_error(f'Login incorrecto con el usuario {username}')
        sys.exit(1)

    soup = BeautifulSoup(html, 'html.parser')
    enlace = soup.find('a', string=lambda texto: texto and 'sistemas web' in texto.lower())
    if enlace:
        uri_sw = enlace.get('href')
        log_exito(f'URI extraida correctamente: {uri_sw}\n')
    else:
        log_error(f'No se encontró el enlace de la asignatura')
        sys.exit(1)

    uri = uri_sw
    headers = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    try:
        response = requests.get(uri, headers=headers)
    except Exception as e:
        log_error(f'Excepcion: {e}')
        sys.exit(1)

    code = response.status_code
    if code != 200:
        log_error('Error al realizar la solicitud')
        sys.exit(1)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    apartados = soup.find('ul', class_='format_onetopic-tabs')
    if not apartados:
        log_error('Error al extraer los apartados')
        sys.exit(1)

    enlaces_apartados = apartados.find_all('a', class_='nav-link')
    uris_apartados = {}

    log_info('APARTADOS:')
    cont = 1
    for enlace in enlaces_apartados:
        nombre = enlace.get('title')
        uri_ap = enlace.get('href')

        if nombre and uri_ap:
            uris_apartados[nombre] = uri_ap
            print(f"{fg('green')}{cont}. {nombre}{attr('reset')}")
            cont += 1

    if not uris_apartados:
        log_error('Error al extraer los apartados')
        sys.exit(1)

    log_info("\nINICIANDO ESCANEO, DESCARGA Y RECOPILACIÓN DE TAREAS...")

    dir_base = "Descargas_Sistemas_Web"
    dir_python_global = os.path.join(dir_base, "Programas_Python")

    os.makedirs(dir_base, exist_ok=True)
    os.makedirs(dir_python_global, exist_ok=True)

    lista_tareas = []

    for nombre_apartado, uri_apartado in uris_apartados.items():
        log_info(f"Escaneando apartado: {nombre_apartado}")

        try:
            response_ap = requests.get(uri_apartado, headers=headers)
        except Exception as e:
            log_error(f"Error de red en apartado {nombre_apartado}: {e}")
            continue

        if response_ap.status_code != 200:
            continue

        soup_ap = BeautifulSoup(response_ap.text, 'html.parser')

        nombre_carpeta_tema = re.sub(r'[\\/*?:"<>|]', "", nombre_apartado).strip()
        ruta_carpeta_tema = os.path.join(dir_base, nombre_carpeta_tema)

        enlaces_recursos = soup_ap.find_all('a', href=lambda href: href and 'mod/resource/view.php' in href)

        for recurso in enlaces_recursos:
            # --- LA SOLUCIÓN AL "FITXATEGIA" ---
            # Buscamos y destruimos cualquier texto oculto de accesibilidad antes de leer
            for oculto in recurso.find_all('span', class_='accesshide'):
                oculto.decompose()
            # -----------------------------------

            nombre_arch = recurso.get_text(strip=True)
            uri_arch = recurso.get('href')
            nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", nombre_arch).strip()

            if ".py" in nombre_limpio.lower() or uri_arch.lower().endswith(".py"):
                ruta_destino = os.path.join(dir_python_global, nombre_limpio)
                if not ruta_destino.endswith(".py"):
                    ruta_destino += ".py"
            else:
                os.makedirs(ruta_carpeta_tema, exist_ok=True)
                ruta_destino = os.path.join(ruta_carpeta_tema, nombre_limpio)
                if not ruta_destino.endswith(".pdf"):
                    ruta_destino += ".pdf"

            try:
                res_archivo = requests.get(uri_arch, headers=headers, allow_redirects=True)
                if res_archivo.status_code == 200:
                    with open(ruta_destino, 'wb') as f:
                        f.write(res_archivo.content)
                    log_data(f"  -> Guardado: {ruta_destino}")
            except Exception as e:
                log_error(f"Error al descargar {nombre_limpio}: {e}")


        enlaces_tareas = soup_ap.find_all('a', href=lambda href: href and 'mod/assign/view.php' in href)

        for tarea in enlaces_tareas:

            for oculto in tarea.find_all('span', class_='accesshide'):
                oculto.decompose()

            titulo_tarea = tarea.get_text(strip=True)
            enlace_tarea = tarea.get('href')
            fecha_entrega = "No especificada"


            try:
                res_tarea = requests.get(enlace_tarea, headers=headers)
                if res_tarea.status_code == 200:
                    soup_tarea = BeautifulSoup(res_tarea.text, 'html.parser')

                    filas_tabla = soup_tarea.find_all('tr')
                    for fila in filas_tabla:
                        encabezado = fila.find('th')
                        if encabezado and ('entrega' in encabezado.text.lower() or 'epea' in encabezado.text.lower()):
                            celda_fecha = fila.find('td')
                            if celda_fecha:
                                fecha_entrega = celda_fecha.get_text(strip=True)
                                break
            except Exception as e:
                pass

            lista_tareas.append({
                'Tarea': titulo_tarea,
                'Fecha_Entrega': fecha_entrega,
                'Enlace': enlace_tarea
            })
            log_exito(f"  -> Tarea detectada: {titulo_tarea} (Fecha: {fecha_entrega})")

    ruta_csv = "tareas.csv"
    if lista_tareas:
        try:
            with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
                writer = csv.DictWriter(archivo_csv, fieldnames=['Tarea', 'Fecha_Entrega', 'Enlace'])
                writer.writeheader()
                writer.writerows(lista_tareas)
            log_info(f"Documento '{ruta_csv}' generado con éxito.")
        except Exception as e:
            log_error(f"No se pudo crear el archivo CSV: {e}")
    else:
        log_error("No se encontraron tareas para el CSV.")

    log_exito("EJECUCIÓN FINALIZADA. Entregables preparados.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("[!] USO: Practica2_Python_ERGpy [nombre de usuario] ['NOMBRE COMPLETO']")
        sys.exit(1)
    main()