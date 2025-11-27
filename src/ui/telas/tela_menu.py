import pygame
from ..config import *
from ..componentes import Botao

class TelaMenu:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        
        largura_btn = 500
        altura_btn = 60
        centro_x = LARGURA_TELA // 2
        centro_y = ALTURA_TELA // 2
        
        self.btn_simples = Botao(
            centro_x - largura_btn // 2, 
            centro_y, 
            largura_btn, 
            altura_btn, 
            "Jogar com Agente Simples (1x2)",
            acao=lambda: self.gerenciador.mudar_estado(ESTADO_EDICAO, modo="simples")
        )
        
        self.btn_objetivo = Botao(
            centro_x - largura_btn // 2, 
            centro_y + 80, 
            largura_btn, 
            altura_btn, 
            "Jogar com Agente Objetivo (7x7)",
            acao=lambda: self.gerenciador.mudar_estado(ESTADO_EDICAO, modo="objetivo")
        )
        
        self.fonte_titulo = get_font(64)

    def processar_eventos(self, eventos):
        for evento in eventos:
            self.btn_simples.lidar_evento(evento)
            self.btn_objetivo.lidar_evento(evento)

    def atualizar(self):
        pass

    def desenhar(self, superficie):
        superficie.fill(COR_FUNDO)
        
        # Título
        titulo_surf = self.fonte_titulo.render("DustBusters", True, COR_TEXTO)
        titulo_rect = titulo_surf.get_rect(center=(LARGURA_TELA // 2, 150))
        superficie.blit(titulo_surf, titulo_rect)
        
        self.btn_simples.desenhar(superficie)
        self.btn_objetivo.desenhar(superficie)
