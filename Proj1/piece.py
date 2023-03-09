import pygame
from macros import TILESIZE

class Piece:

    def __init__(self, color, type):
        self.color = color
        self.type = type


    def draw(self, screen, font, x, y, selected):
        s1 = font.render(self.type[0], True, pygame.Color('darkgrey' if selected else self.color))
        s2 = font.render(self.type[0], True, pygame.Color('darkgrey'))
        pos = pygame.Rect(x * TILESIZE+1, y * TILESIZE + 1, TILESIZE, TILESIZE)
        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
        screen.blit(s1, s1.get_rect(center=pos.center))

