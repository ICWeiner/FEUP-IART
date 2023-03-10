import pygame
from macros import TILESIZE

class Piece:

    def __init__(self, color, type, y, x):
        self.color = color
        self.type = type
        self.y = y
        self.x = x


    def draw(self, screen, font, selected):
        s1 = font.render(self.type, True, pygame.Color('darkgrey' if selected else self.color))
        s2 = font.render(self.type, True, pygame.Color('darkgrey'))
        pos = pygame.Rect(self.x * TILESIZE+1, self.y * TILESIZE + 1, TILESIZE, TILESIZE)
        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
        screen.blit(s1, s1.get_rect(center=pos.center))


    def set_piece(self, y, x):
        self.x = x
        self.y = y
