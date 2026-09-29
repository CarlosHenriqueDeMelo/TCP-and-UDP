import socket

HOST = "127.0.0.1"
PORT = 1211

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind((HOST, PORT))

print(f"Servidor UDP escutando em: {HOST}:{PORT}")

while True:
    data, addr = socket_udp.recvfrom(1024)  
    print(f"Mensagem recebida de {addr}: {data.decode()}")
    socket_udp.sendto(data, addr)



