# NÃO FUNCIONA AINDA

import socket
import protocolo as p

HOST = "127.0.0.1" 
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        data = p.receber_mensagem(s)
        if not data:
            break
        conn.sendall(data)


# if ("+" in data):
#     nums = data.split("+")
# elif ("-" in data):
#     nums = data.split("-")
# elif ("*" in data):
#     nums = data.split("*")
# elif ("/" in data):
#     nums = data.split("/")
# else:
#     p.enviar_mensagem(conn, "ERRO")