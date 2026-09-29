import socket

HOST = "127.0.0.1"
PORT = 1211

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Digite uma mensagem: ")
    socket_udp.sendto(message.encode(), (HOST, PORT))
    data, addr = socket_udp.recvfrom(1024)
    print(f"Resposta recebida de {addr}: {data.decode()}")