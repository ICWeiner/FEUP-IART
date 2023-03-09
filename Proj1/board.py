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

        self.board[0][0] = Piece('red', '■', 0, 0)
        self.board[1][0] = Piece('red', '■', 1, 0)
        self.board[1][1] = Piece('red', '■', 1, 1)
        self.board[0][1] = Piece('green', '■', 0, 1)
        self.board[0][3] = Piece('yellow', '■', 0, 3)
        self.board[2][2] = Piece('green', '■', 2, 2)
        self.board[2][3] = Piece('green', '■', 2, 3)
        self.board[3][2] = Piece('green', '■', 3, 2)
        self.board[3][3] = Piece('red', '■', 3, 3)


    def create_board_surf(self):
        board_surf = pygame.Surface((TILESIZE * self.rows, TILESIZE * self.cols))

        for y in range(self.cols):
            for x in range(self.rows):
                rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(board_surf, pygame.Color('darkgrey'), rect, 1)
        
        return board_surf
    

    def draw_pieces(self, screen, font, selected_piece):
        sx, sy = None, None
        selected = False
        if selected_piece:
            piece, sx, sy = selected_piece

        for y in range(self.cols):
            for x in range(self.rows): 
                piece = self.board[y][x]
                if piece:
                    selected = x == sx and y == sy
                    piece.draw(screen, font, selected)


    def verify_position(self, new_x, new_y, old_x, old_y):
        if (self.get_square(new_y, new_x) is not None
            or abs(new_x - old_x) > 1 or abs(new_y - old_y) > 1
            or abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1
            ):
            return False

        return True


    def set_position(self, drop_pos, selected_piece):
        if drop_pos:
            new_x, new_y = drop_pos
            piece, old_x, old_y = selected_piece
            if self.verify_position(new_x, new_y, old_x, old_y):
                self.set_square(old_y, old_x, None)
                self.set_square(new_y, new_x, piece)
                return True
        return False
    

    def get_square(self, y, x):
        return self.board[y][x]


    def set_square(self, y, x, piece):
        self.board[y][x] = piece
        if piece != None: piece.set_piece(y,x)


