import pygame

# Configurações de Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JANELA = "Aspirador Inteligente"
FPS = 60

# Cores (Placeholders para futura estilização)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
MARROM = (139, 69, 19) # Para sujeira

# Cores Específicas
COR_FUNDO = (47, 52, 71)  # #2f3447
COR_TEXTO = (248, 230, 232)  # #f8e6e8
COR_BOTAO = (148, 111, 145)  # #946f91
COR_BOTAO_HOVER = (96, 111, 128)  # #606f80
COR_GRID_LINHA = (73, 74, 75)  # #494a4b
COR_CELULA = (142, 147, 153)  # #8e9399
COR_AGENTE = AZUL
COR_SUJEIRA = MARROM
COR_PAREDE = PRETO

# Configurações do Grid
TAMANHO_CELULA = 60  # Tamanho em pixels de cada célula do grid
MARGEM_GRID = 20     # Margem ao redor do grid

# Estados do Jogo
ESTADO_MENU = "menu"
ESTADO_EDICAO = "edicao"
ESTADO_JOGO = "jogo"
ESTADO_FIM = "fim"

# Configurações de Fonte
import os
_current_dir = os.path.dirname(__file__)
_font_path = os.path.join(_current_dir, 'assets', 'Orbitron-Regular.ttf')

def get_font(size):
    """Retorna a fonte Orbitron no tamanho especificado"""
    try:
        return pygame.font.Font(_font_path, size)
    except:
        print(f"Erro ao carregar fonte Orbitron, usando fonte padrão")
        return pygame.font.SysFont(None, size)

