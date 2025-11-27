import pygame
from ..config import *
from ..componentes import Botao

class TelaFim:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.passos_finais = 0
        
        centro_x = LARGURA_TELA // 2
        centro_y = ALTURA_TELA // 2
        
        self.btn_jogar_novamente = Botao(
            centro_x - 150, 
            centro_y + 50, 
            300, 
            50, 
            "Jogar Novamente",
            acao=lambda: self.gerenciador.mudar_estado(ESTADO_MENU)
        )
        
        self.btn_sair = Botao(
            centro_x - 150, 
            centro_y + 120, 
            300, 
            50, 
            "Sair",
            acao=lambda: self.gerenciador.sair()
        )
        
        self.fonte_grande = get_font(64)

    def configurar(self, passos):
        self.passos_finais = passos

    def processar_eventos(self, eventos):
        for evento in eventos:
            self.btn_jogar_novamente.lidar_evento(evento)
            self.btn_sair.lidar_evento(evento)

    def atualizar(self):
        pass

    def desenhar(self, superficie):
        superficie.fill(COR_FUNDO)
        
        texto_fim = self.fonte_grande.render("Simulação Finalizada!", True, COR_TEXTO)
        rect_fim = texto_fim.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 100))
        superficie.blit(texto_fim, rect_fim)
        
        texto_passos = self.fonte_grande.render(f"Total de Passos: {self.passos_finais}", True, COR_AGENTE)
        rect_passos = texto_passos.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40))
        superficie.blit(texto_passos, rect_passos)
        
        self.btn_jogar_novamente.desenhar(superficie)
        self.btn_sair.desenhar(superficie)
