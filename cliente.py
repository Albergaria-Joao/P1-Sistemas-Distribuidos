import protocolo as p
import socket
import time
import threading
import random

HOST = "127.0.0.1"
PORT = 65432 # Porta do servidor coordenador em que vai conectar

def thread_respostas(sock): # Função da thread para receber as respostas dos workers via coordenador
    i = 0
    while True:
        res = p.receber_mensagem(sock)
        if res is None or res == p.SENTINELA:
            print("[THREAD] Conexão encerrada.")
            break
        print(f"RES({i}): {res}")
        i += 1
        

operacoes = ["+", "-", "*", "/"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:CLIENTE") # Envia a mensagem de handshake indicando que é cliente

    thread = threading.Thread(target=thread_respostas, args=(s,))
    thread.start() # Inicia a thread para receber as respostas dos workers via coordenador

    i = 0
    while i < 300:
        operacao = random.randint(0, 3)
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        mensagem = f"{num1}{operacoes[operacao]}{num2}" # Manda uma operação aleatória para o coordenador, que vai encaminhar para um worker
        p.enviar_mensagem(s, mensagem)
        print(f"Enviado({i}): {mensagem}")
        time.sleep(0.1) # delay de 0.1 segundos para ajudar na visualização dos prints, pode ser removido para enviar mais rápido
        i += 1

    p.enviar_mensagem(s, p.SENTINELA)  # avisa o coordenador que terminou
    print("[CLIENTE] Todas as operações enviadas, aguardando respostas...")
    thread.join()