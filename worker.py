# NÃO FUNCIONA AINDA

import socket
import protocolo as p
import time
HOST = "127.0.0.1" 
PORT = 65432

s = p.conectar_servidor(HOST, PORT)
while True:
    data = p.receber_mensagem(s).decode()
    if not data:
        s.close()
        break

    if ("+" in data):
        nums = data.split("+")
        result = sum(map(int, nums))
    elif ("-" in data):
        nums = data.split("-")
        result = sum(map(int, nums))
    elif ("*" in data):
        nums = data.split("*")
        result = sum(map(int, nums))
    elif ("/" in data):
        nums = data.split("/")
        result = sum(map(int, nums))
    else:
        p.enviar_mensagem(s, "ERRO")

    print(str(result))
    p.enviar_mensagem(s, str(result))
    time.sleep(0.5)


