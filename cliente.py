import protocolo as p
import socket
import time
import threading
import random

HOST = "127.0.0.1"
PORT = 65432

def thread_respostas(sock):
    i = 0
    while True:
        res = p.receber_mensagem(sock)
        if res is None or res == p.SENTINELA:
            print("[THREAD] Conexão encerrada.")
            break
        i += 1
        print(f"RES({i}): {res}")

operacoes = ["+", "-", "*", "/"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:CLIENTE")

    thread = threading.Thread(target=thread_respostas, args=(s,))
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
        i += 1

    p.enviar_mensagem(s, p.SENTINELA)  # avisa o coordenador que terminou
    print("[CLIENTE] Todas as operações enviadas, aguardando respostas...")
    thread.join()