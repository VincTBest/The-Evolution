import pygame
import creatures
import time


class Debugger:  # only for cheaters and devs
    def __init__(self):
        pass

    def update(self, player, keys):
        K_SHIFT_F12 = keys[pygame.K_F12] and pygame.key.get_mods() & pygame.KMOD_SHIFT
        if K_SHIFT_F12 and keys[pygame.K_1]:
            player.setName("singleCell")
            player.changeData()
        if K_SHIFT_F12 and keys[pygame.K_2]:
            player.setName("multiCell")
            player.changeData()
        if K_SHIFT_F12 and keys[pygame.K_3]:
            player.setName("bacteriaProkaryotes")
            player.changeData()
        if K_SHIFT_F12 and keys[pygame.K_u]:
            player.upgrade()
        if K_SHIFT_F12 and keys[pygame.K_i]:
            player.addFood(10)
            time.sleep(0.1)
        if K_SHIFT_F12 and keys[pygame.K_o]:
            player.addFood(500)
            time.sleep(0.1)
        if K_SHIFT_F12 and keys[pygame.K_p]:
            player.addFood(creatures.creatures[player.get("creature")]["foodToUpgrade"])
            time.sleep(0.1)
