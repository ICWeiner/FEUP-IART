import pygame
from macros import TILESIZE

class Piece:

    def __init__(self, color, y, x):
        self.color = color
        self.y = y
        self.x = x


    def __str__(self):
        return  "Piece has color:" + str(self.color) +  " Y:" + str(self.y) + "X:" + str(self.x) 
    
    def __eq__(self, other):
        if not other:
            return False
        #print( ( self.color == other.color and self.y == other.y and self.x == other.x) )
        return self.color == other.color and self.y == other.y and self.x == other.x

    def __hash__(self):
        return hash((str(self.color) + str(self.y) + str(self.x)))
    

    def draw(self, screen, font, selected):
        s1 = font.render('■', True, pygame.Color('darkgrey' if selected else self.color))
        s2 = font.render('■', True, pygame.Color('darkgrey'))
        pos = pygame.Rect(self.x * TILESIZE+1, self.y * TILESIZE+1, TILESIZE, TILESIZE)
        screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
        screen.blit(s1, s1.get_rect(center=pos.center))


    def set_piece(self, y, x):
        self.x = x
        self.y = y


    def get_connected_pieces(self, board):
        visited = set()
        connected = set()

        def dfs(x, y):
            if (x, y) in visited:
                return
            visited.add((x, y))

            if board.get_square(y, x) and board.get_square(y, x).color == self.color:
                connected.add(board.get_square(y, x))

                if x > 0:
                    dfs(x - 1, y)
                if x < board.cols - 1:
                    dfs(x + 1, y)
                if y > 0:
                    dfs(x, y - 1)
                if y < board.rows - 1:
                    dfs(x, y + 1)

        dfs(self.x, self.y)
        return set(connected)
