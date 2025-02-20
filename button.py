import pygame

class Button:
    def __init__(self, x, y, n, h, a, command, text, font, fontsize, textcolor):
        self.x = x
        self.y = y
        self.n = n  # normal image
        self.h = h  # hover image
        self.a = a  # active image
        self.command = command
        self.rect = self.n.get_rect(center=(x, y))
        self.clicked = False
        self.text = text
        self.font = pygame.font.Font(font, fontsize)
        self.textcolor = textcolor

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

        textSurface = self.font.render(self.text, True, self.textcolor)
        textRect = textSurface.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(textSurface, textRect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False


class QImg:
    def __init__(self, x, y, img, w, h):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (w, h))

    def draw(self, screen):

        imgRect = self.img.get_rect()
        imgRect.center = (self.x, self.y)
        screen.blit(self.img, imgRect)
