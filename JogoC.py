import pickle
import socket
import os
import sys
import time
# Create a TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

server_address = ('localhost', 10000)
sock.connect(server_address)

message = sock.recv(4096)
var = pickle.loads(message)
dim = var

time.sleep(1)

# Numero de jogadores
message = sock.recv(4096)
var = pickle.loads(message)
nJogadores = var

# Numero total de pares de pecas
totalDePares = dim**2 / 2

def novoTabuleiro(dim):
    # Cria um tabuleiro vazio.
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
            data = sock.recv(4096)
            indiceAleatorio = pickle.loads(data)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            data = sock.recv(4096)
            indiceAleatorio = pickle.loads(data)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i
    return tabuleiro

    # Imprime o placar atual.

def novoPlacar(nJogadores):

    return [0] * nJogadores

# Imprime informacoes basicas sobre o estado atual da partida.
def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar)
        sys.stdout.write('\n')

        sys.stdout.write('\n')
        data = sock.recv(4096)
        var = pickle.loads(data)
        print(var)

def imprimeTabuleiro(tabuleiro):
    # Limpa a tela
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

def imprimePlacar(placar):
    nJogadores = len(placar)

    print("Placar:")

    print("---------------------")
    for i in range(0, nJogadores):
        data = sock.recv(4096)
        var = pickle.loads(data)
        print(var)



def leCoordenada(dim):

    var = input("Especifique uma peca: ")
    message = pickle.dumps(var)
    sock.send(message)

    try:
        #\/ rever
        i = int(var.split(' ')[0])
        j = int(var.split(' ')[1])
    except ValueError:
        data = sock.recv(4096)
        var = pickle.loads(data)
        print(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        input(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        return var

    if i < 0 or i >= dim:
        data = sock.recv(4096)
        var = pickle.loads(data)
        print(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        input(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        return var

    if j < 0 or j >= dim:
        data = sock.recv(4096)
        var = pickle.loads(data)
        print(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        input(var)

        data = sock.recv(4096)
        var = pickle.loads(data)
        return var

    #\/talvez essa parte seja desnecessaria
    datai = sock.recv(4096)
    i = pickle.loads(datai)

    dataj = sock.recv(4096)
    j = pickle.loads(dataj)
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

limpaTela()

tabuleiro = novoTabuleiro(dim)

placar = novoPlacar(nJogadores)
paresEncontrados = 0
vez = 0


def incrementaPlacar(placar, jogador):

    data = sock.recv(4096)
    message = pickle.loads(data)
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


while paresEncontrados < totalDePares:
    while True:
        imprimeStatus(tabuleiro, placar, vez)

        #global coordenadas
        coordenadas = leCoordenada(dim)
        if coordenadas == False:
            continue

        il, jl = coordenadas

        if abrePeca(tabuleiro, il, jl) == False:
            data = sock.recv(4096)
            message = pickle.loads(data)
            input(message)
            #input("Pressione <enter> para continuar...")
            continue

        break

    while True:

        imprimeStatus(tabuleiro, placar, vez)

        coordenadas = leCoordenada(dim)
        if coordenadas == False:
            continue

        i2, j2 = coordenadas

        if abrePeca(tabuleiro, i2, j2) == False:
            data = sock.recv(4096)
            message = pickle.loads(data)
            input(message)
            #print("Escolha uma peca ainda fechada!")
            #input("Pressione <enter> para continuar...")
            continue

        break

    imprimeStatus(tabuleiro, placar, vez)

    data = sock.recv(4096)
    message = pickle.loads(data)
    print(message)

    if tabuleiro[il][jl] == tabuleiro[i2][j2]:

        #print("Pecas casam! Ponto para o jogador {0}.".format(vez + 1))
        data = sock.recv(4096)
        message = pickle.loads(data)
        print(message)
        time.sleep(3)
        incrementaPlacar(placar, vez)
        paresEncontrados = paresEncontrados + 1
        removePeca(tabuleiro, il, jl)
        removePeca(tabuleiro, i2, j2)

        time.sleep(5)
    else:

        print("Pecas nao casam!")

        time.sleep(3)

        fechaPeca(tabuleiro, il, jl)
        fechaPeca(tabuleiro, i2, j2)
        vez = (vez + 1) % nJogadores

# Verificar o vencedor e imprimir
pontuacaoMaxima = max(placar)
vencedores = []
for i in range(0, nJogadores):

    if placar[i] == pontuacaoMaxima:
        vencedores.append(i)

if len(vencedores) > 1:

    data = sock.recv(4096)
    message = pickle.loads(data)
    sys.stdout.write(message)

    for i in vencedores:
        data = sock.recv(4096)
        message = pickle.loads(data)
        sys.stdout.write(data)

    sys.stdout.write("\n")

else:
    data = sock.recv(4096)
    message = pickle.loads(data)
    sys.stdout.write(data)
    #print("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))

sock.close()