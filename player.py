import pygame
import math
import assets
import creatures

class Player:
    def __init__(self, screen_width, screen_height, walls):
        # Dynamically set player's position to be the center of the window
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = 3
        self.angle = 0  # Rotation angle
        self.walls = walls  # List of wall objects

        # Load and store the original player image
        self.original_image = assets.loadImage(assets.assets["SingleCellOrganism"])
        self.image = self.original_image  # Image used for drawing

        # Create a rect and center it
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.canUpgrade = False

        # properties

        self.food = 5
        self.upgradeStageNeed = creatures.getCreatures()["singleCell"]["foodToUpgrade"]
        self.stage = 1
        self.evolution = 1
        self.creature = creatures.getCreatures()["singleCell"]["id"]
        self.creatureType = creatures.getCreatures()["singleCell"]["type"]

    def check_collision(self, next_x, next_y):
        """Returns True if the next position collides with a wall."""
        next_rect = self.rect.copy()
        next_rect.center = (next_x, next_y)
        return any(next_rect.colliderect(wall) for wall in self.walls)

    def update(self, keys, mouse_pos):
        sprint = 1
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            sprint = 1.33

        # Calculate angle towards the mouse
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

        # Convert angle to radians for movement calculations
        rad = math.radians(self.angle)

        # Predict next position
        next_x, next_y = self.x, self.y

        if (abs(mouse_pos[0] - self.x) > 4) or (abs(mouse_pos[1] - self.y) > 4):
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


    def draw(self, screen, camera):
        """Draws the rotated player at the correct camera position."""
        transformed_rect = camera.apply(self)  # Get camera-adjusted position
        screen.blit(self.image, transformed_rect.topleft)

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
