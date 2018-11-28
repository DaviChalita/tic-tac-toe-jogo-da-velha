import pickle
import socket
import os
import sys
import time
import random

# Funcoes
#envia mensagens somente para o jogador da vez
def enviaMensagemIndividual(msg, vez):
    message = pickle.dumps(msg)
    jogadores[vez].send(message)
    time.sleep(0.1)
    return msg

#envia mensagens para todos jogadores
def enviaMensagemTodos(msg, nJogadores):
    for i in range(0, nJogadores):
        enviaMensagemIndividual(msg, i)

#envia mensagens para todos menos o jogador da vez
def enviaMensagemTodosMenosJogadorVez(msg, nJogadores):
        for i in range(0, nJogadores):
            if(i != vez):
                enviaMensagemIndividual(msg, i)
#define as dimensoes do tabuleiro
def defineDimensao():
    dim = int(input("Especifique a dimensão: "))
    return dim
#define o numero de jogadores da partida
def defineNumeroJogadores():
    nJogadores = int(input("Especifique o numero de jogadores: "))
    return nJogadores
#limpa a tela
def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')
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
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))

        sys.stdout.write("\n")

# Cria um novo tabuleiro com pecas aleatorias.
# 'dim' eh a dimensao do tabuleiro, necessariamente
# par.
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
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            enviaMensagemTodos(indiceAleatorio, nJogadores)

            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            enviaMensagemTodos(indiceAleatorio, nJogadores)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

    return tabuleiro

# Abre (revela) peca na posicao (i, j). Se posicao ja esta
# aberta ou se ja foi removida, retorna False. Retorna True
# caso contrario.
def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Fecha peca na posicao (i, j). Se posicao ja esta
# fechada ou se ja foi removida, retorna False. Retorna True
# caso contrario.
def fechaPeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Remove peca na posicao (i, j). Se posicao ja esta
# removida, retorna False. Retorna True
# caso contrario.
def removePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = "-"
        return True
#mostra novo placar
def novoPlacar(nJogadores):
    return [0] * nJogadores
#incrementa valor do placar
def incrementaPlacar(placar, jogador):
    placar[jogador] = placar[jogador] + 1
    enviaMensagemTodos(placar[jogador], nJogadores)
#imprime o placar
def imprimePlacar(placar):
    nJogadores = len(placar)

    print("Placar: \n ---------------------")

    for i in range(0, nJogadores):
        print ("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

        data = ("Jogador {0}: {1:2d}".format(i + 1, placar[i]))
        enviaMensagemTodos(data, nJogadores)

# Imprime informacoes basicas sobre o estado atual da partida.
def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar)
        sys.stdout.write('\n')

        sys.stdout.write('\n')

        print ("Vez do Jogador {0}.\n".format(vez + 1))
        vezJogador = ("Vez do Jogador {0}.\n".format(vez + 1))
        enviaMensagemTodos(vezJogador, nJogadores)
#le as coordenadas recebidas do cliente
def leCoordenada(dim, vez):
    data = jogadores[vez].recv(4096)
    var = pickle.loads(data)
    try:
        i = int(var.split(' ')[0])
        j = int(var.split(' ')[1])

    except ValueError:
        erro = ("Coordenadas invalidas! Use o formato \"i j\" (sem aspas), \n")
        erro += ("onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}".format(dim))
        enviaMensagemIndividual(erro, vez)

    if i < 0 or i >= dim:
        erro = ("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim))
        enviaMensagemIndividual(erro, vez)

    if j < 0 or j >= dim:
        erro = ("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim))
        enviaMensagemIndividual(erro, vez)

    enviaMensagemIndividual(i, vez)
    enviaMensagemIndividual(j, vez)

    return (i, j)
#limpa a tela
def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Programa principal

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket à porta
server_address = ('localhost', 5000)
sock.bind(server_address)



# while True para quando jogo acabar esperar novas conexoes
while True:
    limpaTela()
    #define a qtd de jogadores
    nJogadores = defineNumeroJogadores()
    #vetor que guardará as conexoes
    jogadores = []

    for i in range(0, nJogadores):
        # Listen para conexões recebidas

        sock.listen(nJogadores)
        connection, client_address = sock.accept()
        #novas conexoes sao adicionadas ao vetor
        novoJogador = connection
        jogadores.append(novoJogador)
        #envia numero da sua vez para o cliente
        enviaMensagemIndividual(i, i)

    #define o tamanho do tabuleiro
    dim = defineDimensao()

    enviaMensagemTodos(nJogadores, nJogadores)
    enviaMensagemTodos(dim, nJogadores)

    # Numero total de pares de pecas
    totalDePares = dim**2 / 2

    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)

    # Cria um novo placar zerado
    placar = novoPlacar(nJogadores)

    # Partida continua enquanto ainda ha pares de pecas a
    #     # casar.
    paresEncontrados = 0
    vez = 0

    while paresEncontrados < totalDePares:

        imprimeStatus(tabuleiro, placar, vez)

        # Requisita primeira peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim, vez)
            if coordenadas == False:
                continue

            i1, j1 = coordenadas            

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                data = ("Escolha uma peca ainda fechada!")
                data += ("\n")
                data += ("Pressione <enter> para continuar...")
                enviaMensagemIndividual(data, vez)
                continue

            break

        # Requisita segunda peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.

            coordenadas = leCoordenada(dim, vez)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:
                data = ("Escolha uma peca ainda fechada!")
                data += ("\n")
                data += ("Pressione <enter> para continuar...")
                enviaMensagemIndividual(data, vez)
                continue
            break

        enviaMensagemTodosMenosJogadorVez(i1, nJogadores)
        enviaMensagemTodosMenosJogadorVez(j1, nJogadores)
        enviaMensagemTodosMenosJogadorVez(i2, nJogadores)
        enviaMensagemTodosMenosJogadorVez(j2, nJogadores)
        imprimeStatus(tabuleiro, placar, vez)

        # Pecas escolhidas sao iguais?

        msg = (tabuleiro[i1][j1] == tabuleiro[i2][j2])
        enviaMensagemTodos(msg, nJogadores)

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

    pontuacaoMaxima = max(placar)
    vencedores = []

    for i in range(0, nJogadores):
        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        msg = ("Houve empate entre os jogadores ")
        enviaMensagemTodos(msg, nJogadores)

        for i in vencedores:
            sys.stdout.write(str(i + 1) + ' ')
            data = (str(i + 1) + ' ')
            enviaMensagemTodos(msg, nJogadores)

        sys.stdout.write("\n")

    else:
        msg = ("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))
        print(msg)
        enviaMensagemTodos(msg, nJogadores)
        time.sleep(3)

    connection.close()
