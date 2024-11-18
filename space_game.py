import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("window.png")  
pygame.display.set_icon(icon)

# Background Color
background_color = (0, 0, 0)

# Player
player_img = pygame.image.load("player.png")  
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = pygame.image.load("enemy.png")  
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_change = 4
enemy_y_change = 40

# Bullet
bullet_img = pygame.image.load("bullet.png")  
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"  # "ready" means bullet is not visible

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Game Loop
running = True
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement Key Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player Movement
    player_x += player_x_change
    player_x = max(0, min(player_x, 736))  # Keep player within screen bounds

    # Enemy Movement
    enemy_x += enemy_x_change
    if enemy_x <= 0 or enemy_x >= 736:
        enemy_x_change *= -1
        enemy_y += enemy_y_change

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Collision Detection
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score += 1
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)

    # Game Over Condition
    if enemy_y > 440:
        game_over()
        break

    # Display
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score()
    pygame.display.update()
