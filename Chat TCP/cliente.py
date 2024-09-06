import socket
import threading

# Escolha da cifra de criptografia pelo usuário
print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")
print("5. RC4")
escolha = input("Digite o número da cifra desejada: ")

# Solicitação da chave de criptografia
chave = input("Digite a chave para a cifra escolhida: ")

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''
    deslocamento = int(chave) if criptografar else -int(chave)
    for caractere in mensagem:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere
    return resultado

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
    
    chave = chave.upper()
    
    if criptografar:
        mapa_chave = {alfabeto[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        mapa_chave = {alfabeto_substituido[i]: alfabeto[i] for i in range(26)}

    resultado = ''
    for caractere in mensagem.upper():
        resultado += mapa_chave.get(caractere, caractere)
    return resultado

# Função que implementa a Cifra de Playfair
def cifra_de_playfair(mensagem, chave, criptografar=True):
    def formatar_mensagem(mensagem):
        mensagem = mensagem.replace(' ', '').upper()
        formatada = ''
        i = 0
        while i < len(mensagem):
            if i == len(mensagem) - 1:
                formatada += mensagem[i] + 'X'
                i += 1
            elif mensagem[i] == mensagem[i + 1]:
                formatada += mensagem[i] + 'X'
                i += 1
            else:
                formatada += mensagem[i] + mensagem[i + 1]
                i += 2
        return formatada

    def criar_matriz(chave):
        alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        matriz = []
        for caractere in chave.upper():
            if caractere not in matriz and caractere != 'J':
                matriz.append(caractere)
        for caractere in alfabeto:
            if caractere not in matriz:
                matriz.append(caractere)
        return [matriz[i:i + 5] for i in range(0, 25, 5)]

    def encontrar_posicao(matriz, caractere):
        for i, linha in enumerate(matriz):
            for j, valor in enumerate(linha):
                if valor == caractere:
                    return i, j

    mensagem = formatar_mensagem(mensagem)
    matriz = criar_matriz(chave)
    resultado = ''
    
    for i in range(0, len(mensagem), 2):
        linha1, coluna1 = encontrar_posicao(matriz, mensagem[i])
        linha2, coluna2 = encontrar_posicao(matriz, mensagem[i + 1])

        if linha1 == linha2:
            coluna1 = (coluna1 + 1) % 5 if criptografar else (coluna1 - 1) % 5
            coluna2 = (coluna2 + 1) % 5 if criptografar else (coluna2 - 1) % 5
        elif coluna1 == coluna2:
            linha1 = (linha1 + 1) % 5 if criptografar else (linha1 - 1) % 5
            linha2 = (linha2 + 1) % 5 if criptografar else (linha2 - 1) % 5
        else:
            coluna1, coluna2 = coluna2, coluna1

        resultado += matriz[linha1][coluna1] + matriz[linha2][coluna2]
    
    return resultado

# Função que implementa a Cifra de Vigenère
def cifra_de_vigenere(mensagem, chave, criptografar=True):
    texto_criptografado = ""
    chave = chave.upper()
    tamanho_chave = len(chave)
    
    # Repetir a chave para que seu tamanho seja igual ao do texto
    chave_repetida = (chave * (len(mensagem) // tamanho_chave + 1))[:len(mensagem)]

    for i in range(len(mensagem)):
        caractere = mensagem[i]
        if caractere.isalpha():
            caractere_chave = chave_repetida[i]
            deslocamento_chave = ord(caractere_chave) - ord('A')

            if criptografar:
                if caractere.isupper():
                    texto_criptografado += chr((ord(caractere) - ord('A') + deslocamento_chave) % 26 + ord('A'))
                else:
                    texto_criptografado += chr((ord(caractere) - ord('a') + deslocamento_chave) % 26 + ord('a'))
            else:
                if caractere.isupper():
                    texto_criptografado += chr((ord(caractere) - ord('A') - deslocamento_chave) % 26 + ord('A'))
                else:
                    texto_criptografado += chr((ord(caractere) - ord('a') - deslocamento_chave) % 26 + ord('a'))
        else:
            texto_criptografado += caractere

    return texto_criptografado

# Função que implementa o RC4
def rc4(mensagem, chave):
    def ksa(chave):
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + chave[i % len(chave)]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def prga(S, texto):
        i = 0
        j = 0
        resultado = []
        for caractere in texto:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % 256
            resultado.append(chr(ord(caractere) ^ S[t]))
        return ''.join(resultado)

    chave = [ord(c) for c in chave]
    S = ksa(chave)
    return prga(S, mensagem)


# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem):
    if escolha == '1':
        return cifra_de_cesar(mensagem, chave)  # Chave já é um número inteiro agora
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)
    elif escolha == '3':
        return cifra_de_playfair(mensagem, chave)
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)
    elif escolha == '5':
        return rc4(mensagem, chave)
    else:
        return mensagem

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break

# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))
        mensagem_criptografada = criptografar_mensagem(mensagem)
        cliente.send(mensagem_criptografada.encode('ascii'))

# Conectando ao servidor
apelido = input("Escolha seu apelido: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Iniciando threads para envio e recebimento de mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
