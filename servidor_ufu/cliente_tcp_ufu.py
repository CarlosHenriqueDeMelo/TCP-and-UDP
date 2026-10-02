import socket

HOST = "10.0.99.150"
PORT = 1211

socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.connect((HOST, PORT))

boas_vindas = socketTCP.recv(1024)
print(boas_vindas.decode())

while True:
    mensagem = input("Digite uma mensagem (/help para ajuda, /quit para sair): ")
    socketTCP.sendall(mensagem.encode())

    resposta = socketTCP.recv(1024)
    print(resposta.decode())

    if mensagem.strip().lower() == "/quit":
        break

socketTCP.close()