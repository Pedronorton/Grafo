from funcoes import*
import math


def floydWarshall(vertices,arestas,G):
    distancias = matrizDistancias(G,arestas,vertices)
    global menorDistancia
    menorDistancia = distancias
    pais = matrizPais(G,arestas,vertices)

    for k in vertices:#INTERMEDIARIO
        for i in vertices:#VERTICE DE SAIDA
            for j in vertices:#VERTICE DE CHEGADA
                #NECESSARIO FAZER A VERIFICAÇÃO PARA QUE NAO TENHA ERRO NO DICIONARIO
                if(j.id in distancias[i.id]):#J ADJACENTE A I
                    d = float(distancias[i.id][j.id])#DISTANCIA I -> J
                else:#NAO DA PRA SAIR DE I E CHEGAR EM J DE MANEIRA DIRETA
                    d = math.inf

                if(k.id in distancias[i.id]):#K ADJACENTE A I
                    d1 = float(distancias[i.id][k.id])#DISTANCIA DE I -> K
                else:#NAO DA PRA SAIR DE I E CHEGAR EM K DE MANEIRA DIRETA
                    d1 = math.inf

                if(j.id in distancias[k.id]):#J ADJACENTE A K
                    d2 = float(distancias[k.id][j.id])#DISTANCIA DE K -> J
                else:#NAO DA PRA SAIR DE K E CHEGAR EM J DE MANEIRA DIRETA
                    d2 = math.inf
                if(i.id != j.id):#PARA NAO ACHAR DISTANCIA DO VERTICE 'V' PARA O VERTICE 'V'
                    #SE TIRAR ESSE IF É CAPAZ DE ACHAR CICLO NO GRAFO, SAIR DE V E CHEGAR EM V, CASO A DISTANCIA NAO SEJA INF
                    if(d > d1+d2):
                        menorDistancia[i.id][j.id] = d1+d2
                        pais[i.id][j.id] = pais[k.id][j.id]

                else:#CASO I == J, ENTAO A DISTANCIA É ZERO E O PAI DE I É ELE PROPRIO
                    menorDistancia[i.id][j.id] = 0
                    pais[i.id][j.id] = i.id

    print(imprimeTodos(pais,menorDistancia,vertices))
    return menorDistancia


def imprimeTodos(pais,menorDistancia, vertices):
    #FAZ TODOS OS CAMINHOS DE V->U
    for v in vertices:
        for u in vertices:
            global caminho
            caminho = []
            print('Distancia de ',v.id,' até ',u.id,' é: ',menorDistancia[v.id][u.id],' com caminho: ',imprimeCaminho(pais,v.id,u.id))


def imprimeCaminho(pais,v,u):#RETORNA O CAMINHO DE V PARA U
    if(pais[v][u] != None):#CASO HOUVER UM NONE NA MATRIZ PAI, QUER DIZER QUE NAO POSSUI CAMINHO
        caminho.append(u)
        if(pais[v][u] != v):
            imprimeCaminho(pais,v,pais[v][u])
        elif(v!=u):#CASO V!=U ENTAO BASTA COLOCAR O VERTICE INICIAL E INVERTEER A LISTA
            caminho.append(v)
            caminho.reverse()
    return caminho
