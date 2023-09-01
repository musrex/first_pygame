import pygame, sys, os
from pygame.locals import *

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
PLAYER_SIZE = 50
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Playing with Pygame')
clock = pygame.time.Clock()

# musrex_file = os.path.join('images','avatar_small.png')
# musrex_surface = pygame.image.load(musrex_file)

# Setup the player and gravity
player_sprite = pygame.
player_pos = [WIDTH // 2, HEIGHT - GROUND_HEIGHT - PLAYER_SIZE]
player_vel = [0, 0]
gravity = 1
jump_strength = -15
jumping = False

# Player attributes
player_acceleration = 0.5
player_friction = 0.3
player_max_speed = 10
player_current_speed = 0

def move_player():
    global jumping, player_current_speed
    keys = pygame.key.get_pressed()

    acceleration = 0 # No acceleration by default

    if keys[pygame.K_a]: # move left
        acceleration = -player_acceleration
    if keys[pygame.K_d]: # move right
        acceleration = player_acceleration
    
    # Apply acceleration
    player_current_speed += acceleration

    # Apply friction
    if acceleration == 0: # Only apply when not accelarating
        player_current_speed += player_friction * (1 if player_current_speed < 0 else -1)

    # Clamp speed to max
    if abs(player_current_speed) > player_max_speed:
        player_current_speed = player_max_speed if player_current_speed > 0 else -player_max_speed 

    # Applying current speed to player pos
    player_pos[0] += player_current_speed

    if keys[K_SPACE] and not jumping:
        player_vel[1] += jump_strength
        jumping = True
    
    # Gravity
    player_vel[1] += gravity
    player_pos[1] += player_vel[1]

    # Ground
    if player_pos[1] > HEIGHT - GROUND_HEIGHT - PLAYER_SIZE:
        player_pos[1] = HEIGHT - GROUND_HEIGHT - PLAYER_SIZE
        player_vel[1] = 0
        jumping = False

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    move_player()

    # Draw ground and player
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, RED, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()