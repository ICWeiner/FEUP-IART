import pygame
from macros import TILESIZE

class Menu:
    def __init__(self, screen_size):
        self.font = pygame.font.SysFont('Arial', TILESIZE//2)
        self.options = ['New Game 4x4','New Game 6x6','Quit']
        self.labels = [self.font.render(option, True, (255, 255, 255)) for option in self.options]
        self.width = max(label.get_width() for label in self.labels)
        self.height = len(self.options) * self.font.get_height()
        self.x = (screen_size[0] - self.width) // 2
        self.y = (screen_size[1] - self.height) // 2
        self.rects = [pygame.Rect(self.x - 10, self.y + i * (self.font.get_height() + 10), self.width + 20, self.font.get_height() + 10) for i in range(len(self.options))]
        self.selected_option = None
        self.isOpen = True
    

    def draw(self, screen):
        for i, label in enumerate(self.labels):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            screen.blit(label, (self.x - 10 + 5, self.y + i * (self.font.get_height() + 10) + 5))
            pygame.draw.rect(screen, color, self.rects[i], 2)
            if self.rects[i].collidepoint(pygame.mouse.get_pos()):
                color = (255, 0, 0)
                screen.blit(label, (self.x - 10 + 5, self.y + i * (self.font.get_height() + 10) + 5))
                pygame.draw.rect(screen, color, self.rects[i], 2)


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        self.selected_option = i

            if e.type == pygame.MOUSEBUTTONUP:
                if self.selected_option is not None:
                    return self.selected_option
                self.selected_option = None
        return None
    

    def setIsOpen(self, b):
        self.isOpen = b
