import pygame
import sys
import random
from screeninfo import get_monitors

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
BLUE = (0, 0, 255)
 
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
hawk = pygame.image.load("hawk.png")
hawk = pygame.transform.scale(hawk, (120, 80))
magma = pygame.image.load("magma.gif")
magma = pygame.transform.scale(magma, (80, 80))
arrow = pygame.image.load("arrow.png")  # Add arrow image
arrow = pygame.transform.scale(arrow, (40, 20))  # Adjust size as needed
play_button = pygame.image.load("play_button.png")
play_button = pygame.transform.scale(play_button, (200, 80))  # Adjust size as needed
quit_button = pygame.image.load("quit_button.png")
quit_button = pygame.transform.scale(quit_button, (200, 80))  # Adjust size as needed

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
 
hawk_active = False
hawk_x = WIDTH
hawk_y = random.randint(50, HEIGHT - 150)
hawk_speed = 7
hawk_timer = pygame.time.get_ticks()
hawk_interval = 30000  # 30 segundos em milissegundos
hawk_duration = 10000  # 10 segundos em milissegundos
 
game_over = False
start_time = pygame.time.get_ticks()
last_pedra_spawn = pygame.time.get_ticks()
 
# Variáveis para controle de movimento contínuo
keys_pressed = {}
 
# Variável para controlar o estado do jogo
game_state = "menu"  # Can be "menu" or "playing"
 
# Função para exibir texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    
# Função para exibir o menu
def draw_menu():
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw title
    draw_text("Chicken Egg Drop", 64, BLACK, WIDTH // 2 - 200, HEIGHT // 3)
    
    # Draw start button
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
    draw_text("Start Game", 36, WHITE, WIDTH // 2 - 70, HEIGHT // 2 + 10)
    
    # Draw instructions
    draw_text("Use arrows or A/D to move", 30, BLACK, WIDTH // 2 - 150, HEIGHT * 2 // 3)
    draw_text("Click or Space to jump and drop eggs", 30, BLACK, WIDTH // 2 - 200, HEIGHT * 2 // 3 + 40)
 
# Variáveis do jogo
magmas = []  # Lista para armazenar magma blocks
magma_speed = 4  # Mais rápido que pedra_speed
magma_spawn_rate = 3000  # Menos frequente que pedra_spawn_rate
last_magma_spawn = pygame.time.get_ticks()
arrows = []  # Lista para armazenar flechas
arrow_speed = 7  # Velocidade da flecha
last_arrow_time = 0  # Controlar o tempo entre tiros
arrow_cooldown = 500  # Tempo mínimo entre tiros (em milliseconds)

# Add with other game variables
play_button_rect = play_button.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
quit_button_rect = quit_button.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))

# Loop principal do jogo
while True:
    # Handle events first
    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
        
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    game_state = "playing"
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False
        
        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN or (keys[pygame.K_SPACE] and not game_over):
                chicken_velocity = -8
                eggs.append([chicken_x + 15, chicken_y + 40])

    if game_state == "menu":
        screen.blit(background, (0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(quit_button, quit_button_rect)
    
    elif game_state == "playing":
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
            if event.type == pygame.MOUSEBUTTONDOWN or (keys[pygame.K_SPACE] and not game_over):
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
 
            # Gerenciar falcão
            if hawk_active:
                hawk_x -= hawk_speed
                if pygame.time.get_ticks() - hawk_timer > hawk_duration:
                    hawk_active = False
                    hawk_x = WIDTH
            else:
                if pygame.time.get_ticks() - hawk_timer > hawk_interval:
                    hawk_active = True
                    hawk_timer = pygame.time.get_ticks()
                    hawk_y = random.randint(50, HEIGHT - 150)

            # Verificar colisão com falcão
            if hawk_active and chicken_x < hawk_x + hawk.get_width() and chicken_x + chicken.get_width() > hawk_x and chicken_y < hawk_y + hawk.get_height() and chicken_y + chicken.get_height() > hawk_y:
                game_over = True

            # Desenhar falcão
            if hawk_active:
                screen.blit(hawk, (hawk_x, hawk_y))

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
 
            # Gerar magma blocks aleatoriamente
            elapsed_time = pygame.time.get_ticks()
            if elapsed_time - last_magma_spawn > magma_spawn_rate:
                magmas.append([random.randint(0, WIDTH - magma.get_width()), 0])
                last_magma_spawn = elapsed_time

            # Atualizar posição dos magma blocks
            for magma_pos in magmas:
                magma_pos[1] += magma_speed

            # Remover magma blocks que saíram da tela
            magmas = [m for m in magmas if m[1] < HEIGHT]

            # Verificar colisão com magma blocks
            for magma_pos in magmas:
                if (chicken_x < magma_pos[0] + magma.get_width() and 
                    chicken_x + chicken.get_width() > magma_pos[0] and 
                    chicken_y < magma_pos[1] + magma.get_height() and 
                    chicken_y + chicken.get_height() > magma_pos[1]):
                    game_over = True

            # Desenhar magma blocks
            for magma_pos in magmas:
                screen.blit(magma, magma_pos)

            # Atirar flecha quando pressionar SPACE
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - last_arrow_time > arrow_cooldown and not game_over:
                arrows.append([chicken_x + chicken.get_width(), chicken_y + chicken.get_height()/2])
                last_arrow_time = current_time

            # Atualizar posição das flechas
            for arrow_pos in arrows:
                arrow_pos[0] += arrow_speed

            # Remover flechas que saíram da tela
            arrows = [a for a in arrows if a[0] < WIDTH]

            # Desenhar flechas
            for arrow_pos in arrows:
                screen.blit(arrow, arrow_pos)

            # Reset section: add this line
            arrows.clear()  # Clear arrows when resetting

        else:
            # Tela de game over
            draw_text("Game Over", 50, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
            draw_text("Click para recomeçar", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)
 
            # Reiniciar o jogo ao clicar ou pressionar espaço
            if event.type == pygame.MOUSEBUTTONDOWN or keys[pygame.K_SPACE]:
                game_state = "menu"
                game_over = False
                chicken_x = WIDTH // 2 - 25
                chicken_y = HEIGHT // 2
                chicken_velocity = 0
                eggs.clear()
                pedras.clear()
                magmas.clear()  # Clear magma blocks
                hawk_x = WIDTH
                hawk_active = False
                pedra_speed = 2
                pedra_spawn_rate = 1000

    pygame.display.flip()
    clock.tick(FPS)
