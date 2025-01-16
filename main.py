import pygame
import sys
import random
from screeninfo import get_monitors
import pygame.mixer

for monitor in get_monitors():
    print(f"Monitor: {monitor.name}, Width: {monitor.width}, Height: {monitor.height}, Position: ({monitor.x}, {monitor.y})")

# Inicialização do Pygame
pygame.mixer.init()
pygame.init()

# Carregar som da flecha
arrow_sound = pygame.mixer.Sound("arrow_sound.mp3")

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
FPS = 60

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
hawk = pygame.transform.scale(hawk, (80, 80))
magma = pygame.image.load("magma.gif")
magma = pygame.transform.scale(magma, (100, 100))
arrow = pygame.image.load("arrow.png")  # Add arrow image
arrow = pygame.transform.scale(arrow, (40, 20)) 
arrow = pygame.transform.rotate(arrow, (50))  
if arrow is None:
    print("Error: Arrow image not loaded!")
play_button = pygame.image.load("play_button.png")
play_button = pygame.transform.scale(play_button, (300, 30))  # Adjust size as needed
quit_button = pygame.image.load("quit_button.png")
quit_button = pygame.transform.scale(quit_button, (150, 31))  # Adjust size as needed
# Carregar imagem de fundo da tela inicial
menu_background = pygame.image.load("a.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
# Carregar imagem de carregamento
loading_image = pygame.image.load("carregamento.gif")
loading_image = pygame.transform.scale(loading_image, (WIDTH, HEIGHT))



# Carregar imagem de leitura
Reading_world = pygame.image.load("Reading_world.png")
Reading_world = pygame.transform.scale(Reading_world, (WIDTH, HEIGHT))

# Centralizar a imagem de leitura na tela
reading_world_rect = Reading_world.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Add background music
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(1)  # Adjust this value between 0.0 and 1.0
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Could not load or play background music")

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
game_state = "menu"  # Can be "menu", "reading", or "playing"

# Variável para controlar o tempo de exibição da imagem de leitura
reading_start_time = None

# Função para exibir texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    
# Função para exibir o menu
def draw_menu():
    # Draw menu background
    screen.blit(menu_background, (0, 0))
    screen.blit(play_button, play_button_rect)
    screen.blit(quit_button, quit_button_rect)

# Variáveis do jogo
magmas = []  # Lista para armazenar magma blocks
magma_speed = 4  # Mais rápido que pedra_speed
magma_spawn_rate = 3000  # Menos frequente que pedra_spawn_rate
last_magma_spawn = pygame.time.get_ticks()
arrows = []  # Lista para armazenar flechas
arrow_speed = 12  # Increased for better visibility
last_arrow_time = pygame.time.get_ticks()
arrow_cooldown = 100

# Add with other game variables
play_button_rect = play_button.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
quit_button_rect = quit_button.get_rect(center=(WIDTH/2, HEIGHT/2 + 0))

# Add near the other game variables
rock_hit_score = 0  # New variable to track rocks hit

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
            if event.key == pygame.K_UP:  # Volume up
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, current_volume + 0.1))
            elif event.key == pygame.K_DOWN:  # Volume down
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, current_volume - 0.1))
            elif event.key == pygame.K_m:  # Mute/unmute
                if pygame.mixer.music.get_volume() > 0:
                    pygame.mixer.music.set_volume(0.0)
                else:
                    pygame.mixer.music.set_volume(0.5)
        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
        
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    game_state = "reading"
                    reading_start_time = pygame.time.get_ticks()
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN or (keys[pygame.K_SPACE] and not game_over):
                chicken_velocity = -8
                eggs.append([chicken_x + 15, chicken_y + 40])

    if game_state == "menu":
        draw_menu()
    
    elif game_state == "reading":
        screen.blit(Reading_world, (0, 0))
        if pygame.time.get_ticks() - reading_start_time > 10000:  # 10 segundos
            game_state = "playing"
            start_time = pygame.time.get_ticks()  # Reset the timer/score
    
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
            draw_text(f"Rocks Hit: {rock_hit_score}", 30, BLACK, 10, 40)  # Add rock hit score display
 
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

            # Atirar flecha quando pressionar Q
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_q] and current_time - last_arrow_time > arrow_cooldown and not game_over:
                arrow_dict = {
                    'x': chicken_x + (chicken.get_width() - arrow.get_width()) // 2,
                    'y': chicken_y,
                    'rect': pygame.Rect(chicken_x, chicken_y, arrow.get_width(), arrow.get_height())
                }
                arrows.append(arrow_dict)
                last_arrow_time = current_time
                arrow_sound.play()  # Play arrow sound

            # Update and draw arrows
            arrows_to_remove = []
            for arrow_dict in arrows:
                arrow_dict['y'] -= arrow_speed
                arrow_dict['rect'].x = arrow_dict['x']
                arrow_dict['rect'].y = arrow_dict['y']
                
                # Check collision with rocks
                for pedra_pos in pedras[:]:
                    pedra_rect = pygame.Rect(pedra_pos[0], pedra_pos[1], pedra.get_width(), pedra.get_height())
                    if arrow_dict['rect'].colliderect(pedra_rect):
                        # Remove both the arrow and the rock and increase score
                        if arrow_dict not in arrows_to_remove:
                            arrows_to_remove.append(arrow_dict)
                        if pedra_pos in pedras:
                            pedras.remove(pedra_pos)
                            rock_hit_score += 3  # Increase score by 3 when rock is hit
                        break
                
                # Check collision with magma
                for magma_pos in magmas[:]:
                    magma_rect = pygame.Rect(magma_pos[0], magma_pos[1], magma.get_width(), magma.get_height())
                    if arrow_dict['rect'].colliderect(magma_rect):
                        # Remove the arrow and decrease score
                        if arrow_dict not in arrows_to_remove:
                            arrows_to_remove.append(arrow_dict)
                        if magma_pos in magmas:
                            magmas.remove(magma_pos)
                            rock_hit_score = max(0, rock_hit_score - 4)  # Decrease score by 4, but don't go below 0
                        break

                if arrow_dict['y'] < -arrow.get_height():
                    arrows_to_remove.append(arrow_dict)
                else:
                    screen.blit(arrow, (arrow_dict['x'], arrow_dict['y']))

            # Remove used arrows
            for arrow_dict in arrows_to_remove:
                if arrow_dict in arrows:
                    arrows.remove(arrow_dict)

        else:
            game_state = "menu"
            game_over = False
            chicken_x = WIDTH // 2 - 25
            chicken_y = HEIGHT // 2
            chicken_velocity = 0
            eggs.clear()
            pedras.clear()
            magmas.clear()
            hawk_x = WIDTH
            hawk_active = False
            pedra_speed = 2
            pedra_spawn_rate = 1000
            rock_hit_score = 0  # Reset rock hit score
            start_time = pygame.time.get_ticks()  # Reset the timer/score

    pygame.display.flip()
    clock.tick(FPS)
