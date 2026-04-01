import socket
import struct
HOST = "127.0.0.1"
# Aqui a gente implementa o TCP, questões de cabeçalho, etc

def cabecalho(dados):
    tamanho = len(dados)
    cabecalho = struct.pack(">I", tamanho) # Empacota o tamanho da mensagem como uminteiro unsigned big endian de 4 bytes
    return cabecalho

def enviar_mensagem(conexao, mensagem):
    dados = str(mensagem).encode("utf-8")
    conexao.sendall(cabecalho(dados) + dados) # Manda a mensagem codificada com cabeçalho
    # Se não tiver cabeçalho indicando o tamanho, o TCP manda tudo junto numa mensagem só e aí ferra com a soma
        
def receber_bytes(conexao, num_bytes):
    buffer = bytearray()

    while len(buffer) < num_bytes: # vai jogando no buffer byte a byte
        pacote = conexao.recv(num_bytes - len(buffer))
        if not pacote: # se quebrar a conexão no meio
            return None
        buffer.extend(pacote)
    return buffer

def receber_mensagem(conexao):
    cabecalho = receber_bytes(conexao, 4) # pega os 4 primeiros bytes da mensagem (cabeçalho)
    if not cabecalho:
        return None
    tamanho = struct.unpack(">I", cabecalho)[0]
    
    dados_mensagem = receber_bytes(conexao, tamanho) #pega o resto
    if not dados_mensagem:
        return None

    return dados_mensagem.decode("utf-8")
    
def conectar_servidor(host, port, tipo = "WORKER"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    enviar_mensagem(s, f"TIPO:{tipo}")
    return s
