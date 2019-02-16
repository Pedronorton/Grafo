from funcoes import*
import math


def floydWarshall(vertices,arestas,G):
    distancias = matrizDistancias(G,arestas,vertices)
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

    print(imprimeTodos(pais,vertices))
    return menorDistancia


def imprimeTodos(pais,vertices):
    for i in vertices:
        for j in vertices:
            global caminho
            caminho = []
            print('caminho de: ',i.id,' para: ',j.id,' é: ', imprimeCaminho(pais,i.id,j.id))


def imprimeCaminho(pais,v,u):#RETORNA O CAMINHO DE V PARA U
    caminho.append(v)
    if(pais[v][u] != v):
        imprimeCaminho(pais,pais[v][u],u)
    elif(v!=u):
        caminho.append(u)
    return caminho





