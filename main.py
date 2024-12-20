import pygame
import sys
import random
import screeninfo 

from screeninfo import get_monitors

# Get information about all monitors
for monitor in get_monitors():
    print(f"Monitor: {monitor.name}, Width: {monitor.width}, Height: {monitor.height}, Position: ({monitor.x}, {monitor.y})")

# Inicialização do Pygame
pygame.init()
 
# Configurações da tela
WIDTH, HEIGHT = monitor.width, monitor.height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Egg Drop")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
# Relógio para controlar o FPS
clock = pygame.time.Clock()
FPS = 75
 
# Carregar imagens
chicken = pygame.image.load("galinha.png")
chicken = pygame.transform.scale(chicken, (70, 70))
egg = pygame.image.load("ovo.png")
egg = pygame.transform.scale(egg, (40, 50))
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pedra = pygame.image.load("pedra.png")
pedra = pygame.transform.scale(pedra, (100, 100))
 
# Variáveis do jogo
chicken_x = WIDTH // 2 - 25
chicken_y = HEIGHT // 2
chicken_velocity = 0
chicken_speed = 5  # Aumenta a velocidade lateral
chicken_flipped = False  # Variável para controlar se a galinha está invertida
 
eggs = []
egg_speed = 5
 
pedras = []
pedra_speed = 2
pedra_spawn_rate = 1000  # Tempo inicial entre o aparecimento das pedras (em milissegundos)
 
game_over = False
start_time = pygame.time.get_ticks()
last_pedra_spawn = pygame.time.get_ticks()
 
# Variáveis para controle de movimento contínuo
keys_pressed = {}
 
# Função para exibir texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    
 
# Loop principal do jogo

