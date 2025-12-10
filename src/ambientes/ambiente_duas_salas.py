from .ambiente_base import AmbienteBase  # Assumindo que a AmbienteBase foi refatorada

class AmbienteDuasSalas(AmbienteBase):

    def __init__(self, sujeira_inicial={"A": True, "B": True}):
        super().__init__()
        # O estado interno é um dicionário que mapeia localização para estado (True = Sujo)
        self.estado_sujeira = sujeira_inicial.copy()

    def obter_percepcao(self, posicao):
        """
        Retorna (localização, dirty_here).
        """
        dirty_here = self.estado_sujeira.get(posicao, False)
        return (posicao, dirty_here)

    # Método para satisfazer AmbienteBase
    def executar_acao(self, agente, acao):
        """
        Executa a ação: 'Left', 'Right', ou 'Suck'.
        Retorna True se a ação resultou em uma mudança válida no ambiente/agente.
        """
        pos_atual = agente.posicao
        sucesso = False

        if acao == "Suck":
            if self.estado_sujeira[pos_atual]:
                self.estado_sujeira[pos_atual] = False  # Limpa a sala
                sucesso = True

        elif acao == "Right" and pos_atual == "A":
            agente.posicao = "B"
            sucesso = True

        elif acao == "Left" and pos_atual == "B":
            agente.posicao = "A"
            sucesso = True

        return sucesso, {"nova_posicao": agente.posicao}

    def estado_objetivo(self):
        """
        Retorna True se ambas as salas estiverem limpas (False).
        """
        return not any(self.estado_sujeira.values())

    def resetar(self, location='A', dirty_A=True, dirty_B=True):
        self.estado_sujeira['A'] = dirty_A
        self.estado_sujeira['B'] = dirty_B