import pygame
import assets
import creatures


class HUD:
    def __init__(self):

        self.food = None
        self.stage = None
        self.evolution = None
        self.creature = None
        self.creatureType = None
        self.canUpgrade = None

        # define sprites
        self.hud_topleft = assets.loadImage(assets.assets["hud_topleft"])
        self.hudImage = self.hud_topleft
        self.hudImage = pygame.transform.scale(self.hudImage, (630/5*3, 251/5*3))
        self.hudImageRect = self.hudImage.get_rect()
        self.hudImageRect.x = -8
        self.hudImageRect.y = -8
        self.font = pygame.font.Font(assets.assets["audiowide"], 22)
        self.bigFont = pygame.font.Font(assets.assets["audiowide"], 36)
        self.textcolor = (214, 214, 235)

    def update(self, food, stage, evolution, creature, creatureType, canUpgrade):
        self.food = food
        self.stage = stage
        self.evolution = evolution
        self.creature = creature
        self.creatureType =creatureType
        self.canUpgrade = canUpgrade


    def draw(self, screen):
        screen.blit(self.hudImage, self.hudImageRect)
        textSurface = self.font.render(f"Food: {self.food}", True, self.textcolor)
        textRect = textSurface.get_rect()
        textRect.x = self.hudImageRect.x + 15-2
        textRect.y = self.hudImageRect.y + 251/5*3-35-2
        screen.blit(textSurface, textRect)
        textSurface = self.font.render(f"Stage: {self.stage}", True, self.textcolor)
        textRect = textSurface.get_rect()
        textRect.x = self.hudImageRect.x + 15+110+15-2
        textRect.y = self.hudImageRect.y + 251/5*3-35-2
        screen.blit(textSurface, textRect)
        textSurface = self.bigFont.render(f"{creatures.creatures[self.creature]["name"]}", True, self.textcolor)
        textRect = textSurface.get_rect()
        textRect.x = 7
        textRect.y = 4
        screen.blit(textSurface, textRect.topleft)
        textSurface = self.font.render(f"{creatures.creatures[self.creature]["type"]}", True, self.textcolor)
        textRect = textSurface.get_rect()
        textRect.x = 7
        textRect.y = 46
        screen.blit(textSurface, textRect.topleft)
