import socket

HOST = "127.0.0.1"
PORT = 1211

socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.connect((HOST, PORT))

mensagem = input("Digite uma mensagem: ")
socketTCP.sendall(mensagem.encode())

resposta = socketTCP.recv(1024)
print(f"Resposta recebida: {resposta.decode()}")

socketTCP.close()