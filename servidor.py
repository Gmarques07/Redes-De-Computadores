from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

clientes_conectados = []


def enviar_mensagem_para_cliente(mensagem, cliente_socket):
    try:
        cliente_socket.send(mensagem.encode())
    except BrokenPipeError:
        print(f"Erro ao enviar mensagem para o cliente.")


def conexao_cliente(cliente_socket, endereco_cliente):
    # Solicita o nome do cliente
    cliente_socket.send("Identifique-se: ".encode())
    nome_cliente = cliente_socket.recv(1500).decode()
    print(f'Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente})')

    clientes_conectados.append(cliente_socket)

    try:
        while True:
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Cliente {nome_cliente} desconectado.')
                break

            print(f'Mensagem recebida de {nome_cliente} ({endereco_cliente}): {mensagem.decode()}')

            resposta = input(f"Digite sua resposta para o cliente {nome_cliente} ({endereco_cliente}): ")
            cliente_socket.send(resposta.encode())
    except ConnectionResetError:
        print(f"Cliente {nome_cliente} desconectado abruptamente.")
    finally:

        clientes_conectados.remove(cliente_socket)
        cliente_socket.close()

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()
print('Servidor está pronto e aguardando conexões na porta 8000')


def gerenciar_conexoes():
    while True:
        cliente_socket, endereco_cliente = server_socket.accept()
        print(f"Cliente {endereco_cliente} conectado.")
        Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()

Thread(target=gerenciar_conexoes).start()
