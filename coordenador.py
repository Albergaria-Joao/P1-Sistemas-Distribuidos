import socket
import protocolo as p

HOST = "127.0.0.1"  
PORT = 65432        # porta que o servidor vai ouvir

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    print("ouvindo")
    s.bind((HOST, 65432))
    s.listen()
    conn, addr = s.accept() # aceita a conexão na porta que está ouvindo. Addr é a porta do cliente (efêmera)
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = p.receber_mensagem(conn)
            if not data:
                continue
            print("recebeu")
            print(data)
            numbers = data.split("+")
            result = sum(map(int, numbers))
            print(result)
            mensagem = str(result)
            p.enviar_mensagem(conn, mensagem)