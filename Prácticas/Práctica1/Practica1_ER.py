#-*- coding: UTF-8 -*-
import urllib

# --- ENEKO RODRÍGUEZ G02 --- #

import requests,psutil,time,signal,sys


API_KEY='KC1DTLXZ8Q01Q34H'

def handler(sig_num,frame):
    print('\n Saliendo...\n')
    sys.exit(0)



def cpu_ram():
    cpu= psutil.cpu_count()
    ram= psutil.virtual_memory().percent
    print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
    time.sleep(5)

def send_petition(method, uri, headers, cuerpo,allow_red):
    return requests.request(method,uri,headers=headers,data=cuerpo, allow_redirects=allow_red)


def create_channel():
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

    cuerpo_encoded= urllib.parse.urlencode(cuerpo)
    #print(cuerpo_encoded)
    headers['Content-Lenght'] = str(len(cuerpo_encoded))
    response = send_petition(method, uri, headers, cuerpo_encoded, False)
    codigo= response.status_code
    #print(codigo)
    if codigo==200:
        print('[+] Canal creado correctamente. Compruébalo en ThingSpeak')
    else:
        print(f"[-] Error al crear canal. Código de estado {codigo}")
    '''
    description= response.reason
    print(description)
    '''
    response_cuerpo = response.content
    print('Cuerpo de la respuesta: ' + str(response_cuerpo))



if __name__=='__main__':
    signal.signal(signal.SIGINT, handler)
    print('\n[*] Creando canal...\n')
    create_channel()

