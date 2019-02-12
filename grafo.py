class Grafo:
    def __init__(self):
        self.qtdVertices = None
        self.qtdArestas = None
        self.listaArestas = None
        self.listaVertices = None

class Vertice:
    def __init__(self,id):
        self.id = id
        self.pai = None
        self.abertura = float('inf')
        self.fechamento = float('inf')
        self.cor = 'B'

class Aresta:
    def __init__(self, aresta,peso):
        self.tipo = None
        self.aresta = aresta
        self.peso = peso
