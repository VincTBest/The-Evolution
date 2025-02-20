import pygame

class Button:
    def __init__(self, x, y, n, h, a, command):
        self.x = x
        self.y = y
        self.n = n  # normal image
        self.h = h  # hover image
        self.a = a  # active image
        self.command = command
        self.rect = self.n.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                screen.blit(self.a, self.rect)  # active image when clicked
                if not self.clicked:
                    self.command()
                    self.clicked = True
            else:
                screen.blit(self.h, self.rect)  # hover image
                self.clicked = False  # reset click state
        else:
            screen.blit(self.n, self.rect)  # normal image

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
