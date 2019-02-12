from grafo import*
import networkx as nx
import random

def montarGrafo(arquivo):
    #FUNCAO RECEBE O NOME DO ARQUIVO COM AS ARESTAS E ADICIONA NÓS E ARESTAS, RETORNANDO O PRÓPRIO GRAFO
    G = nx.DiGraph()
    manipulador = open(arquivo, 'r')
    global quantidadeVertice
    quantidadeVertice = int(manipulador.read(1))
    manipulador.readline()
    for linha in manipulador:
        x = random.randint(0,10000000000)
        y = random.randint(0,10000000000)
        x1 = random.randint(0,10000000000)
        y1 = random.randint(0,10000000000)
        linha = linha.rstrip()
        linha = linha.split()
        G.add_node(int(linha[0]),pos = (x,y))
        G.add_node(int(linha[1]),pos = (x1,y1))
        G.add_edge(int(linha[0]), int(linha[1]), weight = linha[2])
    return G


def montarListaArestas(G):
    #FUNCAO RECEBE O GRAFO E MONTA UMA LISTA COM AS ARESTAS
    listaArestas = []
    for i in G.edges:
        x = G.get_edge_data(i[0],i[1])#PEGA O PESO DA ARESTA (V,U)
        i = list(i)
        aresta = Aresta(i,x['weight'])
        listaArestas.append(aresta)
    return listaArestas

def definirNos(G):
    #FUNCAO RECEBE O GRAFO E TRANSFORMA CADA INDICE DO NÓ E TRANSFORMA EM OBJETO
    listaVertice = []
    for i in G.nodes:
        vertice = Vertice(i)
        listaVertice.append(vertice)
    return listaVertice


def definirTipoAresta(listaArestas, arestas, corFilho):
    for a in listaArestas:
        if(arestas[0] == a.aresta[0] and arestas[1] == a.aresta[1]):
            if (corFilho == 'B'):
                a.tipo = 'arvore'
            elif(corFilho == 'C'):
                a.tipo = 'direta'
            elif(corFilho == 'P'):
                a.tipo = 'retorno'
            else:
                a.tipo = 'cruzada'

def matrizDistancias(G,arestas):#CRIA UM DICIONARIO DE DICIONARIOS COM O PESO DAS ARESTAS
    matriz = matrizAdjacencia(G)
    distancias = {}
    for i in range(quantidadeVertice):
        adj = {}
        for j in matriz[i]:
            x = pesoAresta(i,j,arestas)
            adj[j] = x
        distancias[i] = adj
    return distancias


def pesoAresta(v,u,arestas):
    for i in arestas:
        if (i.aresta[0] == v and i.aresta[1] == u):
            return i.peso
            break




def atualizaCor(lista,cor,v0):
    #RECEBE A LISTA DE VERTICES, COR A SER ATUALIZADA E O INDICE DO NÓ
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            v.cor = cor
            break

def corVertice(v0,lista):
    for v in lista:
        if (v.id == v0):
            return v.cor

def atualizaTempo(v0,lista,flag,tempo):
    # RECEBE A LISTA DE VERTICES, TEMPO A SER ATUALIZADA, INDICE DO NÓ E FLAG ( TEMPO DE ABERTURA/FECHAMENTO)
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            if (flag == 'abertura'):
                v.abertura = tempo
            else:
                v.fechamento = tempo

def atualizaPai(v0,pai,lista):
    # RECEBE A LISTA DE VERTICES,PAI A SER SETADO E O INDICE DO NÓ FILHO
    #  FAZ UMA BUSCA NA LISTA DE VERTICES E ALTERA
    for v in lista:
        if (v.id == v0):
            v.pai = pai
            break

def zeraLista(vertices):
    #COMO PODE USAR TANTO A FUNCAO BFS QUANTO A DFS UTILIZANDO A MESMA LISTA
    #A FUNCAO TEM COMO O OBJETIVO DE REINICIA-LA
    for v in vertices:
        v.pai = None;
        v.abertura = float('inf')
        v.fechamento = float('inf')
        v.cor = 'B'

def matrizAdjacencia(G):
    #RETORNA A MATRIZ DE ADJACENCIA DE G (UTILIZANDO UMA FUNCAO DA NETWORKX
    return nx.to_dict_of_lists(G)


def BFS(vertices,arestas, verticeInicial, G):
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
        for v in matriz[v0]:#PERCORRE TODOS OS VERTICES ADJACENTES A 'v0'
            aresta = [v0,v]
            if corVertice(v,vertices) == 'B':#SE FOR COR BRANCA, OU SEJA NAO VISITADO ENTAO VISITO
                lista.append(v)
                tam += 1
                visitados.append(v)
            #PARTE QUE VERIFICA QUAL O TIPO DA ARESTA (ARVORE, CRUZADA, DIRETA, RETORNO)
            definirTipoAresta(arestas,aresta,corVertice(v,vertices))
            atualizaCor(vertices, 'C', v)  # ALTERA A COR PARA CINZA
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
    atualizaTempo(v, vertices, 'abertura', tempo)
    atualizaCor(vertices, "C", v)#SETA A COR PARA CINZA (VISITADO)
    for u in matriz[v]:#PERCORRE OS ADJACENTES AO VERTICE
        if (corVertice(u, vertices) == 'B'):
            dfsLista.append(u)
            atualizaCor(vertices, 'C', u)
            dfsVisit(u, matriz, dfsLista, vertices)
    tempo += 1
    atualizaCor(vertices, 'P', v)#DEPOIS DE TER FEITO TODAS AS VISITAS, COLORE-SE DE PRETO
    atualizaTempo(v, vertices, 'fechamento', tempo)
