import pygame
from .config import *

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_base=COR_BOTAO, cor_hover=COR_BOTAO_HOVER, cor_texto=COR_TEXTO, acao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.acao = acao
        self.fonte = get_font(24)
        self.hovered = False

    def desenhar(self, superficie):
        cor = self.cor_hover if self.hovered else self.cor_base
        pygame.draw.rect(superficie, cor, self.rect)
        pygame.draw.rect(superficie, PRETO, self.rect, 2) # Borda

        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)

    def lidar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(evento.pos)
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and evento.button == 1:
                if self.acao:
                    return self.acao()
        return None
