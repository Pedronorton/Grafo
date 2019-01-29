from grafo import*
from funcoes import*
import networkx as nx
import matplotlib.pyplot as plt

def main():
    arquivo  = 'entrada.txt'
    Graph = montarGrafo(arquivo)
    lista = montarListaArestas(Graph)
    vertices = definirNos(Graph)
    print(BFS(vertices, 2, Graph))
    print(DFS(vertices, 2, Graph ))
    for i in vertices:
        print('id = ', i.id, ' tempo Abertura = ', i.tA, 'tempo Fechamento = ', i.tF)

main()