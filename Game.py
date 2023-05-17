import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
width = 800
height = 600

# Colores
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Crear la pantalla
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Square Collision")

clock = pygame.time.Clock()

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

        # Mantener al jugador dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebotar cuando alcanza los bordes de la pantalla
        if self.rect.left < 0 or self.rect.right > width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed_y *= -1

# Grupo de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Función para generar enemigos
def generate_enemies():
    for _ in range(4):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Generar enemigos iniciales
generate_enemies()

# Tiempo
current_time = pygame.time.get_ticks()
enemy_timer = 0

# Puntaje
score = 0
score_timer = 0

# Variable para controlar si el juego está en marcha
running = True

# Variable para controlar si el jugador ha perdido
game_over = False

# Variable para controlar si el jugador ha ganado
game_won = False

# Variable para controlar si se muestra la pantalla de fin de juego
show_end_screen = False

# Loop principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_won:
        # Actualizar sprites
        all_sprites.update()

        # Verificar colisiones entre el jugador y los enemigos
        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True
            show_end_screen = True

        # Generar nuevos enemigos cada 15 segundos
        elapsed_time = pygame.time.get_ticks() - current_time
        if elapsed_time > enemy_timer + 15000:
            generate_enemies()
            enemy_timer = elapsed_time

        # Aumentar el puntaje cada 15 segundos
        if pygame.time.get_ticks() - score_timer >= 15000:
            score += 50
            score_timer = pygame.time.get_ticks()

        # Verificar si el jugador ha ganado
        if score >= 200:
            game_won = True
            show_end_screen = True

        # Dibujar en la pantalla
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Mostrar puntaje en la pantalla
        font = pygame.font.Font(None, 24)
        score_text = font.render("Puntaje: " + str(score), True, BLUE)
        screen.blit(score_text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)
    else:
        if show_end_screen:
            # Pantalla de fin de juego
            screen.fill(WHITE)
            font = pygame.font.Font(None, 36)
            if game_over:
                text = font.render("Has perdido. ¿Qué deseas hacer?", True, RED)
            else:
                text = font.render("¡Has ganado! ¿Qué deseas hacer?", True, GREEN)
            text_rect = text.get_rect(center=(width / 2, height / 2 - 50))
            screen.blit(text, text_rect)

            button_repeat = pygame.Rect(width / 2 - 75, height / 2, 150, 50)
            pygame.draw.rect(screen, GREEN, button_repeat)
            font = pygame.font.Font(None, 24)
            text = font.render("Repetir Juego", True, WHITE)
            text_rect = text.get_rect(center=button_repeat.center)
            screen.blit(text, text_rect)

            button_quit = pygame.Rect(width / 2 - 75, height / 2 + 75, 150, 50)
            pygame.draw.rect(screen, RED, button_quit)
            font = pygame.font.Font(None, 24)
            text = font.render("Salir", True, WHITE)
            text_rect = text.get_rect(center=button_quit.center)
            screen.blit(text, text_rect)

            # Verificar si se hace clic en los botones
            mouse_pos = pygame.mouse.get_pos()
            if button_repeat.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    # Reiniciar el juego
                    all_sprites.empty()
                    enemies.empty()
                    player = Player()
                    all_sprites.add(player)
                    generate_enemies()
                    game_over = False
                    game_won = False
                    show_end_screen = False
                    current_time = pygame.time.get_ticks()
                    enemy_timer = 0
                    score = 0
                    score_timer = pygame.time.get_ticks()

            if button_quit.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    # Salir del juego
                    running = False

            # Actualizar la pantalla
            pygame.display.flip()

# Salir del juego
pygame.quit()
