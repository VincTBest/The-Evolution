import pygame
import math
import assets


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.angle = 0

        # Load player image (scaled)
        self.image = assets.loadImage(assets.assets["SingleCellOrganism"])

        # Create rect for positioning and collision
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, keys, mouse_pos):
        # Calculate angle towards the mouse
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        target_angle = math.degrees(math.atan2(-dy, dx))  # Negative dy for correct angle

        # Rotate with A/D or auto-face mouse
        if keys[pygame.K_a]:
            self.angle += 3
        elif keys[pygame.K_d]:
            self.angle -= 3
        else:
            self.angle = target_angle

        # Convert angle to radians
        rad = math.radians(self.angle)

        # Move forward/backward
        if keys[pygame.K_w]:
            self.x += math.cos(rad) * self.speed
            self.y -= math.sin(rad) * self.speed
        if keys[pygame.K_s]:
            self.x -= math.cos(rad) * self.speed
            self.y += math.sin(rad) * self.speed

        # Update rect position based on the new x and y
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Rotate and draw the player
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_img.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotated_img, rect.topleft)

    def center(self, width, height):
        """Centers the player within the screen."""
        self.rect.center = (width // 2, height // 2)
