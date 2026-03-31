import protocolo as p
import socket
import time

HOST = "127.0.0.1" 
PORT = 65432 # porta doservidor que vai conectar


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        mensagem = "2+3"
        p.enviar_mensagem(s, mensagem)
        print(f"Enviado {mensagem}")
        resposta = p.receber_mensagem(s)
        print(f"Recebido {resposta}")
        time.sleep(0.5)