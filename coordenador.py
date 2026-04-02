import socket
import protocolo as p
import threading
import queue
import uuid

HOST = "127.0.0.1"
PORT = 65432 # Porta que o servidor vai escutar

fila_inputs = queue.Queue()  # carrega (client_id, task)
filas_outputs = {}           # dict: client_id -> Queue para conseguirmos separar as respostas dos clientes
lock_outputs = threading.Lock() # MUTEX para evitar race condition no acesso ao dict de output

def lidar_conexao(conn, addr, f_in):
    with conn:
        mensagem_inicial = p.receber_mensagem(conn)
        if not mensagem_inicial:
            return

        tipo = mensagem_inicial.strip()
        print(f"[HANDSHAKE] {addr} {tipo}")

        while True: # Loop principal para lidar com a conexão
            # Verifica tipo da conexão
            if tipo == "TIPO:WORKER":
                try:
                    client_id, task = f_in.get(timeout=1) # Pega ID do cliente e tarefa da fila de inputs, espera 1s pra não travar a thread caso não tenha nada

                    p.enviar_mensagem(conn, task) # Envia para o worker

                    result = p.receber_mensagem(conn) # Recebe o resultado
                    
                    if not result:
                        print(f"DESCONEXÃO Worker {addr} caiu")
                        f_in.put((client_id, task))  # devolve pra fila
                        break

                    print(f"WORKER {addr} Retornou: {result}")

                    with lock_outputs: # usando mutex para não dar conflito entre as threads
                        if client_id in filas_outputs:
                            filas_outputs[client_id].put(result) # Coloca o resultado na fila do cliente correspondente

                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"ERRO WORKER {e}")
                    break

            elif tipo == "TIPO:CLIENTE":
                client_id = str(uuid.uuid4()) # Gera um uuid para o cliente
                f_out = queue.Queue() # Cria uma fila de output para ele

                with lock_outputs: # usando mutex para não dar conflito entre as threads
                    filas_outputs[client_id] = f_out # Registra a fila do cliente no dict global, com a chave sendo o ID

                print(f"[CLIENTE] {addr} registrado como {client_id[:8]}")

                try:
                    while True:
                        data = p.receber_mensagem(conn) # Recebe mensagem do cliente
                        if not data or data == p.SENTINELA: # Se desconectar ou enviar a mensagem de fim, encerra
                            print(f"DESCONEXÃO Cliente {addr} desconectou.")
                            break

                        print(f"CLIENTE {addr} Solicitou: {data}")
                        f_in.put((client_id, data)) # Coloca na fila de inputs o ID do cliente e a tarefa, para um worker pegar

                        while True:
                            try:
                                result = f_out.get(timeout=5) # Fica esperando resultado na fila de output e envia para o cliente, espera 5s pra não travar a thread caso algo dê errado
                                p.enviar_mensagem(conn, result)
                                break
                            except queue.Empty:
                                print(f"CLIENTE {addr} Aguardando...")

                except Exception as e:
                    print(f"ERRO CLIENTE {e}")
                finally:
                    with lock_outputs: # usando mutex para não dar conflito entre as threads
                        del filas_outputs[client_id] # quando o cliente sai, remove a fila dele do dict global

                break
            else:
                print(f"ERRO Tipo desconhecido: {tipo}")
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("ouvindo")
    s.bind((HOST, PORT)) # Vincula o socket a um endereço e porta específicos
    s.listen()
    while True:
        # Esta thread principal serve para aceitar conexões e criar uma thread para cada uma, lidando com elas de forma concorrente
        conn, addr = s.accept()
        thread = threading.Thread(target=lidar_conexao, args=(conn, addr, fila_inputs))
        thread.start()
        print(f"[SISTEMA] Threads ativas: {threading.active_count() - 1}")