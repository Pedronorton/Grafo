from grafo import*
import networkx as nx


def montarGrafo(arquivo):
    #FUNCAO RECEBE O NOME DO ARQUIVO COM AS ARESTAS E ADICIONA NÓS E ARESTAS, RETORNANDO O PRÓPRIO GRAFO
    G = nx.DiGraph()
    manipulador = open('entrada.txt', 'r')

    for linha in manipulador:
        linha = linha.rstrip()
        linha = linha.split()
        G.add_node(int(linha[0]))
        G.add_node(int(linha[1]))
        G.add_edge(int(linha[0]), int(linha[1]))
    return G


def montarListaArestas(G):
    #FUNCAO RECEBE O GRAFO E MONTA UMA LISTA COM AS ARESTAS
    listaArestas = []
    for i in G.edges:
        i = list(i)
        listaArestas.append(i)
    return listaArestas

def definirNos(G):
    #FUNCAO RECEBE O GRAFO E TRANSFORMA CADA INDICE DO NÓ E TRANSFORMA EM OBJETO
    listaVertice = []
    for i in G.nodes:
        vertice = Vertice(i)
        listaVertice.append(vertice)
    return listaVertice

def atualizaCor(lista,cor,v0):
    #RECEBE A LISTA DE VERTICES, COR A SER ATUALIZADA E O INDICE DO NÓ
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            v.cor = cor

def corVertice(v0,lista):
    for v in lista:
        if (v.id == v0):
            return v.cor

def atualizaTempo(v0,lista,flag,tempo):
    # RECEBE A LISTA DE VERTICES, TEMPO A SER ATUALIZADA, INDICE DO NÓ E FLAG ( TEMPO DE ABERTURA/FECHAMENTO)
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            if (flag == 'tA'):
                v.tA = tempo
            else:
                v.tF = tempo

def atualizaPai(v0,pai,lista):
    # RECEBE A LISTA DE VERTICES,PAI A SER SETADO E O INDICE DO NÓ FILHO
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            v.pai = pai

def zeraLista(vertices):
    #COMO PODE USAR TANTO A FUNCAO BFS QUANTO A DFS UTILIZANDO A MESMA LISTA
    #A FUNCAO TEM COMO O OBJETIVO DE REINICIA-LA
    for v in vertices:
        v.pai = None;
        v.Ta = float('inf')
        v.Tf = float('inf')
        v.cor = 'B'

def matrizAdjacencia(G):
    #RETORNA A MATRIZ DE ADJACENCIA DE G (UTILIZANDO UMA FUNCAO DA NETWORKX
    return nx.to_dict_of_lists(G)


def BFS(vertices, verticeInicial, G):
    #BFS - BUSCA EM LARGURA. FAZ A BUSCA ATE ONDE O VERTICE INICIAL ALCANÇA COM APENAS UMA ARESTA(LARGURA)
    #RECEBE O VERTICE INICIAL E COLOCA NA LISTA DE VISITADOS(RESULTADO FINAL)
    #E COLOCA NA LISTA AUXILIAR COMO CONTROLE DE FLUXO
    matriz = matrizAdjacencia(G)
    zeraLista(vertices)#CASO TENHA FEITO ALGUMA ALTERACAO NA LISTA DE VERTICES, ESSA FUNCAO A ZERA
    lista = [verticeInicial]
    visitados = [verticeInicial]
    atualizaCor(vertices, 'C', verticeInicial)
    tam = len(lista)
    while tam != 0:#ENQUANTO HOUVER VERTICES NA LISTA AUXILIAR TEM QUE PERCORRER
        v0 = lista[0]#PRIMEIRO ELEMENTO DA LISTA AUXILIAR, OU SEJA O PROXIMO VERTICE A SER VISITADO
        for i in matriz[v0]:#PERCORRE TODOS OS VERTICES ADJACENTES
            if corVertice(i,vertices) == 'B':#SE FOR COR BRANCA, OU SEJA NAO VISITADO ENTAO VISITO
                atualizaCor(vertices, 'C', i)#ALTERA A COR PARA CINZA
                lista.append(i)
                tam += 1
                visitados.append(i)
        atualizaCor(vertices, 'P', v0)#DEPOIS DE VISITAR TODOS OS ADJACENTES, COLORE-SE DE PRETO, OU SEJA NAO É NECESSARIO VOLTAR NESSE VERTICE MAIS
        lista.remove(v0)#REMOVE DA LISTA AUXILIAR E CONTINUA O CICLO
        tam -= 1
    return visitados

def DFS(vertices, verticeInicial, G):
    #DFS - BUSCA EM PROFUNDIDADE. RECEBE O GRAFO, LISTA DE VERTICES E VERTICE INICIAL
    #FAZ UMA BUSCA ATÉ O ULTIMO NÓ QUE O VERTICE INICIAL CONSEGUE ALCANÇAR (PROFUNDIDADE)
    zeraLista(vertices)#CASO TENHA FEITO ALGUMA ALTERACAO NA LISTA, BASTA ZERA-LA
    dfsLista = [verticeInicial]#ORDEM DA VISITACAO
    #SE QUER A LISTA COMPLETA DE VERTICES VISITADOS BASTA COLOCAR A LISTA DE VERTICES MESMO
    #CASO QUEIRA A LISTA DOS VERTICES QUE O VERTICE INICIAL ALCANÇA, SÓ POR O VERTICE INICIAL
    listaVisitacao = [verticeInicial]
    matriz = matrizAdjacencia(G)
    global tempo
    tempo = 0
    for v in listaVisitacao:
        if (corVertice(v, vertices) == 'B'):#SE FOR NAO VISITADO, CHAMA-SE A RECURSAO
            dfsVisit(v,matriz,dfsLista,vertices)
    return dfsLista

def dfsVisit(v, matriz, dfsLista, vertices):
    global tempo
    tempo += 1
    atualizaTempo(v, vertices, 'tA', tempo)
    atualizaCor(vertices, "C", v)#SETA A COR PARA CINZA (VISITADO)
    for u in matriz[v]:#PERCORRE OS ADJACENTES AO VERTICE
        if (corVertice(u, vertices) == 'B'):
            dfsLista.append(u)
            atualizaCor(vertices, 'C', u)
            dfsVisit(u, matriz, dfsLista, vertices)
    tempo += 1
    atualizaCor(vertices, 'P', v)#DEPOIS DE TER FEITO TODAS AS VISITAS, COLORE-SE DE PRETO
    atualizaTempo(v, vertices, 'tF', tempo)



