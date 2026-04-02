import socket
import protocolo as p
import time

HOST = "127.0.0.1"
PORT = 65432 # Porta do servidor em que vai conectar

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:WORKER") # Envia a mensagem de handshake indicando que é worker
    print("CONECTEI")

    while True:
        print("RECEBENDO")
        data = p.receber_mensagem(s) # Recebe tarefa repassada pelo coordenador
        print(data)

        if not data or data == p.SENTINELA: # se parar de receber ou receber a mensagem de fim, encerra
            print("ENCERRANDO worker.")
            break

        try:
            # Verifica os operadores e faz a operação solicitada
            if "+" in data:
                nums = data.split("+")
                result = float(nums[0]) + float(nums[1])
            elif "-" in data:
                nums = data.split("-")
                result = float(nums[0]) - float(nums[1])
            elif "*" in data:
                nums = data.split("*")
                result = float(nums[0]) * float(nums[1])
            elif "/" in data:
                nums = data.split("/")
                if float(nums[1]) == 0: # Lida com a divisão por zero
                    raise ZeroDivisionError("divisão por zero")
                result = float(nums[0]) / float(nums[1])
            else:
                p.enviar_mensagem(s, "ERRO: operador inválido")
                continue

            resposta = f"{data} = {result}"
            print(resposta)
            p.enviar_mensagem(s, resposta)

        except (ValueError, ZeroDivisionError) as e:
            p.enviar_mensagem(s, f"ERRO: {e}")

        time.sleep(0.1) # delay de 0.1 segundos para ajudar na visualização dos prints, pode ser removido para enviar mais rápido