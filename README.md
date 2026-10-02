# TCP and UDP — 1ª Atividade Avaliativa (Cibersegurança/UFU)

Aplicações cliente-servidor em Python usando sockets UDP e TCP, desenvolvidas para a disciplina de Cibersegurança (Módulo 3 — Segurança WEB) da UFU.

## Estrutura do repositório

```
TCP-and-UDP/
├── UDP/
│   ├── servidor_udp.py
│   └── cliente_udp.py
├── TCP/
│   ├── servidor_tcp.py
│   └── cliente_tcp.py
└── servidor_ufu/
    ├── servidor_tcp_ufu.py   (HOST = 0.0.0.0, para rodar no servidor da turma)
    ├── cliente_tcp_ufu.py    (aponta para o IP do servidor da turma)
    ├── servidor_udp_ufu.py
    └── cliente_udp_ufu.py
```

As pastas `UDP/` e `TCP/` contêm as versões para rodar localmente (`127.0.0.1`), prontas para o professor testar sem nenhuma configuração extra. A pasta `servidor_ufu/` contém as versões já ajustadas para rodar entre máquinas diferentes, usadas na apresentação com o servidor da turma.

## Porta utilizada

Todas as aplicações usam a porta **1211** (1000 + últimos 3 dígitos da matrícula), conforme pedido no enunciado.

## Como executar (localmente)

**UDP:**
```bash
# Terminal 1
cd UDP
python3 servidor_udp.py

# Terminal 2
cd UDP
python3 cliente_udp.py
```

**TCP:**
```bash
# Terminal 1
cd TCP
python3 servidor_tcp.py

# Terminal 2
cd TCP
python3 cliente_tcp.py
```

## Sistema de comandos

Além da troca de dados básica, o servidor interpreta comandos enviados pelo cliente (qualquer mensagem sem `/` é devolvida como eco):

| Comando | Descrição |
|---|---|
| `/calc <n1> <op> <n2>` | Realiza uma operação matemática (`+`, `-`, `*`, `/`), com tratamento de erros (divisão por zero, valores inválidos) |
| `/time` | Mostra a data e hora atuais do servidor |
| `/whoami` | Mostra o endereço IP e a porta do cliente |
| `/serverinfo` | Mostra o sistema operacional, versão e arquitetura do servidor |
| `/help` | Lista todos os comandos disponíveis |
| `/help <comando>` | Mostra detalhes de um comando específico (ex: `/help calc`) |
| `/quit` | Encerra a conexão (TCP) ou o cliente (UDP) |

## Diferença de comportamento entre TCP e UDP

- **TCP**: a conexão permanece aberta, permitindo trocar múltiplas mensagens até o cliente enviar `/quit` ou fechar o programa (o servidor detecta a desconexão automaticamente).
- **UDP**: não há conceito de conexão — cada mensagem é tratada de forma independente. O comando `/quit` nesse caso só encerra o cliente localmente; o servidor continua no ar, pronto para atender outras mensagens.

## Testado em dois cenários

1. **Local**: cliente e servidor rodando na mesma máquina (`127.0.0.1`).
2. **Remoto**: cliente rodando na máquina local e servidor rodando no servidor da turma (arquivos da pasta `servidor_ufu/`).
