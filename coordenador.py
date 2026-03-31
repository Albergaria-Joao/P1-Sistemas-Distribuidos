import socket
import protocolo as p
import threading
import queue
import time

HOST = "127.0.0.1"  
PORT = 65432        # porta que o servidor vai ouvir

fila_inputs = queue.Queue()
fila_outputs = queue.Queue()

def lidar_conexao(conn, addr, f_in, f_out):
    with conn:
        print(f"Connected by {addr}")
        tipo = p.receber_mensagem(conn).decode()
        print(tipo)
            
        while True:
            print("RODANDO WHILE")

            if tipo == "TIPO:WORKER":
                try:
                    task = f_in.get(timeout=1) # Pega da fila de inputs
                    p.enviar_mensagem(conn, task) # Envia para o worker
                    time.sleep(0.5)
                    result = p.receber_mensagem(conn).decode() # Recebe result
                    if not result:
                        print(f"[DESCONEXÃO] {addr} saiu.")
                        break

                    print(f"[RESPOSTA] {result}")
                    f_out.put(result) # Coloca na fila de output
                except queue.Empty:
                    break
                    
            else: 
                try:
                    data = p.receber_mensagem(conn).decode() # Pega input do cliente
                    print(f"[RECEBIDO] {data}")
                    if not data:
                        print(f"[DESCONEXÃO] {addr} saiu.")
                        break
                    f_in.put(data) # Coloca na fila de input
                    result = f_out.get(timeout=1) # Manda o primeiro resultado da fila para o cliente
                    p.enviar_mensagem(conn, result)

                except queue.Empty:
                    break
            
            
            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    print("ouvindo")
    s.bind((HOST, 65432))
    s.listen()
    while True:
        conn, addr = s.accept() # aceita a conexão na porta que está ouvindo. Addr é a porta do cliente (efêmera)
        thread = threading.Thread(target=lidar_conexao, args=(conn, addr, fila_inputs, fila_outputs)) # Cria uma thread para cuidar de cada conexão
        thread.start()
        print(f"[SISTEMA] Threads ativas: {threading.active_count() - 1}")