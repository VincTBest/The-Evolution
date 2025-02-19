import os
import pygame


# Default texture pack
pack = "default"
assets = {}


def j(*paths):
    """Joins paths for cross-platform compatibility."""
    return os.path.join(*paths)


def changeTexturePack(newpack):
    """Changes the active texture pack and reloads assets."""
    global pack
    pack = newpack
    loadAssets()


def getBasePath():
    """Returns the base path for the current texture pack."""
    return j("textures", pack)


def loadAssets():
    """Loads all asset paths into the assets dictionary."""
    global assets
    basePath = getBasePath()

    assets = {
        "SingleCellOrganism": j(basePath, "creatures", "singleCell.png"),
        "MultiCellOrganism": j(basePath, "creatures", "multiCell.png"),
        "ProkaryotesBacteria": j(basePath, "creatures", "bacteriaProkaryotes.png"),
        "Food": j(basePath, "items", "food.png"),
    }


def loadImage(image_path):
    """Loads an image, scales it down by 25%, and returns a pygame.Surface."""
    try:
        image = pygame.image.load(image_path).convert_alpha()
        scaleAmount = 10
        width, height = image.get_size()
        new_size = (int(width * 1-scaleAmount/100), int(height * 1-scaleAmount/100))  # Scale down
        scaled_image = pygame.transform.scale(image, new_size)
        return scaled_image
    except pygame.error:
        print(f"Error loading image: {image_path}")
        return None


# Load assets initially
loadAssets()
