from .ambiente_base import AmbienteBase

class AmbienteGrid7x7(AmbienteBase):
    def __init__(self, largura=7, altura=7, sujeiras=None, obstaculos=None):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.sujeiras = set(sujeiras) if sujeiras else set()
        self.obstaculos = set(obstaculos) if obstaculos else set()

    # Registra o agente no ambiente
    def registrar_agente(self, agente, posicao_inicial):
        super().registrar_agente(agente, posicao_inicial)

    # Obtem a percepção enviada ao agente
    def obter_percepcao(self, pos):
        percepcao = {
            "estado_atual": "sujo" if pos in self.sujeiras else "limpo",

            "posicoes_vizinhas": self.obter_vizinhos(pos),

            "sujeiras_visiveis": list(self.sujeiras)
        }

        return percepcao

    # Executa a ação (limpar ou se mover)
    def executar_acao(self, agente, acao):
        pos_atual = agente.posicao

        # Ação de limpar
        if acao == "LIMPAR":
            if pos_atual in self.sujeiras:
                self.sujeiras.remove(pos_atual)
            return True, {"nova_posicao": agente.posicao}

        nova_pos = self.mover_posicao(pos_atual, acao)

        # Verifica se não há obstáculos ou se acabou o grid
        if self.sem_obstaculo(nova_pos):
            agente.posicao = nova_pos
            return True, {"nova_posicao": agente.posicao}

        return False, {"nova_posicao": agente.posicao}

    # Verifica se limpou todas as sujeiras do grid
    def estado_objetivo(self):
        return len(self.sujeiras) == 0

    # Retorna a nova posição a partir da direção dada
    def mover_posicao(self, pos, direcao):
        x, y = pos
        movimentos = {
            "CIMA": (x, y - 1),
            "BAIXO": (x, y + 1),
            "ESQUERDA": (x - 1, y),
            "DIREITA": (x + 1, y)
        }
        return movimentos[direcao]

    # Verifica se não há obstáculos e se está dentro dos limites do grid
    def sem_obstaculo(self, pos):
        return (
            self.dentro_limites(pos) and
            pos not in self.obstaculos
        )

    # Verifica se a posição dada está dentro dos limites do grid
    def dentro_limites(self, pos):
        x, y = pos
        return 0 <= x < self.largura and 0 <= y < self.altura

    # Retorna os vizinhos válidos
    def obter_vizinhos(self, pos):
        x, y = pos

        candidatos = {
            "CIMA":     (x, y - 1),
            "BAIXO":    (x, y + 1),
            "ESQUERDA": (x - 1, y),
            "DIREITA":  (x + 1, y)
        }

        # Filtrar vizinhos válidos
        return {
            direcao: p
            for direcao, p in candidatos.items()
            if self.sem_obstaculo(p)
        }