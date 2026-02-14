#-*- coding: UTF-8 -*-
from asyncio.windows_events import NULL

import requests,psutil,time,signal,sys,urllib


# --- ENEKO RODRÍGUEZ G02 --- #

# --- TO DO --> requisito B que si existe el canal, se trabaje con el ya existente. si se supera el limite de canales pare el programa pidiendo al usuario que borre alguno y despues escriba "listo" p.e.  ---
API_KEY='U2LDYJQ1ATAV89X7'
CHANNEL_NAME='ergCanal'
channel_id= None
write_key= None


def handler(sig_num,frame):
    print('\n[!] Saliendo...\n')
    sys.exit(1)

def cpu_ram():
    signal.signal(signal.SIGINT, handler)
    cpu= psutil.cpu_count()
    ram= psutil.virtual_memory().percent
    print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
    return cpu, ram

def check_channel():
    method= 'GET'
    uri= 'https://api.thingspeak.com/channels.json'
    headers= {'Host': 'api.thingspeak.com',
              'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo={'api_key': API_KEY}

    response = requests.request(method, uri, headers=headers, data=cuerpo)
    canales=response.json()
    for canal in canales:
        print(canal)


    for canal in canales:
        if canal.get('name') == CHANNEL_NAME:
            return True
    return False

def create_channel():
    id=check_channel()
    if id!=NULL:
        print(f'[!] El canal {CHANNEL_NAME} ya existe. Se utilizará el ya existente')

    global channel_id
    global write_key

    method= 'POST'

    uri= 'https://api.thingspeak.com/channels.json'

    headers= {'Host': 'api.thingspeak.com',
              'Content-Type': 'application/x-www-form-urlencoded'}

    cuerpo= {'api_key': API_KEY,
              'name': CHANNEL_NAME,
              'description': 'RAM and CPU channel',
              'field1': '%CPU',
              'field2': '%RAM',
              'public_flag': 'true'}
    params=''
    cuerpo_encoded= urllib.parse.urlencode(cuerpo)
    headers['Content-Length'] = str(len(cuerpo_encoded))
    response = requests.request(method, uri, headers=headers, data=cuerpo_encoded)
    codigo= response.status_code
    description=response.reason
    if codigo==200:
        print('[+] Canal creado correctamente. Compruébalo en ThingSpeak')
    elif codigo==402:
        print("[-] Has llegado al límite de canales creados. Por favor, elimina alguno y vuelve a intentarlo")
        listo=input("[!] Escribe 'Listo' cuando lo hayas hecho...\n")

    else:
        print(f"[-] Error al crear canal. Código de estado {codigo} {description}")
        sys.exit(1)

    data=response.json()
    channel_id=data.get('id')
    write_key=next((k['api_key'] for k in data.get('api_keys', []) if k.get('write_flag')), None)


    if channel_id!=None and write_key!=None:
        file=open("id_and_key.txt", "w")
        file.write("ID: " + str(channel_id))
        file.write("\nWrite key: " + write_key)
        file.close()
        print("[+] ID del canal y API de escritura copiadas al archivo 'id_and_key.txt' correctamente")

def post_data():
    while True:
        print('[*] Subiendo %CPU y %RAM al canal creado... \n')
        cpu_act, ram_act = cpu_ram()
        method= 'POST'
        uri= 'https://api.thingspeak.com/update.json'
        headers= {'Host': 'api.thingspeak.com',
                  'X-THINGSPEAKAPIKEY': write_key}
        cuerpo= {'field1': cpu_act,
                 'field2': ram_act}
        response = requests.request(method, uri, headers=headers, data=cuerpo)
        codigo=response.status_code
        if codigo==200:
            print('\n[+] Valores añadidos correctamente al canal. En 15 segundos se subirán nuevos valores')
        else:
            print('[-] Ha habido un error al subir los valores. Inténtalo de nuevo\n')
            print('[!] Saliendo...\n')
        time.sleep(5)

def get_last_100():
    method='GET'
    uri= f'https://api.thingspeak.com/channels/{channel_id}/feeds.json'
    headers= {'Host': 'api.thingspeak.com',}
    cuerpo= {'api_key': API_KEY,
             'results': 100}
    response= requests.request(method, uri, headers=headers, data=cuerpo)
    codigo=response.status_code
    print(codigo)

if __name__=='__main__':
    signal.signal(signal.SIGINT, handler)
    print('\n[*] Creando canal...\n')
    create_channel()
    post_data()


