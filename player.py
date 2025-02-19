import pygame
import math
import assets

class Player:
    def __init__(self, screen_width, screen_height):
        # Dynamically set player's position to be the center of the window
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = 3
        self.angle = 0  # Rotation angle

        # Load and store the original player image
        self.original_image = assets.loadImage(assets.assets["SingleCellOrganism"])
        self.image = self.original_image  # Image used for drawing

        # Create a rect and center it
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, keys, mouse_pos):
        sprint = 1
        if pygame.key.get_mods() & pygame.KMOD_SHIFT == 1:
            sprint = 1.33


        # Calculate angle towards the mouse
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

        # Convert angle to radians for movement calculations
        rad = math.radians(self.angle)

        # Move forward/backward based on rotation
        if keys[pygame.K_w]:
            self.x += math.cos(rad) * self.speed*sprint
            self.y += math.sin(rad) * self.speed*sprint

        if keys[pygame.K_s]:
            self.x -= math.cos(rad) * self.speed*sprint
            self.y -= math.sin(rad) * self.speed*sprint

        # Update rect position
        self.rect.center = (self.x, self.y)

        # Rotate the image correctly
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Keep rect centered after rotation
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen, camera):
        """Draws the rotated player at the correct camera position."""
        transformed_rect = camera.apply(self)  # Get camera-adjusted position
        screen.blit(self.image, transformed_rect.topleft)
