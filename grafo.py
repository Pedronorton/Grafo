class Vertice:
    def __init__(self,id):
        self.id = id
        self.pai = None
        self.tA = float('inf')
        self.tF = float('inf')
        self.cor = 'B'
