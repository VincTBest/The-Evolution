import pygame
import math
import assets
import creatures


class Player:
    def __init__(self, screen_width, screen_height, walls, targetFps, joystick, mouse_pos):

        self.joystick = joystick
        self.controller = False

        self.liveSecs = 0
        self.liveFrame = 0
        self.isDead = False
        self.targetFps = targetFps
        self.frame = 0
        self.temp1 = False
        self.drawFrame = 0
        self.name = "singleCell"

        self.prev_mouse_pos = mouse_pos

        # Dynamically set player's position to be the center of the window
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.angle = 0  # Rotation angle
        self.walls = walls  # List of wall objects

        # Load and store the original player image
        self.original_image = assets.loadImage(assets.assets[creatures.getCreatures()[self.name]["imageName"]])
        self.image = self.original_image  # Image used for drawing

        # Create a rect and center it
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.canUpgrade = False

        # properties

        self.food = 5
        self.stage = 1
        self.stEvolution = 1
        self.stEvolution2 = 1
        self.evolution = 1

        # change-data properties

        self.speed = creatures.getCreatures()[self.name]["speed"]
        self.upgradeStageNeed = creatures.getCreatures()[self.name]["foodToUpgrade"]
        self.upgradeEvolNeed = creatures.getCreatures()[self.name]["stageToEvolve"]
        self.creature = creatures.getCreatures()[self.name]["id"]
        self.creatureType = creatures.getCreatures()[self.name]["type"]

        # gui
        self.textcolor = (214, 214, 235)
        self.font = pygame.font.Font(assets.assets["audiowide"], 26)

    def check_collision(self, next_x, next_y):
        """Returns True if the next position collides with a wall."""
        next_rect = self.rect.copy()
        next_rect.center = (next_x, next_y)
        return any(next_rect.colliderect(wall) for wall in self.walls)

    def update(self, keys, mouse_pos, joystick):

        l_x = 0
        l_y = 0
        r_x = 0
        r_y = 0

        if joystick is not None:
            l_x = self.joystick.get_axis(0)
            l_y = self.joystick.get_axis(1)
            r_x = self.joystick.get_axis(2)
            r_y = self.joystick.get_axis(3)

        if not self.isDead:
            self.liveFrame += 1
            self.liveSecs = self.liveFrame/60

        self.frame += 1



        cps = 8
        sprint = 1
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            sprint = 1.33
            cps = 2

        if self.controller and joystick.get_axis(5)>-0.45:
            sprint = 1.33
            cps = 2

        if self.frame >= self.targetFps*cps:
            self.frame = 0
            self.food -= 1

        if self.food < 0:
            self.speed = 0
            self.die()
            self.food = 5
            self.setName("singleCell")
            self.changeData()

        next_x, next_y = self.x, self.y

        if not self.controller:

            # Calculate angle towards the mouse
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            self.angle = math.degrees(math.atan2(dy, dx))

            # Convert angle to radians for movement calculations
            rad = math.radians(self.angle)

            if (abs(mouse_pos[0] - self.x) > 6) or (abs(mouse_pos[1] - self.y) > 6):
                if keys[pygame.K_w]:  # Forward movement
                    new_x = self.x + math.cos(rad) * self.speed * sprint
                    new_y = self.y + math.sin(rad) * self.speed * sprint
                    if not self.check_collision(new_x, new_y):
                        next_x, next_y = new_x, new_y

                if keys[pygame.K_s]:  # Backward movement
                    new_x = self.x - math.cos(rad) * self.speed * sprint
                    new_y = self.y - math.sin(rad) * self.speed * sprint
                    if not self.check_collision(new_x, new_y):
                        next_x, next_y = new_x, new_y
        else:
            if abs(r_x) > 0.25 or abs(r_y) > 0.25:  # Prevent drift
                self.angle = math.degrees(math.atan2(r_y, r_x))  # Rotate towards right stick direction
                rad = math.radians(self.angle)  # Update movement angle

                new_x = self.x + math.cos(rad) * self.speed * sprint
                new_y = self.y + math.sin(rad) * self.speed * sprint
                if not self.check_collision(new_x, new_y):
                    next_x, next_y = new_x, new_y

        # Apply movement
        self.x, self.y = next_x, next_y
        self.rect.center = (self.x, self.y)

        # Rotate the image correctly
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Keep rect centered after rotation
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.food >= self.upgradeStageNeed:
            self.canUpgrade = True
        else:
            self.canUpgrade = False

        if self.stage >= self.upgradeEvolNeed:
            self.stage -= self.upgradeEvolNeed
            self.evolution += 1

        if self.evolution != self.stEvolution2:
            self.stEvolution2 = self.evolution
            self.setName(creatures.tiers[self.evolution])
            self.changeData()

        if any([keys[key] for key in
                [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_LSHIFT]]) or \
                pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1] or mouse_pos != self.prev_mouse_pos:
            self.controller = False

        elif any([self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]) or abs(
                l_x) > 0.25 or abs(l_y) > 0.25 or abs(r_x) > 0.25 or abs(r_y) > 0.25:
            self.controller = True

        self.prev_mouse_pos = mouse_pos

    def draw(self, screen):
        self.drawFrame += 1

        if self.evolution != self.stEvolution:  # DO NOT TOUCH
            if self.drawFrame <= self.targetFps*3:
                textSurface = self.font.render("You Evolved!", True, self.textcolor)
                textRect = textSurface.get_rect()
                textRect.center = (self.screen_width / 2, 40)
                screen.blit(textSurface, textRect.topleft)
                self.temp1 = True
            else:
                oldDraw = self.drawFrame
                self.drawFrame = 0
                if self.temp1:
                    self.stEvolution = self.evolution
                    self.drawFrame = oldDraw
        else:
            self.temp1 = False

    def addFood(self, amount):
        self.food += amount

    def get(self, name):
        if name == "food":
            return self.food
        elif name == "stage":
            return self.stage
        elif name == "evolution":
            return self.evolution
        elif name == "creature":
            return self.creature
        elif name == "creatureType":
            return self.creatureType
        elif name == "canUpgrade":
            return self.canUpgrade
        else:
            return None

    def setName(self, name):
        self.name = name

    def changeData(self):
        self.creature = creatures.getCreatures()[self.name]["id"]
        self.upgradeStageNeed = creatures.getCreatures()[self.name]["foodToUpgrade"]
        self.upgradeEvolNeed = creatures.getCreatures()[self.name]["stageToEvolve"]
        self.creatureType = creatures.getCreatures()[self.name]["type"]
        self.speed = creatures.getCreatures()[self.name]["speed"]

        # image stuff

        self.original_image = assets.loadImage(assets.assets[creatures.getCreatures()[self.name]["imageName"]])
        self.image = self.original_image  # Image used for drawing

    def upgrade(self):
        self.food -= self.upgradeStageNeed
        self.stage += 1

    def die(self):
        self.isDead = True

    def dead(self):
        return self.isDead

    def getLive(self):
        return self.liveSecs, self.liveFrame
