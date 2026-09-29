import socket

HOST = "0.0.0.0"
PORT = 1211

socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind((HOST, PORT))
socketTCP.listen(1)

print(f"Servidor TCP escutando em: {HOST}:{PORT}")

while True:
    conn, addr = socketTCP.accept()
    print(f"Conexão estabelecida com: {addr}")
    data = conn.recv(1024)
    print(f"Mensagem recebida de {addr}: {data.decode()}")
    conn.sendall(data)
    conn.close()
