import socket
import struct

HOST = "127.0.0.1"
SENTINELA = "FIM"

def cabecalho(dados):
    tamanho = len(dados)
    cabecalho = struct.pack(">I", tamanho)
    return cabecalho

def enviar_mensagem(conexao, mensagem):
    dados = str(mensagem).encode("utf-8")
    conexao.sendall(cabecalho(dados) + dados)

def receber_bytes(conexao, num_bytes):
    buffer = bytearray()
    while len(buffer) < num_bytes:
        pacote = conexao.recv(num_bytes - len(buffer))
        if not pacote:
            return None
        buffer.extend(pacote)
    return buffer

def receber_mensagem(conexao):
    cabecalho = receber_bytes(conexao, 4)
    if not cabecalho:
        return None
    tamanho = struct.unpack(">I", cabecalho)[0]

    dados_mensagem = receber_bytes(conexao, tamanho)
    if not dados_mensagem:
        return None

    return dados_mensagem.decode("utf-8")

def conectar_servidor(host, port, tipo="WORKER"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    enviar_mensagem(s, f"TIPO:{tipo}")
    return s