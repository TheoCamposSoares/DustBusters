import heapq
from .heuristica import HeuristicaManhattan

class PlanejadorAEstrela:

    def __init__(self):
        self.heuristica = HeuristicaManhattan()

    def reconstruir_caminho(self, origem, destino, pais):
        caminho = []
        atual = destino

        while atual != origem:
            caminho.append(atual)
            atual = pais[atual]

        caminho.reverse()
        return caminho

    def obter_vizinhos(self, ambiente, pos):
        return ambiente.obter_vizinhos(pos)

    def buscar(self, ambiente, inicio, objetivo):

        fila = []
        heapq.heappush(fila, (0, inicio))

        g = {inicio: 0}
        pais = {}

        visitados = set()

        while fila:
            _, atual = heapq.heappop(fila)

            if atual in visitados:
                continue
            visitados.add(atual)

            if atual == objetivo:
                return self.reconstruir_caminho(inicio, objetivo, pais)

            for _, vizinho in self.obter_vizinhos(ambiente, atual).items():

                custo_g = g[atual] + 1  # cada passo custa 1

                if vizinho not in g or custo_g < g[vizinho]:
                    g[vizinho] = custo_g
                    h = self.heuristica.calcular(vizinho, objetivo)
                    f = custo_g + h

                    pais[vizinho] = atual
                    heapq.heappush(fila, (f, vizinho))

        return None  # sem caminho
