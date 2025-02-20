import pygame
import assets
import creatures
import button
import time


class HUD:
    def __init__(self, w, h):

        self.WIDTH = w
        self.HEIGHT = h

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

        self.upg_n_l = assets.loadImage(assets.assets["upg_n"])
        self.upg_h_l = assets.loadImage(assets.assets["upg_h"])
        self.upg_a_l = assets.loadImage(assets.assets["upg_a"])

        sizeDown = False

        self.btn_2w = 206
        self.btn_2h = 206

        if sizeDown:
            self.btn_2w, nw = 206/1
            self.btn_2h, nh = 206/1
            self.upg_n_l = pygame.transform.scale(self.upg_n_l, (nw, nh))
            self.upg_h_l = pygame.transform.scale(self.upg_h_l, (nw, nh))
            self.upg_a_l = pygame.transform.scale(self.upg_a_l, (nw, nh))

    def update(self, food, stage, evolution, creature, creatureType, canUpgrade):
        self.food = food
        self.stage = stage
        self.evolution = evolution
        self.creature = creature
        self.creatureType = creatureType
        self.canUpgrade = canUpgrade

    def draw(self, screen, player):

        # HUD base
        screen.blit(self.hudImage, self.hudImageRect)

        # HUD text
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

        # upgrade button

        upgrade_button = button.Button(self.WIDTH-10-self.btn_2w/2, self.HEIGHT-10-self.btn_2h/2, self.upg_n_l, self.upg_h_l, self.upg_a_l, lambda: self.playerUpgrade(player), "Upgrade", assets.assets["audiowide"], 22, self.textcolor)

        if self.canUpgrade:
            upgrade_button.draw(screen)

    def playerUpgrade(self, player):
        player.upgrade()
        time.sleep(0.1)
