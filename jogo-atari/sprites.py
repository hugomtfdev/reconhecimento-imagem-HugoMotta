# Classes e Entidades do Jogo (Sprites)
import pygame
import random
import math
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cria superfície transparente com dimensões baseadas no tamanho do jogador
        self.size = PLAYER_SIZE
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image_original = self.image.copy()
        
        # Desenha a nave espacial retrô com estilo vetorial ciano neon
        # Desenho de triângulo de nave de arcade com recorte na base
        self.points = [
            (self.size // 2, 0),                       # Bico superior
            (0, self.size - 5),                        # Asa esquerda inferior
            (self.size // 2, self.size - 12),          # Recorte interno central
            (self.size, self.size - 5)                 # Asa direita inferior
        ]
        
        # Preenchimento transparente azulado sutil
        pygame.draw.polygon(self.image, (0, 240, 255, 30), self.points)
        # Contorno neon brilhante
        pygame.draw.polygon(self.image, COLOR_PLAYER, self.points, 3)
        # Detalhe interno do motor (linha central)
        pygame.draw.line(self.image, COLOR_BULLET, (self.size // 2, self.size - 12), (self.size // 2, self.size - 6), 2)
        
        self.rect = self.image.get_rect()
        # Posiciona a nave no centro inferior da tela
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        
        self.speed = PLAYER_SPEED
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = PLAYER_COOLDOWN

    def update(self):
        # Captura as teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Movimentação para a esquerda
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Movimentação para a direita
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # Restringe a nave dentro das bordas laterais da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, bullet_group):
        # Verifica se passou tempo suficiente desde o último tiro (cooldown)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now
            # Cria e adiciona o projétil ao grupo
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            return True
        return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT), pygame.SRCALPHA)
        # Efeito de brilho do projétil neon magenta
        # Centro branco com contorno magenta brilhante
        self.image.fill(COLOR_BULLET)
        pygame.draw.rect(self.image, COLOR_WHITE, (1, 1, BULLET_WIDTH - 2, BULLET_HEIGHT - 2))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        # Move o projétil verticalmente para cima
        self.rect.y -= self.speed
        # Remove o projétil se ele sair do topo da tela
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, score=0):
        super().__init__()
        # Define tamanho aleatório
        self.radius = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.diameter = self.radius * 2
        
        # Cria superfície transparente
        self.image_original = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.image = self.image_original.copy()
        
        # Gera pontos de um polígono irregular para dar visual retrô de asteroide
        num_points = random.randint(8, 12)
        points = []
        center = self.radius
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Varia o raio ligeiramente para tornar o formato irregular
            r = self.radius * random.uniform(0.7, 1.0)
            px = center + r * math.cos(angle)
            py = center + r * math.sin(angle)
            points.append((px, py))
            
        # Desenha o asteroide (fundo sutil e borda neon laranja)
        pygame.draw.polygon(self.image_original, (255, 153, 0, 15), points)
        pygame.draw.polygon(self.image_original, COLOR_ASTEROID, points, 2)
        
        self.rect = self.image_original.get_rect()
        # Nasce no topo da tela com coordenada X aleatória
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.diameter)
        self.rect.bottom = 0
        
        # Lógica de dificuldade dinâmica: a velocidade sobe com a pontuação
        # A cada 150 pontos, a velocidade aumenta sutilmente
        difficulty = score / 150.0
        min_speed = ASTEROID_MIN_SPEED + difficulty * 0.25
        max_speed = ASTEROID_MAX_SPEED + difficulty * 0.35
        
        # Limita a velocidade máxima dos asteroides para manter o jogo sempre jogável
        min_speed = min(min_speed, 7.5)
        max_speed = min(max_speed, 11.0)
        
        # Velocidade e física aleatórias baseadas na dificuldade
        self.speed = random.uniform(min_speed, max_speed)
        
        # Configuração para efeito de rotação profissional
        self.angle = 0
        self.rot_speed = random.uniform(-3, 3) # Velocidade de rotação (graus por frame)

    def update(self):
        # Move para baixo
        self.rect.y += int(self.speed)
        
        # Aplica a rotação do asteroide
        self.angle = (self.angle + self.rot_speed) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect(center=old_center)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(2, 5)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Partículas variam entre amarelo brilhante, vermelho e laranja neon
        self.color = random.choice([COLOR_PARTICLE, COLOR_BULLET, COLOR_ASTEROID])
        self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Velocidade em X e Y simulando uma explosão radial
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
        # Tempo de vida aleatório em frames
        self.life = random.randint(PARTICLE_MIN_LIFE, PARTICLE_MAX_LIFE)
        self.max_life = self.life
        self.decay = PARTICLE_DECAY

    def update(self):
        # Movimentação física simples com desaceleração
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)
        self.vx *= self.decay
        self.vy *= self.decay
        
        # Reduz a vida da partícula
        self.life -= 1
        
        # Reduz opacidade conforme a partícula morre (fade out)
        alpha = int((self.life / self.max_life) * 255)
        self.image.set_alpha(alpha)
        
        # Se a vida acabar, remove a partícula
        if self.life <= 0:
            self.kill()
