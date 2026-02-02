#-*- coding: UTF-8 -*-

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

def send_petition(method, uri, headers, cuerpo,allow_red):
    return requests.request(method,uri,headers=headers,data=cuerpo, allow_redirects=allow_red)

def create_channel():
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

    cuerpo_encoded= urllib.parse.urlencode(cuerpo)
    #print(cuerpo_encoded)
    headers['Content-Length'] = str(len(cuerpo_encoded))
    response = send_petition(method, uri, headers, cuerpo_encoded, False)
    codigo= response.status_code
    #print(codigo)
    if codigo==200:
        print('[+] Canal creado correctamente. Compruébalo en ThingSpeak')
    else:
        print(f"[-] Error al crear canal. Código de estado {codigo}")

    data=response.json()
    channel_id=data.get('id')
    write_key=next((k['api_key'] for k in data.get('api_keys', []) if k.get('write_flag')), None)


    if channel_id!=None and write_key!=None:
        file=open("channel_id_and_write_api_key.txt", "w")
        file.write(str(channel_id))
        file.write(write_key)
        file.close()



if __name__=='__main__':
    signal.signal(signal.SIGINT, handler)
    print('\n[*] Creando canal...\n')
    create_channel()

