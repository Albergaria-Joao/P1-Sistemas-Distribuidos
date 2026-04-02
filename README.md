# Sistema Distribuído de Cálculo: Arquitetura Master-Worker

Este projeto implementa um sistema distribuído em Python baseado no modelo **Master-Worker**. Ele utiliza comunicação via Sockets TCP puros para processar operações matemáticas de forma assíncrona e distribuída. O coordenador atua como um *broker* central, gerenciando o balanceamento de carga entre múltiplos nós trabalhadores (*workers*) e roteando os resultados de volta para os clientes corretos de forma isolada.

Projeto desenvolvido para a disciplina de Sistemas Distribuídos, ministrada pelo Prof. Dr. Carlos Caetano de Almeida.

Autores:
* Gabriel Palace Novaes Henrique | RA 202310491
* João Vítor Albergaria Barbosa | RA 202310501

FACAMP - Faculdades de Campinas | Engenharia da Computação

## Arquitetura e Decisões de Design

O sistema foi desenhado para lidar com os principais desafios de sistemas distribuídos:

* **Message Framing (Enquadramento):** Para contornar a natureza de fluxo contínuo (stream) do TCP e evitar a aglutinação ou fragmentação de mensagens, foi implementado um protocolo de camada de aplicação em que toda mensagem é prefixada com um cabeçalho de 4 bytes (`struct` em formato *Big-Endian*) que indica o tamanho exato do *payload*.
* **Concorrência Thread-per-Connection:** O nó coordenador suporta múltiplos clientes e *workers* simultaneamente. O loop principal de `accept()` delega cada nova conexão de socket para uma *thread* isolada.
* **Demultiplexação de Respostas:** Para evitar condição de corrida entre múltiplos clientes aguardando resultados, o Coordenador injeta um ID único para cada cliente conectado. As tarefas são envelopadas com esse ID antes de entrarem na fila de trabalho global. Quando o *worker* devolve o resultado, o coordenador roteia o dado estritamente para a `queue.Queue` específica daquele ID de cliente.
* **Graceful Shutdown:** Implementação de uma *sentinela* de controle (mensagem `FIM`). O cliente avisa ativamente que esgotou sua carga de trabalho, permitindo que as *threads* e os *sockets* sejam encerrados limpos e sem perdas de dados.

## Estrutura dos Componentes

O projeto é modularizado em 4 componentes fundamentais:

* `protocolo.py`: A espinha dorsal da comunicação de rede. Abstrai a manipulação dos *sockets* (leitura e escrita) e garante o empacotamento/desempacotamento (*Message Framing*) e a decodificação segura dos bytes para *strings*. Contém a definição da sentinela `FIM`.
* `coordenador.py`: O nó *Master*. Abre a porta TCP e faz o *listen*. Executa o *handshake* de aplicação para distinguir *workers* de clientes. Mantém uma fila *thread-safe* (`queue.Queue`) para tarefas pendentes e um dicionário de filas para o roteamento reverso dos resultados.
* `worker.py`: O nó de processamento. Conecta-se ao Coordenador informando sua tipagem. Fica em *idle* aguardando requisições, faz o *parsing* matemático, calcula a operação e devolve o *payload* do resultado ao *Master*. É estritamente sem estado (*stateless*).
* `cliente.py`: O nó gerador de carga. Submete as expressões matemáticas para cálculo. Utiliza uma *thread* separada dedicada exclusivamente a fazer o *polling* das respostas retornadas pelo Coordenador, permitindo o envio de mensagens sem bloqueio (*non-blocking* na perspectiva do loop de envio).

## Como Executar

A inicialização dos processos deve ser feita de forma descentralizada. Em um ambiente de produção, cada componente rodaria em um host/container distinto. Para testes locais, utilize terminais isolados.

**1. Inicie o Coordenador (Master)**
O Coordenador deve ser o primeiro a subir para realizar o `bind` da porta TCP.
```bash
python coordenador.py
```

**2. Provisione os Workers**
```bash
python worker.py
```
*(Repita este comando em diferentes terminais para escalar horizontalmente a capacidade de processamento).*

**3. Inicie os Clientes (Geração de Carga)**
```bash
python cliente.py
```
O log do `coordenador.py` registrará as conexões (*handshakes*), o balanceamento da fila e a roteirização do cálculo por ID.
