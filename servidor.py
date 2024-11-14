from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

clientes_conectados = {}

def enviar_mensagem_para_cliente(mensagem, destinatario):
    if destinatario in clientes_conectados:
        try:
            clientes_conectados[destinatario].send(mensagem.encode())
        except BrokenPipeError:
            print(f"Erro ao enviar mensagem para {destinatario}.")
    else:
        print(f"Destinatário {destinatario} não encontrado.")


def conexao_cliente(cliente_socket, endereco_cliente):

    cliente_socket.send("Identifique-se: ".encode())
    nome_cliente = cliente_socket.recv(1500).decode()
    print(f'Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente})')

    clientes_conectados[nome_cliente] = cliente_socket

    try:
        while True:
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Cliente {nome_cliente} desconectado.')
                break

            mensagem_decodificada = mensagem.decode()
            print(f'Mensagem recebida de {nome_cliente} ({endereco_cliente}): {mensagem_decodificada}')


            if ':' in mensagem_decodificada:
                destinatario, conteudo = mensagem_decodificada.split(":", 1)
                destinatario = destinatario.strip()
                conteudo = conteudo.strip()

                enviar_mensagem_para_cliente(f"Mensagem de {nome_cliente}: {conteudo}", destinatario)
            else:
                cliente_socket.send("Formato de mensagem inválido. Use 'destinatario: mensagem'.".encode())
    except ConnectionResetError:
        print(f"Cliente {nome_cliente} desconectado abruptamente.")
    finally:

        clientes_conectados.pop(nome_cliente, None)
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