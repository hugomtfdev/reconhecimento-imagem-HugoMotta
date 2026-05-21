# Lógica de Controle e Interface do Jogo (Game Engine)
import pygame
import random
import sys
import math
from config import *
from sprites import Player, Bullet, Asteroid, Particle

class Game:
    def __init__(self, screen):
        self.screen = screen
        
        # Inicializa fontes clássicas
        self.font_score = pygame.font.SysFont("Consolas", 28, bold=True)
        self.font_gameover = pygame.font.SysFont("Consolas", 64, bold=True)
        self.font_restart = pygame.font.SysFont("Consolas", 24, bold=True)
        
        # Cria um starfield estático/dinâmico de fundo para aumentar a imersão
        self.stars = []
        for _ in range(60):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.2, 1.2),
                'brightness': random.randint(100, 255)
            })
            
        # Inicializa os elementos do jogo
        self.reset()

    def reset(self):
        # Grupos de sprites do Pygame
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        
        # Cria o jogador
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Estado do jogo
        self.score = 0
        self.game_over = False
        self.last_spawn = pygame.time.get_ticks()
        
    def handle_events(self):
        # Loop de eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.key == pygame.K_r:
                    self.reset()
                    
        # Disparo contínuo com base nas teclas pressionadas (enquanto pressionar Barra de Espaço)
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.shoot(self.bullets)

    def create_explosion(self, x, y):
        # Spawna partículas de explosão retrô
        for _ in range(PARTICLE_COUNT):
            particle = Particle(x, y)
            self.particles.add(particle)
            self.all_sprites.add(particle)

    def update(self):
        # Sempre atualiza as partículas de fundo, mesmo no Game Over
        if self.game_over:
            self.particles.update()
            return
            
        # Atualização do Starfield (estrelas descendo sutilmente)
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
                
        # Spawna novos asteroides conforme a taxa de spawn dinâmica
        now = pygame.time.get_ticks()
        # Lógica de dificuldade dinâmica: o intervalo de spawn diminui com a pontuação
        # A cada 100 pontos, reduz o intervalo de spawn em 80ms, com um limite mínimo de 450ms
        current_spawn_rate = max(450, ASTEROID_SPAWN_RATE - int(self.score / 100) * 80)
        
        if now - self.last_spawn > current_spawn_rate:
            self.last_spawn = now
            asteroid = Asteroid(self.score)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
            
        # Atualiza todos os sprites do jogo
        self.all_sprites.update()
        
        # 1. Verifica colisões: Projéteis vs Asteroides
        # groupcollide(group1, group2, dokill1, dokill2) -> retorna dicionário de colisões
        hits = pygame.sprite.groupcollide(self.bullets, self.asteroids, True, True)
        for bullet, hit_asteroids in hits.items():
            for asteroid in hit_asteroids:
                # Incrementa placar proporcional ao tamanho (asteroides menores dão mais pontos!)
                points = int((ASTEROID_MAX_SIZE - asteroid.radius) + 10)
                self.score += points
                # Cria a explosão de partículas
                self.create_explosion(asteroid.rect.centerx, asteroid.rect.centery)
                
        # 2. Verifica colisão: Asteroides vs Jogador
        player_hit = pygame.sprite.spritecollide(self.player, self.asteroids, False)
        if player_hit:
            self.game_over = True
            # Cria super explosão no jogador
            self.create_explosion(self.player.rect.centerx, self.player.rect.centery)
            
        # 3. Verifica se algum asteroide passou direto da tela (toca o fundo)
        for asteroid in self.asteroids:
            if asteroid.rect.top > SCREEN_HEIGHT:
                self.game_over = True
                # Cria uma explosão onde o asteroide bateu
                self.create_explosion(asteroid.rect.centerx, SCREEN_HEIGHT - 5)

    def draw(self):
        # Limpa a tela com a cor de fundo profunda
        self.screen.fill(BG_COLOR)
        
        # Desenha as estrelas ao fundo (com intensidades de brilho diferentes)
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            # Estrelas menores e maiores com base na velocidade delas
            size = 1 if star['speed'] < 0.7 else 2
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), size)
            
        # Desenha todos os sprites na tela (exceto o jogador se estiver Game Over, para simular destruição)
        for sprite in self.all_sprites:
            if isinstance(sprite, Player) and self.game_over:
                continue
            self.screen.blit(sprite.image, sprite.rect)
            
        # Desenha o HUD de Pontuação (Score) no canto superior esquerdo com brilho retrô
        # Formata placar com zeros à esquerda (ex: 000520)
        score_text = self.font_score.render(f"SCORE: {self.score:06d}", True, COLOR_WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Se for Game Over, renderiza a tela vermelha e os comandos de reinício
        if self.game_over:
            # Desenha um overlay de cor avermelhada escura e semi-transparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((40, 10, 20, 150)) # Vermelho profundo com 150 de opacidade
            self.screen.blit(overlay, (0, 0))
            
            # Texto principal de Game Over
            text_go = self.font_gameover.render("GAME OVER", True, COLOR_BULLET)
            rect_go = text_go.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            
            # Desenha um brilho sutil (glow) atrás do texto de Game Over
            glow_surface = self.font_gameover.render("GAME OVER", True, COLOR_DARK_RED)
            self.screen.blit(glow_surface, rect_go.move(2, 2))
            self.screen.blit(text_go, rect_go)
            
            # Texto mostrando pontuação final
            text_final = self.font_score.render(f"FINAL SCORE: {self.score}", True, COLOR_WHITE)
            rect_final = text_final.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(text_final, rect_final)
            
            # Texto de reinício pulsante (efeito neon senoidal)
            # Frequência de pulsação baseada no tempo do Pygame
            pulse = int(120 + 135 * math.sin(pygame.time.get_ticks() * 0.007))
            pulse = max(0, min(255, pulse)) # Mantém entre 0 e 255
            color_pulse = (0, pulse, pulse) # Ciano pulsando
            
            text_restart = self.font_restart.render("PRESS 'R' TO RESTART", True, color_pulse)
            rect_restart = text_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(text_restart, rect_restart)
