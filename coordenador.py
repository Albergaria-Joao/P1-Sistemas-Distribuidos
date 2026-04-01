import socket
import protocolo as p
import threading
import queue
import time

HOST = "127.0.0.1"  
PORT = 65432        # porta que o servidor vai ouvir

fila_inputs = queue.Queue() # fila de tarefas
fila_outputs = queue.Queue() # fila de resultados

def lidar_conexao(conn, addr, f_in, f_out):
    with conn:
        mensagem_inicial = p.receber_mensagem(conn)
        if not mensagem_inicial:
            return
            
        tipo = mensagem_inicial.strip()
        print(f"[HANDSHAKE] {addr} {tipo}")
            
        while True:
            if tipo == "TIPO:WORKER":
                try:
                    task = f_in.get(timeout=1) # pega da fila de inputs
                    
                    p.enviar_mensagem(conn, task)
                    
                    result = p.receber_mensagem(conn) 
                    if not result:
                        print(f"DESCONEXÃO Worker {addr} caiu")
                        break
                        
                    print(f"WORKER {addr} Retornou: {result}")
                    f_out.put(result) # joga na fila de outputs
                    
                except queue.Empty: # se a fila estiver vazia
                    continue 
                except Exception as e:
                    print(f"ERRO WORKER {e}")
                    break
                    
            elif tipo == "TIPO:CLIENTE": 
                try:
                    data = p.receber_mensagem(conn) 
                    if not data:
                        print(f"DESCONEXÃO Cliente {addr} desconectou.")
                        break
                        
                    print(f"CLIENTE {addr} Solicitou: {data}")
                    f_in.put(data)
                    
                    # Repensar lógica de output único p/ caso tenha vários clientes
                    while True:
                        try:
                            result = f_out.get(timeout=5) 
                            p.enviar_mensagem(conn, result)
                            break # Sai do loop de espera do resultado, volta a aguardar novo input do cliente
                        except queue.Empty:
                            print(f"CLIENTE {addr} Aguardando...")
                            
                except Exception as e:
                    print(f"ERRO CLIENTE {e}")
                    break
            else:
                print(f"ERRO Tipo desconhecido: {tipo}")
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