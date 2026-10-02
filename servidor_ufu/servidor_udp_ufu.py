import socket
import datetime
import platform
import platform

HOST = "0.0.0.0"
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
    "  /quit                 - Encerra o programa cliente\n"
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
    "Devolve o endereço IP e a porta de origem usados no seu último datagrama enviado."
)

AJUDA_QUIT = (
    "/quit\n"
    "Encerra o programa cliente localmente.\n"
    "Como o UDP não usa conexão, o servidor não precisa ser avisado: ele\n"
    "continua no ar, pronto para atender outros datagramas a qualquer momento."
)

AJUDA_SERVERINFO = (
    "/serverinfo\n"
    "Mostra informações somente-leitura sobre o sistema onde o servidor está rodando\n"
    "(sistema operacional, versão e arquitetura). Não executa nenhum comando do\n"
    "sistema — por segurança, o servidor nunca roda comandos arbitrários vindos da rede."
)

AJUDA_COMANDOS = {
    "calc": AJUDA_CALC,
    "time": AJUDA_TIME,
    "whoami": AJUDA_WHOAMI,
    "quit": AJUDA_QUIT,
    "serverinfo": AJUDA_SERVERINFO,
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

    if comando == "/quit":
        # No UDP o /quit é tratado apenas no cliente (não há conexão a encerrar aqui),
        # mas respondemos de forma amigável caso o servidor receba esse comando.
        return "Este servidor UDP não mantém conexão; para sair, use /quit no seu cliente."

    # Comando desconhecido, mas começou com "/"
    return f"Comando '{comando}' não reconhecido. Digite /help para ver os comandos disponíveis."


def main():
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_udp.bind((HOST, PORT))

    print(f"Servidor UDP escutando em: {HOST}:{PORT}")

    while True:
        data, addr = socket_udp.recvfrom(1024)
        texto = data.decode()
        print(f"Mensagem recebida de {addr}: {texto}")

        resposta = processar_mensagem(texto, addr)
        socket_udp.sendto(resposta.encode(), addr)


if __name__ == "__main__":
    main()