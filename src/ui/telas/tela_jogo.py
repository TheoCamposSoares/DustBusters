import pygame
import os
from ..config import *
from ..componentes import Botao
from ...simulacao.engine import SimulationEngine

class TelaJogo:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.engine = None
        self.timer_passo = 0
        self.DELAY_PASSO = 200 # ms
        
        self.offset_x = 0
        self.offset_y = 0
        
        # Armazenar caminho dos assets
        base_path = os.path.dirname(__file__)
        self.assets_path = os.path.join(base_path, '..', 'assets')
        
        # Sprites serão carregados em configurar()
        self.sprite_objetivo = None
        self.sprite_simples = None
        self.sprite_parede = None
        self.sprite_sujeira = None

        # Estado de Animação
        self.pos_visual = (0, 0) # (x, y) em coordenadas do grid (floats)
        self.target_pos = (0, 0)
        self.animating = False
        self.animation_speed = 0.05 # Células por frame (ajustar para suavidade)

    def _get_grid_coords(self, pos_logica):
        """Converte posição lógica (A/B ou x,y) para coordenadas x,y do grid"""
        if self.engine.modo == "simples":
            return (0, 0) if pos_logica == "A" else (1, 0)
        return pos_logica
    
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
                fallback.fill(COR_PAREDE if full_cell else COR_AGENTE)
                return fallback
        
        self.sprite_objetivo = load_sprite_proportional('eve_nanobanana.png', size_multiplier=2.4)
        self.sprite_simples = load_sprite_proportional('walle_triste.png', size_multiplier=1.5)
        self.sprite_parede = load_sprite_proportional('parede.png', full_cell=True)
        self.sprite_sujeira = load_sprite_proportional('poeira.png', size_multiplier=0.8)

    def configurar(self, config):
        self.engine = SimulationEngine(config)
        
        # Definir tamanho de célula baseado no modo
        self.tamanho_celula = 200 if self.engine.modo == "simples" else TAMANHO_CELULA
        
        # Carregar sprites com tamanho correto
        self._load_sprites(self.tamanho_celula)
        
        # Configurar velocidades baseadas no modo
        if self.engine.modo == "simples":
            self.DELAY_PASSO = 400  # Mais lento (ms entre ações)
            self.animation_speed = 0.01  # Deslize moderado
        else:
            self.DELAY_PASSO = 150  # Mais rápido
            self.animation_speed = 0.05  # Deslize mais rápido
        
        # Recalcular offsets para centralizar
        grid_largura = self.engine.grid_size[0] * self.tamanho_celula
        grid_altura = self.engine.grid_size[1] * self.tamanho_celula
        self.offset_x = (LARGURA_TELA - grid_largura) // 2
        self.offset_y = (ALTURA_TELA - grid_altura) // 2
        
        # Inicializar posição visual
        start_coords = self._get_grid_coords(self.engine.agente.posicao)
        self.pos_visual = list(start_coords)
        self.target_pos = list(start_coords)
        self.animating = False
        
        self.timer_passo = pygame.time.get_ticks()

    def processar_eventos(self, eventos):
        pass # Usuário apenas assiste

    def atualizar(self):
        # Lógica de Animação
        if self.animating:
            dx = self.target_pos[0] - self.pos_visual[0]
            dy = self.target_pos[1] - self.pos_visual[1]
            
            dist = (dx**2 + dy**2)**0.5
            
            if dist < self.animation_speed:
                self.pos_visual = list(self.target_pos)
                self.animating = False
            else:
                self.pos_visual[0] += (dx / dist) * self.animation_speed
                self.pos_visual[1] += (dy / dist) * self.animation_speed
            return # Não executa lógica do jogo enquanto anima

        # Lógica do Jogo (só roda se não estiver animando)
        if self.engine.finalizado:
            # Pequeno delay visual antes de mudar de tela
            pygame.time.wait(500)
            self.gerenciador.mudar_estado(ESTADO_FIM, passos=self.engine.passos)
            return

        agora = pygame.time.get_ticks()
        if agora - self.timer_passo > self.DELAY_PASSO:
            self.timer_passo = agora
            
            # Guardar posição antiga
            old_pos = self.engine.agente.posicao
            
            self.engine.executar_passo()
            
            # Verificar se moveu
            new_pos = self.engine.agente.posicao
            if new_pos != old_pos:
                self.target_pos = self._get_grid_coords(new_pos)
                self.animating = True

    def desenhar(self, superficie):
        superficie.fill(COR_FUNDO)
        
        # Desenhar Grid e Itens Estáticos
        for x in range(self.engine.grid_size[0]):
            for y in range(self.engine.grid_size[1]):
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
                
                is_dirty = False
                is_wall = False
                
                if self.engine.modo == "simples":
                    loc = "A" if x == 0 else "B"
                    is_dirty = self.engine.ambiente.estado_sujeira[loc]
                else:
                    is_dirty = (x, y) in self.engine.ambiente.sujeiras
                    is_wall = (x, y) in self.engine.ambiente.obstaculos

                if is_dirty:
                    # Desenhar sujeira centralizada
                    superficie.blit(self.sprite_sujeira, (rect.x, rect.y))
                if is_wall:
                    # Desenhar parede preenchendo célula
                    superficie.blit(self.sprite_parede, (rect.x, rect.y))

        # Desenhar Agente (com posição visual interpolada)
        pixel_x = self.offset_x + self.pos_visual[0] * self.tamanho_celula
        pixel_y = self.offset_y + self.pos_visual[1] * self.tamanho_celula
        
        sprite = self.sprite_simples if self.engine.modo == "simples" else self.sprite_objetivo
        superficie.blit(sprite, (pixel_x, pixel_y))

        # HUD
        fonte = get_font(36)
        texto_passos = fonte.render(f"Passos: {self.engine.passos}", True, COR_TEXTO)
        superficie.blit(texto_passos, (20, 20))
