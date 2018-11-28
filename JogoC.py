import pickle
import socket
import os
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
sock.connect(server_address)

def recebeMensagem():
    data = sock.recv(4096)
    message = pickle.loads(data)
    time.sleep(0.1)
    return message

def handleError():
    err = recebeMensagem()
    print(err)

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

def novoPlacar(nJogadores):
    return [0] * nJogadores


def imprimePlacar(placar, nJogadores):
    print("Placar:")
    print("---------------------")
    for i in range(0, nJogadores):
        msg = recebeMensagem()
        print(msg)

def imprimeStatus(tabuleiro, placar, nJogadores, vez):
        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar, nJogadores)
        sys.stdout.write('\n')

        sys.stdout.write('\n')
        var = recebeMensagem()
        print(var)

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


def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

def incrementaPlacar(placar, jogador):
    message = recebeMensagem()
    placar[jogador] = message


def removePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = "-"
        return True


def fechaPeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Programa principal
limpaTela()
id = recebeMensagem()
print("Você é o jogador número " + str(id + 1))
nJogadores = recebeMensagem()

dim = recebeMensagem()

tabuleiro = novoTabuleiro(dim)

placar = novoPlacar(nJogadores)

totalDePares = dim**2 / 2
paresEncontrados = 0
vez = 0

while paresEncontrados < totalDePares:

    #imprimeStatus(tabuleiro, placar, nJogadores, vez)
    

    while True:
        imprimeStatus(tabuleiro, placar, nJogadores, vez)
        if (vez == id):
            coordenadas = leCoordenada(dim)

            if coordenadas == False:
                continue

            il, jl = coordenadas

            if abrePeca(tabuleiro, il, jl) == False:
                message = recebeMensagem()
                input(message)
                #input("Pressione <enter> para continuar...")
                continue

        break

    while True:
        imprimeStatus(tabuleiro, placar, nJogadores, vez)
        if (vez == id):
            coordenadas = leCoordenada(dim)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            if abrePeca(tabuleiro, i2, j2) == False:
                message = recebeMensagem()
                input(message)
                #print("Escolha uma peca ainda fechada!")
                #input("Pressione <enter> para continuar...")
                continue

        break

    i1 = recebeMensagem()
    print("imprime i1")
    print(i1)
    time.sleep(2)
    j1 = recebeMensagem()
    print("imprime j1")
    print(j1)
    time.sleep(2)
    i2 = recebeMensagem()
    print("imprime i2")
    print(i2)
    time.sleep(2)
    j2 = recebeMensagem()
    print("imprime j2")
    print(j2)
    time.sleep(2)

      # Mensagem mostrando pares escolhidos
    #1
    imprimeStatus(tabuleiro, placar, nJogadores, vez)
#2
    message = recebeMensagem()
    print(message)

#3
    # Mensagem Indicando se jogador acertou ou não
    msg = recebeMensagem()
    print(msg)

    # Atualiza placar e tabuleiro
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
    #print("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))

sock.close()
