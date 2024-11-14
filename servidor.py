from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def escutar_cliente(cliente_socket, endereco_cliente):
    while True:
        try:
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Conexão com {endereco_cliente} encerrada.')
                cliente_socket.close()
                break
            print(f'Mensagem recebida do cliente. ({endereco_cliente}): {mensagem.decode()}')
        except ConnectionResetError:
            print(f'Cliente {endereco_cliente} desconectado.')
            cliente_socket.close()
            break


def enviar_para_cliente(cliente_socket):
    while True:
        try:
            mensagem = input("Digite sua mensagem para o cliente: ")
            cliente_socket.send(mensagem.encode())
        except (BrokenPipeError, ConnectionResetError):
            print("Erro ao enviar mensagem. Cliente desconectado.")
            cliente_socket.close()
            break


def iniciar_servidor():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen()
    print('Servidor aguardando conexões na porta 8000')

    while True:
        cliente_socket, endereco_cliente = server_socket.accept()
        print(f'Conexão estabelecida com {endereco_cliente}')
        Thread(target=escutar_cliente, args=(cliente_socket, endereco_cliente)).start()
        Thread(target=enviar_para_cliente, args=(cliente_socket,)).start()

if __name__ == "__main__":
    iniciar_servidor()
