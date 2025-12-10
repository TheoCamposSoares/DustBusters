from abc import ABC, abstractmethod

class AgenteBase(ABC):

    def __init__(self, max_passos=100, func_desempenho=None):
        self.max_passos = max_passos
        self.func_desempenho = func_desempenho
        self.passos = 0
        self.pontuacao = 0
        self.ambiente = None
        self.posicao = None


    # Vincula o agente ao ambiente e define posição inicial
    def vincular_ambiente(self, ambiente, posicao_inicial):
        self.ambiente = ambiente
        self.posicao = posicao_inicial

    # Retorna a percepção atual do ambiente
    def perceber(self):
        return self.ambiente.obter_percepcao(self.posicao)

    # Como agir no ambiente
    def agir(self, acao):
        self.passos += 1
        
        # Executa a ação
        sucesso, info_ambiente_pos_acao = self.ambiente.executar_acao(self, acao)
        
        # Atualiza a posição do agente
        nova_posicao = info_ambiente_pos_acao.get("nova_posicao")
        if sucesso and nova_posicao:
            self.posicao = nova_posicao

        # Atualiza o desempenho
        self._atualizar_desempenho(acao, sucesso, info_ambiente_pos_acao)

        return sucesso

    # Reseta a contagem de passos
    def resetar(self):
        self.passos = 0

    @abstractmethod
    # Decide a ação do agente baseado na percepcao
    def decidir_acao(self, percepcao):
        pass

    # Atualiza o desempenho aplicando a recompensa à pontuação
    def _atualizar_desempenho(self, acao, sucesso, info_ambiente_pos_acao):
        if self.func_desempenho is not None:
            recompensa = self.func_desempenho(self, acao, sucesso, info_ambiente_pos_acao)
            self.pontuacao += recompensa
