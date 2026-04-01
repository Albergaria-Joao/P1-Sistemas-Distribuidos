# NÃO FUNCIONA AINDA

import socket
import protocolo as p
import time
HOST = "127.0.0.1" 
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:WORKER")
    print("CONECTEI")
    while True:
        print("RECEBENDO")
        data = p.receber_mensagem(s)
        print(data)
        if not data:
            s.close()
            break
        # fazer alguma validação das operações, ex. mandou letra, mais de um operador, etc
        if ("+" in data):
            nums = data.split("+")
            result = float(nums[0]) + float(nums[1])
        elif ("-" in data):
            nums = data.split("-")
            result = float(nums[0]) - float(nums[1])
        elif ("*" in data):
            nums = data.split("*")
            result = float(nums[0]) * float(nums[1])
        elif ("/" in data):
            nums = data.split("/")
            result = float(nums[0]) / float(nums[1])
        else:
            p.enviar_mensagem(s, "ERRO")


        print(str(result))
        resposta = f"{data} = {str(result)}"
        p.enviar_mensagem(s, resposta)
        time.sleep(0.5)


