import pickle
import socket
import os
import sys
import time

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conecta o socket à porta que servidor está escutando
server_address = ('localhost', 5000)
sock.connect(server_address)

#recebe a mensagem do servidor
def recebeMensagem():
    data = sock.recv(4096)
    message = pickle.loads(data)
    time.sleep(0.1)
    return message

#recebe se der erro
def handleError():
    err = recebeMensagem()
    print(err)
#cria novo tabuleiro
def novoTabuleiro(dim):
    tabuleiro = []

    for i in range(0, dim):
        linha = []
        
        for j in range(0, dim):
            linha.append(0)

        tabuleiro.append(linha)

    # Cria uma lista de todas as posicoes do tabuleiro. Util para
    # sortearmos posicoes aleatoriamente para as pecas.
    posicoesDisponiveis = []
    for i in range(0, dim):

        for j in range(0, dim):
            posicoesDisponiveis.append((i, j))

    # Varre todas as pecas que serao colocadas no
    # tabuleiro e posiciona cada par de pecas iguais
    # em posicoes aleatorias.
    for j in range(0, dim // 2):
        for i in range(1, dim + 1):
            
            # Sorteio da posicao da segunda peca com valor 'i'
            indiceAleatorio = recebeMensagem()
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)
            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            indiceAleatorio = recebeMensagem()
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i
    return tabuleiro
#faz um novo placar
def novoPlacar(nJogadores):
    return [0] * nJogadores
#imprime status do tabuleiro
def imprimeStatus(tabuleiro, placar, nJogadores, vez):
        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar, nJogadores)
        sys.stdout.write('\n')

        sys.stdout.write('\n')
        var = recebeMensagem()
        print(var)
#imprime o tabuleiro
def imprimeTabuleiro(tabuleiro):
    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    sys.stdout.write("     ")

    for i in range(0, dim):
        sys.stdout.write("{0:2d} ".format(i))

    sys.stdout.write("\n")

    # Imprime separador horizontal
    sys.stdout.write("-----")

    for i in range(0, dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for i in range(0, dim):

        # Imprime coordenadas verticais
        sys.stdout.write("{0:2d} | ".format(i))

        # Imprime conteudo da linha 'i'
        for j in range(0, dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                sys.stdout.write(" - ")

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))

            else:

                # Nao, imprime '?'
                sys.stdout.write(" ? ")
                #sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))

        sys.stdout.write("\n")
#imprime o placar
def imprimePlacar(placar, nJogadores):
    print("Placar:")
    print("---------------------")
    for i in range(0, nJogadores):
        msg = recebeMensagem()
        print(msg)
#le as coordenadas inseridas pelo jogador e manda para o cliente
def leCoordenada(dim):

    var = input("Especifique uma peca: ")
    message = pickle.dumps(var)
    sock.send(message)

    try:
        i = int(var.split(' ')[0])
        j = int(var.split(' ')[1])

    except ValueError:
        handleError()

    if i < 0 or i >= dim:
        handleError()

    if j < 0 or j >= dim:
        handleError()

    i = recebeMensagem()
    j = recebeMensagem()

    return (i, j)

#limpa a tela
def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')
#abre a peça do tabuleiro
def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False
#incrementa o placar
def incrementaPlacar(placar, jogador):
    message = recebeMensagem()
    placar[jogador] = message

#remove a peça
def removePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = "-"
        return True

#fecha a peça
def fechaPeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Programa principal
limpaTela()
#recebe o seu id
id = recebeMensagem()
print("Você é o jogador número " + str(id + 1))
#recebe a qtd de jogadores
nJogadores = recebeMensagem()
#recebe o tamanho do tabuleiro
dim = recebeMensagem()
tabuleiro = novoTabuleiro(dim)
placar = novoPlacar(nJogadores)
totalDePares = dim**2 / 2
paresEncontrados = 0
vez = 0
#inicializa as variaveis (valor arbitrario)
i1 = 0
j1 = 0
i2 = 0
j2= 0

# Partida continua enquanto ainda ha pares de pecas a
# casar.
while paresEncontrados < totalDePares:

    imprimeStatus(tabuleiro, placar, nJogadores, vez)

    if (vez == id):
        while True:
            imprimeStatus(tabuleiro, placar, nJogadores, vez)

            coordenadas = leCoordenada(dim)

            if coordenadas == False:
                continue

            il, jl = coordenadas

            if abrePeca(tabuleiro, il, jl) == False:
                message = recebeMensagem()
                input(message)
                continue

            break
        while True:

            imprimeStatus(tabuleiro, placar, nJogadores, vez)

            coordenadas = leCoordenada(dim)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            if abrePeca(tabuleiro, i2, j2) == False:
                message = recebeMensagem()
                input(message)
                continue

            break
    else:
        imprimeStatus(tabuleiro, placar, nJogadores, vez)
        #erro foi encontrado e foi necessario adicionar variavel
        #sincronizar para consertá-lo
        sincronizar = recebeMensagem()
        sincronizar = recebeMensagem()
        sincronizar = recebeMensagem()

        i1 = recebeMensagem()
        j1 = recebeMensagem()

        abrePeca(tabuleiro, i1, j1)
        i2 = recebeMensagem()

        j2 = recebeMensagem()
        abrePeca(tabuleiro, i2, j2)

    imprimeStatus(tabuleiro, placar, nJogadores, vez)

    # Mensagem de jogador acertou ou não
    msg = recebeMensagem()
    if msg:
        msg = ("Pecas casam! Ponto para o jogador {0}.".format(vez + 1))
        print(msg)

        incrementaPlacar(placar, vez)
        paresEncontrados = paresEncontrados + 1
        removePeca(tabuleiro, i1, j1)
        removePeca(tabuleiro, i2, j2)

    else:
        msg = ("Pecas não casam!")
        print(msg)

        fechaPeca(tabuleiro, i1, j1)
        fechaPeca(tabuleiro, i2, j2)
        vez = (vez + 1) % nJogadores

    time.sleep(3)

# Verificar o vencedor e imprimir
pontuacaoMaxima = max(placar)
vencedores = []
for i in range(0, nJogadores):

    if placar[i] == pontuacaoMaxima:
        vencedores.append(i)

if len(vencedores) > 1:
    message = recebeMensagem()
    sys.stdout.write(message)

    for i in vencedores:
        message = recebeMensagem()
        sys.stdout.write(message)

    sys.stdout.write("\n")

else:
    message = recebeMensagem()
    sys.stdout.write(message)

sock.close()
