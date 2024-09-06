import socket
import threading

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''
    deslocamento = chave if criptografar else -chave
    for caractere in mensagem:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere
    return resultado

# Função que implementa o RC4
def rc4(mensagem, chave):
    S = list(range(256))
    T = [ord(chave[i % len(chave)]) for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    resultado = ''
    for caractere in mensagem:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        resultado += chr(ord(caractere) ^ k)
    
    return resultado

# Função que gerencia as mensagens recebidas dos clientes
def gerenciar_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            print(f"[Mensagem recebida]: {mensagem}")
            
            # Exemplo de criptografia e descriptografia com RC4
            chave = 'minha_chave'  # A chave precisa ser compartilhada entre o cliente e o servidor
            mensagem_descriptografada = rc4(mensagem, chave)
            print(f"[Mensagem descriptografada]: {mensagem_descriptografada}")

            transmitir_mensagem(mensagem, cliente)
        except:
            clientes.remove(cliente)
            cliente.close()
            break

# Função que transmite mensagens para todos os clientes
def transmitir_mensagem(mensagem, cliente):
    for cliente_conectado in clientes:
        if cliente_conectado != cliente:
            cliente_conectado.send(mensagem.encode('ascii'))

# Configurando o servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 55555))
servidor.listen()

clientes = []

# Aceitando conexões de clientes
while True:
    cliente, endereco = servidor.accept()
    print(f"Conectado a {endereco}")
    
    clientes.append(cliente)

    thread = threading.Thread(target=gerenciar_cliente, args=(cliente,))
    thread.start()
