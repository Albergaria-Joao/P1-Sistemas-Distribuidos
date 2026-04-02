import socket
import protocolo as p
import time

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    p.enviar_mensagem(s, "TIPO:WORKER")
    print("CONECTEI")

    while True:
        print("RECEBENDO")
        data = p.receber_mensagem(s)
        print(data)

        if not data or data == p.SENTINELA:
            print("ENCERRANDO worker.")
            break

        try:
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
                if float(nums[1]) == 0:
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

        time.sleep(0.5)