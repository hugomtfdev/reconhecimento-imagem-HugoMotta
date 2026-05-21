# Ponto de Entrada Principal (Main Loop)
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

def main():
    # Inicializa todos os módulos do Pygame
    pygame.init()
    
    # Configuração da janela do jogo
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Star Defender - Atari Style 2D")
    
    # Define o relógio para controle de FPS (taxa de atualização)
    clock = pygame.time.Clock()
    
    # Instancia a nossa máquina de estados e controle do jogo
    game = Game(screen)
    
    # Loop de execução principal do jogo
    running = True
    while running:
        # 1. Processamento de Entradas (Teclado, Janela)
        game.handle_events()
        
        # 2. Atualização dos Estados (Física, Movimento, Colisões)
        game.update()
        
        # 3. Renderização Visual (Desenho dos Elementos)
        game.draw()
        
        # 4. Atualização da Tela
        pygame.display.flip()
        
        # 5. Controle de Taxa de Frames (FPS = 60)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
