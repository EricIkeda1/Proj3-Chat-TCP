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

# Solicitação do texto plano apenas se RC4 for selecionada
texto_plano = ""
if escolha == '5':
    texto_plano = input("Digite o texto plano: ")

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

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Alfabeto original
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'  # Alfabeto substituído
    
    chave = chave.upper()  # Converte a chave para maiúsculas
    
    if criptografar:
        # Cria um mapa de substituição usando o alfabeto original e substituído
        mapa_chave = {alfabeto[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        # Cria um mapa de substituição invertido para descriptografar
        mapa_chave = {alfabeto_substituido[i]: alfabeto[i] for i in range(26)}

    resultado = ''  # Inicializa a string para armazenar o resultado
    for caractere in mensagem.upper():  # Converte a mensagem para maiúsculas e itera sobre cada caractere
        resultado += mapa_chave.get(caractere, caractere)  # Substitui o caractere ou mantém o original
    return resultado  # Retorna a mensagem criptografada ou descriptografada


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
    resultado = ''
    chave = chave.lower()
    indice_chave = 0
    
    for caractere in mensagem:
        if caractere.isalpha():
            deslocamento = ord(chave[indice_chave]) - ord('a')
            deslocamento = deslocamento if criptografar else -deslocamento
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
            indice_chave = (indice_chave + 1) % len(chave)
        else:
            resultado += caractere
    return resultado

# Função RC4
def rc4(key, text):
    S = list(range(256))
    j = 0
    key_length = len(key)
    
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))
    
    return ''.join(result)

# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem, escolha, chave):
    if escolha == '5':  # RC4
        chave_bytes = chave  # Para RC4, a chave deve ser uma string de bytes
        return rc4(chave_bytes, mensagem)
    else:
        # Outras cifras podem ser implementadas aqui
        return mensagem

# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem, escolha, chave):
    if escolha == '1':
        return cifra_de_cesar(mensagem, int(chave))
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)
    elif escolha == '3':
        return cifra_de_playfair(mensagem, chave)
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)
    else:
        return mensagem

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            if escolha == '5':  # RC4
                print(f"Texto Plano: {texto_plano}")
                texto_plano_ascii = [ord(c) for c in texto_plano]
                print(f"Texto Plano ASCII: {texto_plano_ascii}")
                mensagem_criptografada = criptografar_mensagem(texto_plano, escolha, chave)
                print(f"Texto Criptografado: {[ord(c) for c in mensagem_criptografada]}")
                print(f"Chave: {chave}")
                chave_ascii = [ord(c) for c in chave]
                print(f"Chave ASCII: {chave_ascii}")
            else:
                print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break
        
# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))
        mensagem_criptografada = criptografar_mensagem(mensagem, escolha, chave)
        if escolha == '5':  # RC4
            print(f"Texto Criptografado a ser enviado: {[ord(c) for c in mensagem_criptografada]}")
        cliente.send(''.join(mensagem_criptografada).encode('ascii'))
        
# Solicitação do IP do servidor e da porta
ip_servidor = input("Digite o IP do servidor: ")
porta_servidor = int(input("Digite a porta do servidor: "))

# Conectando ao servidor
apelido = input("Escolha seu apelido: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Iniciando threads para envio e recebimento de mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()