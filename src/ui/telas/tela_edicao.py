import pygame
import os
from ..config import *
from ..componentes import Botao

class TelaEdicao:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.modo = None # "simples" ou "objetivo"
        self.grid_size = (0, 0)
        self.celulas = {} # (x, y) -> tipo ("sujeira", "obstaculo", "vazio")
        self.ferramenta_atual = "sujeira" # "sujeira", "obstaculo"
        
        # Armazenar caminho dos assets
        base_path = os.path.dirname(__file__)
        self.assets_path = os.path.join(base_path, '..', 'assets')
        
        # Sprites serão carregados em configurar()
        self.sprite_parede = None
        self.sprite_sujeira = None
        
        # UI Elements
        self.btn_comecar = None
        self.btn_sujeira = None
        self.btn_parede = None
        
        self.offset_x = 0
        self.offset_y = 0
        self.fundo = get_background("background2.png")
    
    def _load_sprites(self, cell_size):
        """Carrega sprites com o tamanho de célula especificado"""
        def load_sprite_proportional(filename, full_cell=False, size_multiplier=1.0):
            try:
                img = pygame.image.load(os.path.join(self.assets_path, filename)).convert_alpha()
                img_width, img_height = img.get_size()
                
                if full_cell:
                    scale = max(cell_size / img_width, cell_size / img_height)
                else:
                    scale = min(cell_size / img_width, cell_size / img_height) * 0.8
                
                scale *= size_multiplier
                
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                scaled_img = pygame.transform.smoothscale(img, (new_width, new_height))
                surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                
                x_offset = (cell_size - new_width) // 2
                y_offset = (cell_size - new_height) // 2
                surface.blit(scaled_img, (x_offset, y_offset))
                
                return surface
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")
                fallback = pygame.Surface((cell_size, cell_size))
                fallback.fill(COR_PAREDE if full_cell else COR_SUJEIRA)
                return fallback


        # Sprites de obstáculos (paredes antigas comentadas)
        # self.sprite_obstaculo = load_sprite_proportional('parede.png', full_cell=True)  # Parede tijolin
        # self.sprite_obstaculo = load_sprite_proportional('paredenave.png', full_cell=True)  # Parede nave
        self.sprite_cadeira = load_sprite_proportional('spritecadeira.png', full_cell=True)
        self.sprite_mesa = load_sprite_proportional('spritemesa.png', full_cell=True)
        self.sprite_sujeira = load_sprite_proportional('poeira.png', size_multiplier=0.8)

    def configurar(self, modo):
        self.modo = modo
        if modo == "simples":
            self.grid_size = (2, 1) # 2 colunas, 1 linha
        else:
            self.grid_size = (7, 7)
            
        self.celulas = {} # Limpa grid
        self.proximo_obstaculo = "cadeira" # Alterna entre cadeira e mesa
        
        # Definir tamanho de célula baseado no modo
        self.tamanho_celula = 200 if modo == "simples" else TAMANHO_CELULA
        
        # Carregar sprites com tamanho correto
        self._load_sprites(self.tamanho_celula)
        
        # Centralizar Grid
        grid_largura = self.grid_size[0] * self.tamanho_celula
        grid_altura = self.grid_size[1] * self.tamanho_celula
        self.offset_x = (LARGURA_TELA - grid_largura) // 2 - 100 # Um pouco para a esquerda para caber menu lateral
        self.offset_y = (ALTURA_TELA - grid_altura) // 2
        
        # Botões
        self.btn_comecar = Botao(LARGURA_TELA - 180, ALTURA_TELA - 80, 150, 50, "Começar", acao=self.iniciar_jogo)
        
        self.btn_sujeira = Botao(LARGURA_TELA - 180, 100, 150, 50, "Sujeira", acao=lambda: self.selecionar_ferramenta("sujeira"))
        self.btn_obstaculo = Botao(LARGURA_TELA - 180, 170, 150, 50, "Obstáculo", acao=lambda: self.selecionar_ferramenta("obstaculo"))

    def selecionar_ferramenta(self, ferramenta):
        self.ferramenta_atual = ferramenta

    def iniciar_jogo(self):
        # Passa a configuração do grid para a tela de jogo
        config = {
            "modo": self.modo,
            "grid_size": self.grid_size,
            "celulas": self.celulas
        }
        self.gerenciador.mudar_estado(ESTADO_JOGO, config=config)

    def processar_eventos(self, eventos):
        for evento in eventos:
            self.btn_comecar.lidar_evento(evento)
            self.btn_sujeira.lidar_evento(evento)
            if self.modo == "objetivo":
                self.btn_obstaculo.lidar_evento(evento)
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clique esquerdo
                    mx, my = evento.pos
                    # Verificar clique no grid
                    col = (mx - self.offset_x) // self.tamanho_celula
                    lin = (my - self.offset_y) // self.tamanho_celula
                    
                    if 0 <= col < self.grid_size[0] and 0 <= lin < self.grid_size[1]:
                        key = (col, lin)
                        # Toggle ou set
                        if self.celulas.get(key) == self.ferramenta_atual:
                            del self.celulas[key] # Remove se já existe
                        elif self.ferramenta_atual == "obstaculo":
                            # Alternar entre cadeira e mesa
                            self.celulas[key] = self.proximo_obstaculo
                            self.proximo_obstaculo = "mesa" if self.proximo_obstaculo == "cadeira" else "cadeira"
                        else:
                            self.celulas[key] = self.ferramenta_atual

    def atualizar(self):
        pass

    def desenhar(self, superficie):
        superficie.blit(self.fundo, (0, 0))
        
        # Desenhar Grid
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(
                    self.offset_x + x * self.tamanho_celula,
                    self.offset_y + y * self.tamanho_celula,
                    self.tamanho_celula,
                    self.tamanho_celula
                )
                # Preencher célula com cor de fundo
                pygame.draw.rect(superficie, COR_CELULA, rect)
                # Desenhar borda da célula
                pygame.draw.rect(superficie, COR_GRID_LINHA, rect, 1)
                
                conteudo = self.celulas.get((x, y))
                if conteudo == "sujeira":
                    superficie.blit(self.sprite_sujeira, (rect.x, rect.y))
                elif conteudo == "cadeira":
                    superficie.blit(self.sprite_cadeira, (rect.x, rect.y))
                elif conteudo == "mesa":
                    superficie.blit(self.sprite_mesa, (rect.x, rect.y))
        
        # UI Lateral
        self.btn_comecar.desenhar(superficie)
        
        # Highlight ferramenta selecionada
        if self.ferramenta_atual == "sujeira":
            self.btn_sujeira.cor_base = CINZA_ESCURO
            self.btn_obstaculo.cor_base = COR_BOTAO
        else:
            self.btn_sujeira.cor_base = COR_BOTAO
            self.btn_obstaculo.cor_base = CINZA_ESCURO
            
        self.btn_sujeira.desenhar(superficie)
        if self.modo == "objetivo":
            self.btn_obstaculo.desenhar(superficie)
            
        # Instruções
        fonte = get_font(24)
        texto = fonte.render(f"Modo: {self.modo.capitalize()} - Clique no grid para editar", True, COR_TEXTO)
        superficie.blit(texto, (20, 20))
