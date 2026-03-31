import socket

HOST = "127.0.0.1"
# Aqui a gente implementa o TCP, questões de cabeçalho, etc


def enviar_mensagem(conexao, mensagem):
    conexao.sendall(mensagem.encode("utf-8")) # Manda a mensagem codificada
        
def receber_mensagem(conexao):
    data = conexao.recv(1024) 
    if not data:
        return 
    return data
    