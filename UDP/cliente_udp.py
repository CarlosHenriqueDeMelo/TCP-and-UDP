import socket

HOST = "127.0.0.1"
PORT = 1211

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Cliente UDP pronto. Digite /help para ver os comandos disponíveis.")

while True:
    mensagem = input("Digite uma mensagem (/help para ajuda, /quit para sair): ")

    if mensagem.strip().lower() == "/quit":
        print("Encerrando cliente. Até logo!")
        break

    socket_udp.sendto(mensagem.encode(), (HOST, PORT))
    data, addr = socket_udp.recvfrom(1024)
    print(data.decode())

socket_udp.close()