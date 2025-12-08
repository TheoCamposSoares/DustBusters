from ..base_agent import AgenteBase
from .planejador_aestrela import PlanejadorAEstrela
from .heuristica import HeuristicaManhattan

class AgenteBaseadoObjetivo(AgenteBase):

    def __init__(self, max_passos=200, func_desempenho=None):
        super().__init__(max_passos, func_desempenho)
        self.objetivo = "limpar_tudo"
        self.planejador = PlanejadorAEstrela()
        self.caminho_atual = []  # sequência de coordenadas
        self.destino_atual = None

    def decidir_acao(self, percepcao):

        #Se a posição atual está suja: limpar
        if percepcao["estado_atual"] == "sujo":
            self.caminho_atual = []  # interrompe movimento
            return "LIMPAR"

        # Se existe sujeira visível mas não existe um caminho
        sujeiras = percepcao.get("sujeiras_visiveis", [])

        if sujeiras and not self.caminho_atual:
            # Seleciona a sujeira mais próxima usando a heurística Manhattan
            self.destino_atual = min(
                sujeiras, 
                key=lambda s: HeuristicaManhattan.calcular(self.posicao, s)
            )
            
            self.caminho_atual = self.planejador.buscar(
                ambiente=self.ambiente,
                inicio=self.posicao,
                objetivo=self.destino_atual
            )

        # Se existe um caminho planejado: seguir ele
        if self.caminho_atual:
            proximo = self.caminho_atual.pop(0)
            return self._converter_movimento(proximo)

        # Se não há sujeiras: explorar
        return self._explorar(percepcao)

    def _converter_movimento(self, destino):
        x, y = self.posicao
        dx, dy = destino

        if dx > x: return "DIREITA"
        if dx < x: return "ESQUERDA"
        if dy > y: return "BAIXO"
        if dy < y: return "CIMA"

        return None

    def _explorar(self, percepcao):
        for direcao, livre in percepcao["posicoes_vizinhas"].items():
            if livre:
                return direcao
        return None
