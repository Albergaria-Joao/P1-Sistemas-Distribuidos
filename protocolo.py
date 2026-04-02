import socket
import struct

SENTINELA = "FIM" # Mensagem que vai indicar o fim da comunicação

def cabecalho(dados):
    tamanho = len(dados)
    cabecalho = struct.pack(">I", tamanho) # Empacota o tamanho da mensagem como um inteiro unsigned big endian de 4 bytes
    return cabecalho

def enviar_mensagem(conexao, mensagem):
    dados = str(mensagem).encode("utf-8")
    conexao.sendall(cabecalho(dados) + dados) # Envia a mensagem codificada com cabeçalho
    # Se não tiver cabeçalho indicando o tamanho, o receptor pode não saber quando a mensagem termina, podendo resultar em mensagens truncadas ou misturadas
    # Ex: o cliente manda "3+4" e logo depois "5*6", o coordenador pode receber "3+45*6" se não tiver um jeito de delimitar as mensagens

def receber_bytes(conexao, num_bytes):
    buffer = bytearray()
    while len(buffer) < num_bytes: # Pega a mensagem byte a byte
        pacote = conexao.recv(num_bytes - len(buffer))
        if not pacote:
            return None
        buffer.extend(pacote)
    return buffer

def receber_mensagem(conexao):
    cabecalho = receber_bytes(conexao, 4) # Recebe o cabeçalho de 4B para saber o tamanho da mensagem
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