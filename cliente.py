import protocolo as p
import socket
import time
import threading
import random
HOST = "127.0.0.1" 
PORT = 65432 # porta doservidor que vai conectar

def thread_respostas(sock):
    i = 0
    while True:
        i += 1
        res = p.receber_mensagem(s)
        print(f"RES({i}): {res}")


# time.sleep(0.5)
# thread = threading.Thread(target=thread_respostas, args=(s))
# thread.start()
operacoes = ["+", "-", "*", "/"]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:CLIENTE")
    thread = threading.Thread(target=thread_respostas, args=(s,)) # Cria uma thread para cuidar de cada conexão
    thread.start()
    
    i = 0
    while i < 100:
        operacao = random.randint(0, 3)
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        mensagem = f"{num1}{operacoes[operacao]}{num2}"
        p.enviar_mensagem(s, mensagem)
        print(f"Enviado({i}): {mensagem}")
        time.sleep(0.1)
        
        #resposta = p.receber_mensagem(s)
        #print(resposta)
        # print(f"Recebido {resposta}")
        
        i += 1
    thread.join()
    s.close()
