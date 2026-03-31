import protocolo as p
import socket
import time
import threading

HOST = "127.0.0.1" 
PORT = 65432 # porta doservidor que vai conectar

def thread_respostas(sock):
    while True:
        res = p.receber_mensagem(s).decode()
        print("RESULT {res}")

s = p.conectar_servidor(HOST, PORT, "CLIENTE")
# time.sleep(0.5)
# thread = threading.Thread(target=thread_respostas, args=(s))
# thread.start()
i = 0
while i < 100:
    mensagem = "2+3"
    p.enviar_mensagem(s, mensagem)
    # print(f"Enviado {mensagem}")
    # resposta = p.receber_mensagem(s)
    # print(f"Recebido {resposta}")
    time.sleep(0.1)
    print("ENVIADO")
    i += 1
s.close()
