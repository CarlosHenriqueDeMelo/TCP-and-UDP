import socket
import datetime
import platform

HOST = "127.0.0.1"
PORT = 1211

# Textos de ajuda de cada comando (descrições em português)
AJUDA_GERAL = (
    "Comandos disponíveis:\n"
    "  /calc <n1> <op> <n2>  - Realiza uma operação matemática (+, -, *, /)\n"
    "  /time                 - Mostra a hora atual do servidor\n"
    "  /whoami               - Mostra seu endereço IP e porta\n"
    "  /serverinfo           - Mostra informações do sistema do servidor\n"
    "  /help                 - Lista todos os comandos\n"
    "  /help <comando>       - Mostra detalhes de um comando específico\n"
    "  /quit                 - Encerra a conexão\n"
    "Qualquer outra mensagem enviada sem '/' será devolvida como eco."
)

AJUDA_CALC = (
    "/calc <n1> <op> <n2>\n"
    "Realiza uma operação matemática entre dois números.\n"
    "Operadores aceitos: + (soma), - (subtração), * (multiplicação), / (divisão)\n"
    "Exemplo: /calc 10 + 5"
)

AJUDA_TIME = (
    "/time\n"
    "Devolve a data e hora atuais do servidor, no formato DD/MM/AAAA HH:MM:SS."
)

AJUDA_WHOAMI = (
    "/whoami\n"
    "Devolve o endereço IP e a porta de origem usados na sua conexão atual."
)

AJUDA_QUIT = (
    "/quit\n"
    "Encerra a conexão atual de forma organizada, avisando o servidor antes de sair."
)

AJUDA_COMANDOS = {
    "calc": AJUDA_CALC,
    "time": AJUDA_TIME,
    "whoami": AJUDA_WHOAMI,
    "quit": AJUDA_QUIT,
    "help": "/help\nLista os comandos disponíveis, ou detalha um comando específico se informado.",
}


def processar_calc(partes):
    """Trata o comando /calc, incluindo validação de erros."""
    if len(partes) != 4:
        return "Erro: uso correto é /calc <n1> <op> <n2> (ex: /calc 10 + 5)"

    _, n1_str, operador, n2_str = partes

    try:
        n1 = float(n1_str)
        n2 = float(n2_str)
    except ValueError:
        return "Erro: os valores informados precisam ser números."

    if operador == "+":
        resultado = n1 + n2
    elif operador == "-":
        resultado = n1 - n2
    elif operador == "*":
        resultado = n1 * n2
    elif operador == "/":
        if n2 == 0:
            return "Erro: não é possível dividir por zero."
        resultado = n1 / n2
    else:
        return f"Erro: operador '{operador}' não reconhecido. Use +, -, * ou /."

    return f"Resultado: {resultado}"


def processar_mensagem(texto, addr):
    """Decide o que fazer com a mensagem recebida e devolve a resposta (str)."""
    texto_limpo = texto.strip()

    # Mensagem sem "/" no início -> apenas eco
    if not texto_limpo.startswith("/"):
        return texto

    partes = texto_limpo.split()
    comando = partes[0].lower()

    if comando == "/calc":
        return processar_calc(partes)

    if comando == "/time":
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"Hora do servidor: {agora}"

    if comando == "/whoami":
        return f"Seu endereço: {addr[0]}, porta: {addr[1]}"

    if comando == "/serverinfo":
        so = platform.system()
        versao = platform.release()
        arquitetura = platform.machine()
        return f"Servidor rodando em: {so} {versao} ({arquitetura})"

    if comando == "/help":
        if len(partes) == 1:
            return AJUDA_GERAL
        nome_comando = partes[1].lower()
        if nome_comando in AJUDA_COMANDOS:
            return AJUDA_COMANDOS[nome_comando]
        return f"Comando '{nome_comando}' não encontrado. Digite /help para ver a lista completa."

    # Comando desconhecido, mas começou com "/"
    return f"Comando '{comando}' não reconhecido. Digite /help para ver os comandos disponíveis."


def atender_cliente(conn, addr):
    """Cuida de toda a conversa com um cliente, do início ao /quit."""
    print(f"Conexão estabelecida com: {addr}")

    # Mensagem de boas-vindas assim que a conexão é aberta
    boas_vindas = "Conectado ao servidor. Digite /help para ver os comandos disponíveis."
    conn.sendall(boas_vindas.encode())

    while True:
        data = conn.recv(1024)

        # Cliente fechou o terminal/conexão abruptamente
        if not data:
            print(f"Cliente {addr} desconectou (conexão encerrada).")
            break

        texto = data.decode()
        print(f"Mensagem recebida de {addr}: {texto}")

        if texto.strip().lower() == "/quit":
            conn.sendall("Encerrando conexão. Até logo!".encode())
            print(f"Cliente {addr} solicitou /quit.")
            break

        resposta = processar_mensagem(texto, addr)
        conn.sendall(resposta.encode())

    conn.close()


def main():
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketTCP.bind((HOST, PORT))
    socketTCP.listen(1)

    print(f"Servidor TCP escutando em: {HOST}:{PORT}")

    while True:
        conn, addr = socketTCP.accept()
        atender_cliente(conn, addr)


if __name__ == "__main__":
    main()