import socket
import protocolo as p
import threading
import queue
import uuid

HOST = "127.0.0.1"
PORT = 65432

fila_inputs = queue.Queue()  # agora carrega (client_id, task)
filas_outputs = {}           # dict: client_id -> Queue
lock_outputs = threading.Lock()

def lidar_conexao(conn, addr, f_in):
    with conn:
        mensagem_inicial = p.receber_mensagem(conn)
        if not mensagem_inicial:
            return

        tipo = mensagem_inicial.strip()
        print(f"[HANDSHAKE] {addr} {tipo}")

        while True:
            if tipo == "TIPO:WORKER":
                try:
                    client_id, task = f_in.get(timeout=1)

                    p.enviar_mensagem(conn, task)

                    result = p.receber_mensagem(conn)
                    if not result:
                        print(f"DESCONEXÃO Worker {addr} caiu")
                        f_in.put((client_id, task))  # devolve pra fila
                        break

                    print(f"WORKER {addr} Retornou: {result}")

                    with lock_outputs:
                        if client_id in filas_outputs:
                            filas_outputs[client_id].put(result)

                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"ERRO WORKER {e}")
                    break

            elif tipo == "TIPO:CLIENTE":
                client_id = str(uuid.uuid4())
                f_out = queue.Queue()

                with lock_outputs:
                    filas_outputs[client_id] = f_out

                print(f"[CLIENTE] {addr} registrado como {client_id[:8]}")

                try:
                    while True:
                        data = p.receber_mensagem(conn)
                        if not data or data == p.SENTINELA:
                            print(f"DESCONEXÃO Cliente {addr} desconectou.")
                            break

                        print(f"CLIENTE {addr} Solicitou: {data}")
                        f_in.put((client_id, data))

                        while True:
                            try:
                                result = f_out.get(timeout=5)
                                p.enviar_mensagem(conn, result)
                                break
                            except queue.Empty:
                                print(f"CLIENTE {addr} Aguardando...")

                except Exception as e:
                    print(f"ERRO CLIENTE {e}")
                finally:
                    with lock_outputs:
                        del filas_outputs[client_id]

                break
            else:
                print(f"ERRO Tipo desconhecido: {tipo}")
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("ouvindo")
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=lidar_conexao, args=(conn, addr, fila_inputs))
        thread.start()
        print(f"[SISTEMA] Threads ativas: {threading.active_count() - 1}")