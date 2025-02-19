import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Viewport of the camera
        self.world_size = (0, 0)  # World boundaries

    def apply(self, entity):
        """Applies the camera transformation to an entity."""
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Applies the camera transformation to a rectangle (for food, objects, etc.)."""
        return rect.move(self.camera.topleft)

    def update(self, target):
        """Moves the camera to always follow the player properly."""
        self.camera.x = -target.x + int(self.camera.width / 2)
        self.camera.y = -target.y + int(self.camera.height / 2)

    def set_world_size(self, width, height):
        """Set the world size to the camera."""
        self.world_size = (width, height)
