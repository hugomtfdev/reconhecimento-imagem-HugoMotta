# Configurações do Jogo Atari-Style 2D

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Paleta de Cores Neon (RGB)
BG_COLOR = (10, 10, 18)         # Azul-escuro profundo (espaço)
COLOR_PLAYER = (0, 240, 255)     # Ciano neon
COLOR_BULLET = (255, 0, 85)      # Magenta/Vermelho vibrante
COLOR_ASTEROID = (255, 153, 0)   # Laranja neon
COLOR_PARTICLE = (255, 220, 50)  # Ouro/Amarelo brilhante
COLOR_WHITE = (255, 255, 255)    # Branco puro
COLOR_GRAY = (150, 150, 150)     # Cinza para textos secundários
COLOR_DARK_RED = (180, 0, 50)    # Vermelho escuro para efeitos de dano/fim

# Parâmetros do Jogador (Nave)
PLAYER_SIZE = 45                 # Tamanho da base do triângulo da nave
PLAYER_SPEED = 7                 # Velocidade de movimento
PLAYER_COOLDOWN = 250            # Tempo mínimo entre tiros (milissegundos)

# Parâmetros dos Projéteis (Balas)
BULLET_SPEED = 10                # Velocidade de subida do projétil
BULLET_WIDTH = 4                 # Largura do projétil retangular
BULLET_HEIGHT = 15               # Altura do projétil retangular

# Parâmetros dos Asteroides
ASTEROID_SPAWN_RATE = 1600       # Tempo inicial entre surgimento de novos asteroides (milissegundos)
ASTEROID_MIN_SPEED = 1.0         # Velocidade mínima inicial de queda
ASTEROID_MAX_SPEED = 3.2         # Velocidade máxima inicial de queda
ASTEROID_MIN_SIZE = 25           # Diâmetro mínimo do asteroide
ASTEROID_MAX_SIZE = 55           # Diâmetro máximo do asteroide

# Parâmetros de Partículas (Explosões)
PARTICLE_COUNT = 15              # Número de partículas geradas por explosão
PARTICLE_MIN_SPEED = 1           # Velocidade mínima das partículas
PARTICLE_MAX_SPEED = 4           # Velocidade máxima das partículas
PARTICLE_DECAY = 0.95            # Fator de desaceleração das partículas
PARTICLE_MIN_LIFE = 20           # Vida mínima da partícula (frames)
PARTICLE_MAX_LIFE = 45           # Vida máxima da partícula (frames)