while True:
    # Desenhar o fundo
    screen.blit(background, (0, 0))
 
    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        # Capturar eventos de teclado
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
 
        # Soltar ovo e mover galinha para cima com mouse ou espaço
        if (event.type == pygame.MOUSEBUTTONDOWN or keys_pressed.get(pygame.K_SPACE) and not game_over):
            chicken_velocity = -8
            eggs.append([chicken_x + 15, chicken_y + 40])
 
    if not game_over:
        # Atualizar posição da galinha
        chicken_velocity += 0.5  # Gravidade
        chicken_y += chicken_velocity
 
        # Movimento contínuo para os lados
        if keys_pressed.get(pygame.K_LEFT) or keys_pressed.get(pygame.K_a):
            chicken_x -= chicken_speed
            if not chicken_flipped:
                chicken = pygame.transform.flip(chicken, True, False)  # Inverter horizontalmente
                chicken_flipped = True
        if keys_pressed.get(pygame.K_RIGHT) or keys_pressed.get(pygame.K_d):
            chicken_x += chicken_speed
            if chicken_flipped:
                chicken = pygame.transform.flip(chicken, True, False)  # Inverter horizontalmente
                chicken_flipped = False
 
        # Limitar movimento da galinha para cima e baixo
        if chicken_y < 0:
            chicken_y = 0
            chicken_velocity = 0  # Impede que a galinha "salte" para fora da tela
        # Verifica se a galinha chegou ao fim da tela embaixo
        if chicken_y > HEIGHT - chicken.get_height():
            game_over = True
 
        # Atualizar ovos
        for egg_pos in eggs:
            egg_pos[1] += egg_speed
 
        # Gerar pedras aleatoriamente
        elapsed_time = pygame.time.get_ticks()
        if elapsed_time - last_pedra_spawn > pedra_spawn_rate:
            pedras.append([random.randint(0, WIDTH - pedra.get_width()), 0])
            last_pedra_spawn = elapsed_time
 
        # Atualizar posição das pedras
        for pedra_pos in pedras:
            pedra_pos[1] += pedra_speed
 
        # Remover pedras que saíram da tela
        pedras = [pedra for pedra in pedras if pedra[1] < HEIGHT]
 
        # Verificar colisão com pedras
        for pedra_pos in pedras:
            if chicken_x < pedra_pos[0] + pedra.get_width() and chicken_x + chicken.get_width() > pedra_pos[0] and chicken_y < pedra_pos[1] + pedra.get_height() and chicken_y + chicken.get_height() > pedra_pos[1]:
                game_over = True
 
        # Desenhar ovos
        for egg_pos in eggs:
            screen.blit(egg, (egg_pos[0], egg_pos[1]))
 
        # Desenhar pedras
        for pedra_pos in pedras:
            screen.blit(pedra, pedra_pos)
 
        # Desenhar galinha
        screen.blit(chicken, (chicken_x, chicken_y))
 
        # Limitar movimento da galinha para os lados
        if chicken_x < 0:
            chicken_x = 0
        if chicken_x > WIDTH - chicken.get_width():
            chicken_x = WIDTH - chicken.get_width()
 
        # Calcular pontuação
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        draw_text(f"Score: {elapsed_time}", 30, BLACK, 10, 10)
 
    else:
        # Tela de game over
        draw_text("Game Over", 50, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Click para recomeçar", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)
 
        # Reiniciar o jogo ao clicar ou pressionar espaço
        if event.type == pygame.MOUSEBUTTONDOWN or keys_pressed.get(pygame.K_SPACE):
            chicken_x = WIDTH // 2 - 25
            chicken_y = HEIGHT // 2
            chicken_velocity = 0
            eggs.clear()
            pedras.clear()
            game_over = False
            start_time = pygame.time.get_ticks()
            pedra_speed = 2
            pedra_spawn_rate = 1000
 
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Egg Drop")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Relógio para controlar o FPS
clock = pygame.time.Clock()
FPS = 75

# Carregar imagens
chicken = pygame.image.load("galinha.png")
chicken = pygame.transform.scale(chicken, (70, 70))
egg = pygame.image.load("ovo.png")
egg = pygame.transform.scale(egg, (40, 50))
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pedra = pygame.image.load("pedra.png")
pedra = pygame.transform.scale(pedra, (100, 100))

# Variáveis do jogo
chicken_x = WIDTH // 2 - 25
chicken_y = HEIGHT // 2
chicken_velocity = 0
chicken_speed = 5  # Aumenta a velocidade lateral
chicken_flipped = False  # Variável para controlar se a galinha está invertida

eggs = []
egg_speed = 5

pedras = []
pedra_speed = 2
pedra_spawn_rate = 1000  # Tempo inicial entre o aparecimento das pedras (em milissegundos)

game_over = False
start_time = pygame.time.get_ticks()
last_pedra_spawn = pygame.time.get_ticks()

# Variáveis para controle de movimento contínuo
keys_pressed = {}

# Função para exibir texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Loop principal do jogo
while True:
    # Desenhar o fundo
    screen.blit(background, (0, 0))

    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Capturar eventos de teclado
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False

        # Soltar ovo e mover galinha para cima com mouse ou espaço
        if (event.type == pygame.MOUSEBUTTONDOWN or keys_pressed.get(pygame.K_SPACE) and not game_over):
            chicken_velocity = -8
            eggs.append([chicken_x + 15, chicken_y + 40])

    if not game_over:
        # Atualizar posição da galinha
        chicken_velocity += 0.5  # Gravidade
        chicken_y += chicken_velocity

        # Movimento contínuo para os lados
        if keys_pressed.get(pygame.K_LEFT) or keys_pressed.get(pygame.K_a):
            chicken_x -= chicken_speed
            if not chicken_flipped:
                chicken = pygame.transform.flip(chicken, True, False)  # Inverter horizontalmente
                chicken_flipped = True
        if keys_pressed.get(pygame.K_RIGHT) or keys_pressed.get(pygame.K_d):
            chicken_x += chicken_speed
            if chicken_flipped:
                chicken = pygame.transform.flip(chicken, True, False)  # Inverter horizontalmente
                chicken_flipped = False

        # Limitar movimento da galinha para cima e baixo
        if chicken_y < 0:
            chicken_y = 0
            chicken_velocity = 0  # Impede que a galinha "salte" para fora da tela
        # Verifica se a galinha chegou ao fim da tela embaixo
        if chicken_y > HEIGHT - chicken.get_height():
            game_over = True

        # Atualizar ovos
        for egg_pos in eggs:
            egg_pos[1] += egg_speed

        # Gerar pedras aleatoriamente
        elapsed_time = pygame.time.get_ticks()
        if elapsed_time - last_pedra_spawn > pedra_spawn_rate:
            pedras.append([random.randint(0, WIDTH - pedra.get_width()), 0])
            last_pedra_spawn = elapsed_time

        # Atualizar posição das pedras
        for pedra_pos in pedras:
            pedra_pos[1] += pedra_speed

        # Remover pedras que saíram da tela
        pedras = [pedra for pedra in pedras if pedra[1] < HEIGHT]

        # Verificar colisão com pedras
        for pedra_pos in pedras:
            if chicken_x < pedra_pos[0] + pedra.get_width() and chicken_x + chicken.get_width() > pedra_pos[0] and chicken_y < pedra_pos[1] + pedra.get_height() and chicken_y + chicken.get_height() > pedra_pos[1]:
                game_over = True

        # Desenhar ovos
        for egg_pos in eggs:
            screen.blit(egg, (egg_pos[0], egg_pos[1]))

        # Desenhar pedras
        for pedra_pos in pedras:
            screen.blit(pedra, pedra_pos)

        # Desenhar galinha
        screen.blit(chicken, (chicken_x, chicken_y))

        # Limitar movimento da galinha para os lados
        if chicken_x < 0:
            chicken_x = 0
        if chicken_x > WIDTH - chicken.get_width():
            chicken_x = WIDTH - chicken.get_width()

        # Calcular pontuação
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        draw_text(f"Score: {elapsed_time}", 30, BLACK, 10, 10)

    else:
        # Tela de game over
        draw_text("Game Over", 50, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Click para recomeçar", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)

        # Reiniciar o jogo ao clicar ou pressionar espaço
        if event.type == pygame.MOUSEBUTTONDOWN or keys_pressed.get(pygame.K_SPACE):
            chicken_x = WIDTH // 2 - 25
            chicken_y = HEIGHT // 2
            chicken_velocity = 0
            eggs.clear()
            pedras.clear()
            game_over = False
            start_time = pygame.time.get_ticks()
            pedra_speed = 2
            pedra_spawn_rate = 1000

    # Atualizar a tela
    pygame.displaycd
