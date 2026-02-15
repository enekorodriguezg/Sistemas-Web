#-*- coding: UTF-8 -*-
import requests, psutil, time, signal, sys, urllib, csv


API_KEY = 'U2LDYJQ1ATAV89X7'
CHANNEL_NAME = 'ergCanal'
channel_id = None
write_key = None

def handler(sig_num, frame):
    print("\n\n[!] Ctrl+C detectado. Iniciando guardado de datos...")
    if channel_id and write_key:
        data=get_last_100_json()
        create_csv(data)

    print("[!] Saliendo del programa...")
    sys.exit(0)

def cpu_ram():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    print("CPU: " + str(cpu) + "%\tRAM: " + str(ram) + "%")
    return cpu, ram

def check_channel():
    method = 'GET'
    uri = 'https://api.thingspeak.com/channels.json'
    headers = {'Host': 'api.thingspeak.com',
               'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': API_KEY}

    try:
        response = requests.request(method, uri, headers=headers, data=cuerpo)
        if response.status_code == 200:
            canales = response.json()
            for canal in canales:
                if canal.get('name') == CHANNEL_NAME:
                    cid = canal.get('id')
                    wk = next((k['api_key'] for k in canal.get('api_keys', []) if k.get('write_flag')), None)
                    return cid, wk
    except:
        pass
    return None, None

def create_channel():
    global channel_id
    global write_key

    existing_channel_id, existing_write_key = check_channel()

    if existing_channel_id is not None:
        print(f'[!] El canal {CHANNEL_NAME} ya existe. Se utilizará el ya existente')
        channel_id = existing_channel_id
        write_key = existing_write_key

        file = open("id_and_key.txt", "w")
        file.write("ID: " + str(channel_id))
        file.write("\nWrite key: " + write_key)
        file.close()
        return

    print("[*] El canal no existe. Creando uno nuevo...\n")
    method = 'POST'
    uri = 'https://api.thingspeak.com/channels.json'
    headers = {'Host': 'api.thingspeak.com',
               'Content-Type': 'application/x-www-form-urlencoded'}

    cuerpo = {'api_key': API_KEY,
              'name': CHANNEL_NAME,
              'description': 'RAM and CPU channel',
              'field1': '%CPU',
              'field2': '%RAM',
              'public_flag': 'true'}

    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    headers['Content-Length'] = str(len(cuerpo_encoded))

    try:
        response = requests.request(method, uri, headers=headers, data=cuerpo_encoded)
        codigo = response.status_code
    except:
        sys.exit(1)

    if codigo == 200:
        print('[+] Canal creado correctamente. Compruébalo en ThingSpeak')
        data = response.json()
        channel_id = data.get('id')
        write_key = next((k['api_key'] for k in data.get('api_keys', []) if k.get('write_flag')), None)

        if channel_id and write_key:
            file = open("id_and_key.txt", "w")
            file.write("ID: " + str(channel_id))
            file.write("\nWrite key: " + write_key)
            file.close()
            print("[+] ID del canal y API de escritura copiadas al archivo 'id_and_key.txt' correctamente")

    elif codigo == 402:
        print("[-] Has llegado al límite de canales creados. Por favor, elimina alguno y vuelve a intentarlo")
        input("[!] Pulsa 'ENTER' cuando lo hayas hecho... \n")
        create_channel()
        return
    else:
        print(f"[-] Error al crear canal. Código de estado {codigo}")
        sys.exit(1)

def post_data():
    while True:
        print('[*] Subiendo %CPU y %RAM al canal creado... \n')
        cpu_act, ram_act = cpu_ram()

        method = 'POST'
        uri = 'https://api.thingspeak.com/update.json'
        headers = {'Host': 'api.thingspeak.com',
                   'X-THINGSPEAKAPIKEY': write_key}
        cuerpo = {'field1': cpu_act,
                  'field2': ram_act}

        try:
            response = requests.request(method, uri, headers=headers, data=cuerpo)
            if response.status_code == 200:
                print('\n[+] Valores añadidos correctamente al canal. En 15 segundos se subirán nuevos valores')
            else:
                print('[-] Ha habido un error al subir los valores. Inténtalo de nuevo\n')
        except:
            pass

        time.sleep(15)

def get_last_100_json():
    method = 'GET'
    uri=f'https://api.thingspeak.com/channels/{channel_id}/feeds.json'
    headers = {'Host': 'api.thingspeak.com'}
    cuerpo={'api_key': API_KEY,
            'results': 100}
    try:
        response=requests.request(method, uri, headers=headers, params=cuerpo)
        codigo=response.status_code
        if codigo == 200:
            data=response.json()
            return data
        else:
            print(f"[-] Ha habido algún error al descargar los datos {codigo}")
    except Exception as e:
        print(f"[-] Excepción {e}")
    return None

def create_csv(data):
    if not data:
        return

    items=data.get('feeds',[])
    if not items:
        print("[-] El JSON está vacío o no tiene feeds")
        return

    file=open("last_100.csv","w")
    keys=list(items[0].keys())
    header_line=",".join(keys)

    for item in items:
        values=[]
        for key in keys:
            val=str(item.get(key,''))
            values.append(val)
        row_line=",".join(values)
        file.write(row_line + "\n")

    file.close()
    print("[+] CSV creado correctamente")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    print('\n[*] Iniciando programa...\n')
    create_channel()
    if channel_id and write_key:
        post_data()
    data=get_last_100_json()
    create_csv(data)