import pygame
from piece import Piece
from macros import TILESIZE

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.board = []
        for y in range(self.cols):
            self.board.append([])
            for x in range(self.rows):
                self.board[y].append(None)

        self.board[0][0] = Piece('red', '■')
        self.board[1][0] = Piece('red', '■')
        self.board[1][1] = Piece('red', '■')
        self.board[0][1] = Piece('green', '■')
        self.board[0][3] = Piece('yellow', '■')
        self.board[2][2] = Piece('green', '■')
        self.board[2][3] = Piece('green', '■')
        self.board[3][2] = Piece('green', '■')
        self.board[3][3] = Piece('red', '■')


    def create_board_surf(self):
        board_surf = pygame.Surface((TILESIZE * self.rows, TILESIZE * self.cols))

        for y in range(self.cols):
            for x in range(self.rows):
                rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(board_surf, pygame.Color('darkgrey'), rect, 1)
        
        return board_surf
    

    def draw_pieces(self, screen, font, selected_piece):
        sx, sy = None, None
        if selected_piece:
            piece, sx, sy = selected_piece

        for y in range(self.cols):
            for x in range(self.rows): 
                piece = self.board[y][x]
                if piece:
                    selected = x == sx and y == sy
                    piece.draw(screen, font, x, y, selected)


    def verify_and_set_position(self, drop_pos, selected_piece):
        if drop_pos:
            new_x, new_y = drop_pos
            piece, old_x, old_y = selected_piece
            if not (self.get_piece(new_y, new_x) != None 
                or new_x > old_x+1 or new_y > old_y+1 
                or new_x < old_x-1 or new_y < old_y-1
                or ((old_x+1 == new_x and old_y+1 == new_y)
                or (old_x-1 == new_x and old_y-1 == new_y)
                or (old_x-1 == new_x and old_y+1 == new_y)
                or (old_x+1 == new_x and old_y-1 == new_y))
            ):
                self.set_piece(old_y, old_x, None)
                self.set_piece(new_y, new_x, piece)
                
        return None
    

    def get_piece(self, y, x):
        return self.board[y][x]


    def set_piece(self, y, x, piece):
        self.board[y][x] = piece

