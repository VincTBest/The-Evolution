import req
try:
    import pygame
    import button
    import assets
    import random
    import hud
    import debug
    import controller
    import ds
    from player import Player
    from camera import Camera
except ImportError as e:
    print(e)
    print("Installing third-party packages")
    req.install_packages()
    quit()

targetFps = 60
scene = "menu"

# init
pygame.init()
pygame.font.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    joystickType = controller.get_controller_type()
else:
    joystick = None
    joystickType = None

screenSizeTest = False

# Screen settings (convert to integers)
if screenSizeTest:
    WIDTH = random.randint(min(int(1920 / 5 * 4), int(1024 / 5 * 4)), max(int(1920 / 5 * 4), int(1024 / 5 * 4)))
    HEIGHT = random.randint(min(int(1080 / 5 * 4), int(768 / 5 * 4)), max(int(1080 / 5 * 4), int(768 / 5 * 4)))
else:
    WIDTH, HEIGHT = int(1920 / 5 * 4), int(1080 / 5 * 4)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Evolution")

# Create camera
camera = Camera(WIDTH, HEIGHT)

walls = []

mouse_pos = pygame.mouse.get_pos()

# Create player at the center of the screen
player = Player(WIDTH, HEIGHT, walls, targetFps, joystick, mouse_pos)

# Create HUD
hud = hud.HUD(WIDTH, HEIGHT)

# Create Keys
keys = pygame.key.get_pressed()

# Create Debug
debug = debug.Debugger()
debug.update(player, keys)

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
            player.addFood(1)
            if joystick is not None:
                joystick.rumble(4, 7, 200)
            break  # Only remove one food at a time


def setScene(sceneName):
    global scene
    scene = sceneName


# Spawn initial food
spawnFood()

clock = pygame.time.Clock()
running = True

btn_n_l = assets.loadImage(assets.assets["btn_n"])
btn_h_l = assets.loadImage(assets.assets["btn_h"])
btn_a_l = assets.loadImage(assets.assets["btn_a"])

play_button = button.Button(WIDTH/2, HEIGHT/2-80, btn_n_l, btn_h_l, btn_a_l, lambda: setScene("playArea"), "Play", assets.assets["audiowide"], 26, (214, 214, 235))
options_button = button.Button(WIDTH/2, HEIGHT/2, btn_n_l, btn_h_l, btn_a_l, lambda: setScene("opt"), "Options", assets.assets["audiowide"], 26, (214, 214, 235))
quit_button = button.Button(WIDTH/2, HEIGHT/2+80, btn_n_l, btn_h_l, btn_a_l, lambda: quit(), "Quit", assets.assets["audiowide"], 26, (214, 214, 235))

menu_button = button.Button(WIDTH/2, 40, btn_n_l, btn_h_l, btn_a_l, lambda: setScene("menu"), "Main Menu", assets.assets["audiowide"], 26, (214, 214, 235))

# controller diagrams

dag_scd = 5
dag_y = 110

ps5_diagram = button.QImg(WIDTH/2, dag_y, assets.loadImage(assets.assets["ps5_diagram"]), 1452/dag_scd, 940/dag_scd)
ps4_diagram = button.QImg(WIDTH/2, dag_y, assets.loadImage(assets.assets["ps4_diagram"]), 1452/dag_scd, 940/dag_scd)
x_diagram = button.QImg(WIDTH/2, dag_y, assets.loadImage(assets.assets["x_diagram"]), 1452/dag_scd, 940/dag_scd)
al_diagram = button.QImg(WIDTH/2, dag_y, assets.loadImage(assets.assets["al_diagram"]), 1452/dag_scd, 940/dag_scd)

while running:

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystickType = controller.get_controller_type()
    else:
        joystick = None
        joystickType = None

    keys = pygame.key.get_pressed()
    debug.update(player, keys)
    if scene == "playArea":

        hud.update(player.get("food"), player.get("stage"), player.get("evolution"), player.get("creature"), player.get("creatureType"), player.get("canUpgrade"))

        screen.fill((10, 11, 45))  # Clear screen

        # Spawn food randomly
        if random.random() < 0.08:
            spawnFood()

        # Check for food collision
        checkFoodCollision()

        # Draw all food items (apply camera transformation)
        for food_rect in foods:
            transformed_food_rect = camera.apply_rect(food_rect)  # Adjust food position
            screen.blit(food_image, transformed_food_rect)

        # Update player

        mouse_pos = pygame.mouse.get_pos()
        player.update(keys, mouse_pos, joystick)

        # Draw player (apply camera transformation)
        screen.blit(player.image, camera.apply(player))
        player.draw(screen)
        hud.draw(screen, player)

        if player.isDead:
            setScene("playerDead")

    elif scene == "menu":
        screen.fill((10, 11, 45))

        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        if joystickType is not None and joystickType != "unk":
            if joystickType == "ps5":
                ps5_diagram.draw(screen)
            elif joystickType == "ps4":
                ps4_diagram.draw(screen)
            elif joystickType == "x":
                x_diagram.draw(screen)
            elif joystickType == "al":
                al_diagram.draw(screen)

    elif scene == "playerDead":
        screen.fill((10, 11, 45))
        font01 = pygame.font.Font(assets.assets["audiowide"], 28)
        textSurface = font01.render(f"You're dead", True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2-16)
        menu_button.draw(screen)
        screen.blit(textSurface, textRect)
        textSurface = font01.render(f"You survived {player.getLive()[0]} seconds", True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2+16)
        menu_button.draw(screen)
        screen.blit(textSurface, textRect)

    else:
        screen.fill((0, 0, 0))
        font01 = pygame.font.Font(assets.assets["audiowide"], 26)
        textSurface = font01.render(f"No scene named \"{scene}\"", True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2)
        menu_button.draw(screen)
        screen.blit(textSurface, textRect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            ds.cl_ds()

    pygame.display.flip()
    clock.tick(targetFps)

pygame.quit()
