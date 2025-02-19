import pygame
import assets
import random
from player import Player

# Initialize pygame
pygame.init()

# Screen settings (convert to integers)
WIDTH, HEIGHT = int(1920 / 5 * 4), int(1080 / 5 * 4)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution - Player Controller")

# Create player at the center of the screen
player = Player(WIDTH // 2, HEIGHT // 2)

# Load an image for the food item
food_image = assets.loadImage(assets.assets["Food"])

# List to hold food objects
foods = []

# Create food object at a random location within the world bounds
def spawnFood():
    x = random.randint(0, WIDTH - 50)  # Food size subtracted to prevent overflow
    y = random.randint(0, HEIGHT - 50)
    food_rect = pygame.Rect(x, y, 50, 50)  # Food size
    foods.append(food_rect)

# Check for collision between player and food
def checkFoodCollision():
    global foods
    for food_rect in foods[:]:
        if player.rect.colliderect(food_rect):  # If player collides with food
            foods.remove(food_rect)  # Remove the food from the list
            break  # Only remove one food at a time

# Spawn initial food
spawnFood()

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((10, 11, 45))  # Clear screen

    # Center the player on the screen
    player.center(WIDTH, HEIGHT)

    # Spawn food randomly
    if random.random() < 0.08:  # Adjust the spawn rate here (8% chance each frame)
        spawnFood()

    # Check for food collision
    checkFoodCollision()

    # Draw all food items
    for food_rect in foods:
        screen.blit(food_image, food_rect)

    # Update player
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    player.update(keys, mouse_pos)
    player.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
