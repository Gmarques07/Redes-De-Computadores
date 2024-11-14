from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def enviar_mensagens(s):
    while True:
        try:
            mensagem = input("Digite sua mensagem para o servidor: ")
            s.send(mensagem.encode())
        except BrokenPipeError:
            print("Conexão com o servidor foi interrompida.")
            break
        except KeyboardInterrupt:
            print("Encerrando o cliente.")
            s.close()
            break

def escutar_mensagens(s):
    while True:
        try:
            mensagem = s.recv(1500)
            if not mensagem:
                print("Conexão com o servidor encerrada.")
                s.close()
                break
            print(f'Mensagem recebida do servidor: {mensagem.decode()}')
        except ConnectionResetError:
            print("Servidor desconectado.")
            s.close()
            break

def main():
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 8000))
        print('Conectado ao servidor na porta 8000')

        # Iniciar threads para enviar e escutar mensagens
        Thread(target=enviar_mensagens, args=(s,)).start()
        Thread(target=escutar_mensagens, args=(s,)).start()
    except ConnectionRefusedError:
        print("Servidor não está disponível. Tente novamente mais tarde.")
        s.close()

if __name__ == "__main__":
    main()
