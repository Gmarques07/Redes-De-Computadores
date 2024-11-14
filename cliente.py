from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def escutar_servidor(s):
    while True:
        try:
            mensagem = s.recv(1500)
            if not mensagem:
                print("Conexão com o servidor encerrada.")
                break
            print(f'Mensagem recebida do servidor: {mensagem.decode()}')
        except ConnectionResetError:
            print("Servidor desconectado.")
            break


def enviar_para_servidor(s):
    while True:
        try:
            mensagem = input("Digite sua mensagem para o servidor: ")
            if mensagem.lower() == 'sair':
                s.send('Cliente desconectado'.encode())
                break
            s.send(mensagem.encode())
        except BrokenPipeError:
            print("Conexão com o servidor foi perdida.")
            break
        except KeyboardInterrupt:
            print("Finalizando o cliente.")
            s.close()
            break


s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 8000))


nome_cliente = input("Identifique-se: ")
s.send(nome_cliente.encode())

print(f'Conectado ao servidor na porta 8000 como {nome_cliente}')


Thread(target=escutar_servidor, args=(s,)).start()
Thread(target=enviar_para_servidor, args=(s,)).start()
