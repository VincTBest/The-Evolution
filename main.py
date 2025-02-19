import pygame
import assets
import random
from player import Player
from camera import Camera

scene = "menu"

# Initialize pygame
pygame.init()

# Screen settings (convert to integers)
WIDTH, HEIGHT = int(1920 / 5 * 4), int(1080 / 5 * 4)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Evolution")

# Create camera
camera = Camera(WIDTH, HEIGHT)

# Create player at the center of the screen
player = Player(WIDTH, HEIGHT)

# Load an image for the food item
food_image = assets.loadImage(assets.assets["Food"])

# Set the world size (for the camera's bounds)
world_width, world_height = int(WIDTH * 2), int(HEIGHT * 2)
camera.set_world_size(world_width, world_height)

# List to hold food objects
foods = []

# Create food object at a random location within the world bounds
def spawnFood():
    x = random.randint(0, world_width - 50)  # Food size subtracted to prevent overflow
    y = random.randint(0, world_height - 50)
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
    if scene == "playArea":
        screen.fill((10, 11, 45))  # Clear screen

        # Spawn food randomly
        if random.random() < 0.08:  # Adjust the spawn rate here (8% chance each frame)
            spawnFood()

        # Check for food collision
        checkFoodCollision()

        # Draw all food items (apply camera transformation)
        for food_rect in foods:
            transformed_food_rect = camera.apply_rect(food_rect)  # Adjust food position
            screen.blit(food_image, transformed_food_rect)

        # Update player
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        player.update(keys, mouse_pos)

        # Draw player (apply camera transformation)
        screen.blit(player.image, camera.apply(player))
    elif scene == "menu":
        screen.fill((10, 11, 45))
        pass

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
