from ..ambientes.ambiente_duas_salas import AmbienteDuasSalas
from ..ambientes.grid import AmbienteGrid7x7
from ..agentes.simples.agente_simples import SimpleReflexAgent
from ..agentes.objetivo.agente_objetivo import AgenteBaseadoObjetivo

class SimulationEngine:
    def __init__(self, config):
        self.modo = config["modo"]
        self.grid_size = config["grid_size"]
        self.passos = 0
        self.finalizado = False
        
        self.ambiente = None
        self.agente = None
        
        self._inicializar_simulacao(config["celulas"])

    def _inicializar_simulacao(self, celulas):
        if self.modo == "simples":
            # Converter celulas (x,y) para formato do ambiente duas salas ("A", "B")
            sujeira_inicial = {"A": False, "B": False}
            if celulas.get((0, 0)) == "sujeira": sujeira_inicial["A"] = True
            if celulas.get((1, 0)) == "sujeira": sujeira_inicial["B"] = True
            
            self.ambiente = AmbienteDuasSalas(sujeira_inicial)
            self.agente = SimpleReflexAgent()
            self.agente.vincular_ambiente(self.ambiente, "A") # Começa sempre em A
            
        else:
            # Modo Objetivo (Grid 7x7)
            sujeiras = set()
            obstaculos = set()
            
            for (x, y), tipo in celulas.items():
                if tipo == "sujeira":
                    sujeiras.add((x, y))
                elif tipo in ["parede", "cadeira", "mesa"]:  # Aceita paredes antigas e novos obstáculos
                    obstaculos.add((x, y))
            
            self.ambiente = AmbienteGrid7x7(
                largura=self.grid_size[0], 
                altura=self.grid_size[1], 
                sujeiras=sujeiras, 
                obstaculos=obstaculos
            )
            
            self.agente = AgenteBaseadoObjetivo()
            start_pos = (0, 0) # Padrão
            
            # Verificar se start_pos não é parede
            if start_pos in obstaculos:
                 # Procura primeira livre
                 found = False
                 for x in range(self.grid_size[0]):
                     for y in range(self.grid_size[1]):
                         if (x,y) not in obstaculos:
                             start_pos = (x, y)
                             found = True
                             break
                     if found: break
            
            self.agente.vincular_ambiente(self.ambiente, start_pos)

    def executar_passo(self):
        if self.finalizado:
            return

        percepcao = self.agente.perceber()
        acao = self.agente.decidir_acao(percepcao)
        
        if acao is None: # Agente parou/terminou
            self.finalizado = True
        else:
            self.agente.agir(acao)
            self.passos = self.agente.passos
            
            # Verificar se objetivo foi alcançado (ambiente limpo)
            if self.ambiente.estado_objetivo():
                self.finalizado = True
            
            # Verificar limite de passos
            if self.passos >= self.agente.max_passos:
                self.finalizado = True
