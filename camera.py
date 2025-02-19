import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # The viewport of the camera
        self.world_size = (0, 0)  # Initial world size
        self.zoom = 1  # Zoom level (no zoom = 1)

    def apply(self, entity):
        """Applies the camera transformation to an entity."""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Moves the camera to always follow the target (player)."""
        # Directly center the camera on the player's position
        x = 0
        y = 0

        # Apply the new camera position
        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)

    def set_world_size(self, width, height):
        """Set the world size to the camera."""
        self.world_size = (width, height)
