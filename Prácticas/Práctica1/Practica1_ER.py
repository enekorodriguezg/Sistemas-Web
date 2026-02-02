#-*- coding: UTF-8 -*-
from asyncio.windows_events import NULL

import requests,psutil,time,signal,sys,urllib

# --- ENEKO RODRÍGUEZ G02 --- #


API_KEY='U2LDYJQ1ATAV89X7'
channel_id= None
write_key= None

def handler(sig_num,frame):
    print('\n Saliendo...\n')
    sys.exit(0)


def cpu_ram():
    cpu= psutil.cpu_count()
    ram= psutil.virtual_memory().percent
    print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
    time.sleep(5)

def send_petition(method, uri, headers=None, cuerpo=None, params=None, allow_red=False):
    return requests.request(method, uri, headers=headers, data=cuerpo, params=params, allow_redirects=allow_red)

def check_channel():
    method= 'GET'
    uri= 'https://api.thingspeak.com/channels.json'
    headers= {'Host': 'api.thingspeak.com',
              'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo={'api_key': API_KEY,
            'tag': 'ergCanal'}


    response= send_petition(method, uri, cuerpo)
    print(response.content)

    if response.content:
        return True
    else:
        return False

def create_channel():

    if check_channel():
        print('[!] El canal ya existe por lo que no se creará\r\n[!] Saliendo...\n')
        sys.exit(0)

    global channel_id
    global write_key

    method= 'POST'

    uri= 'https://api.thingspeak.com/channels.json'

    headers= {'Host': 'api.thingspeak.com',
              'Content-Type': 'application/x-www-form-urlencoded'}

    cuerpo= {'api_key': API_KEY,
              'name': 'ergCanal',
              'description': 'RAM and CPU channel',
              'field1': '%CPU',
              'field2': '%RAM',
              'public_flag': 'true'}
    params=''
    cuerpo_encoded= urllib.parse.urlencode(cuerpo)
    #print(cuerpo_encoded)
    headers['Content-Length'] = str(len(cuerpo_encoded))
    response = send_petition(method, uri, headers=headers, cuerpo=cuerpo_encoded)
    codigo= response.status_code
    #print(codigo)
    if codigo==200:
        print('[+] Canal creado correctamente. Compruébalo en ThingSpeak')
    else:
        print(f"[-] Error al crear canal. Código de estado {codigo}")
        sys.exit(0)

    data=response.json()
    channel_id=data.get('id')
    write_key=next((k['api_key'] for k in data.get('api_keys', []) if k.get('write_flag')), None)


    if channel_id!=None and write_key!=None:
        file=open("id_and_key.txt", "w")
        file.write("ID: " + str(channel_id))
        file.write("\nWrite key: " + write_key)
        file.close()
        print("[+] ID del canal y API de escritura copiadas al archivo 'id_and_key.txt' correctamente")



if __name__=='__main__':
    signal.signal(signal.SIGINT, handler)
    print('\n[*] Creando canal...\n')
    create_channel()

