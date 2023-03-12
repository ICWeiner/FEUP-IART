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
        return not (self.get_square(new_y, new_x) is not None
            or abs(new_x - old_x) > 1 or abs(new_y - old_y) > 1
            or abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1
            )


    def set_position(self, drop_pos, selected_piece):
        if drop_pos:
            new_x, new_y = drop_pos
            piece, old_x, old_y = selected_piece
            connected_pieces = self.get_connected_pieces(piece)
            old_connected_pieces = set(connected_pieces)

            for connected_piece in connected_pieces:
                self.set_square(connected_piece.y, connected_piece.x, None)

            valid = True
            for connected_piece in connected_pieces:
                if not self.verify_position(connected_piece.x + new_x - old_x, connected_piece.y + new_y - old_y, connected_piece.x, connected_piece.y):
                    for old_connected_piece in old_connected_pieces:
                        self.set_square(old_connected_piece.y, old_connected_piece.x, old_connected_piece)
                        valid = False
                    break

            if valid:
                for connected_piece in connected_pieces:    
                    self.set_square(connected_piece.y + new_y - old_y, connected_piece.x + new_x - old_x, connected_piece)

            return True
        return False
    

    def get_square(self, y, x):
        return self.board[y][x]


    def set_square(self, y, x, piece):
        self.board[y][x] = piece
        if piece != None:
            piece.set_piece(y,x)
        
                
    def get_connected_pieces(self, piece):
        if piece == None: return set()
        color = piece.color
        visited = set()
        connected = set()

        def dfs(x, y):
            if (x, y) in visited:
                return
            visited.add((x, y))

            if self.get_square(y, x) and self.get_square(y, x).color == color:
                connected.add(self.get_square(y, x))

                if x > 0:
                    dfs(x - 1, y)
                if x < self.cols - 1:
                    dfs(x + 1, y)
                if y > 0:
                    dfs(x, y - 1)
                if y < self.rows - 1:
                    dfs(x, y + 1)

        dfs(piece.x, piece.y)
        return set(connected)
    

##################################


    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        x, y = [int(v // TILESIZE) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (self.get_square(y,x), x, y)
        except IndexError: pass
        return None, None, None
    

    def draw_selector(self, screen, piece):
        connected_pieces = self.get_connected_pieces(piece)
        if connected_pieces != None:
            for piece in connected_pieces:
                rect = (piece.x * TILESIZE, piece.y * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)  #FIXME fix color
    

    def draw_drag(self, screen, selected_piece, font):
        if selected_piece:
            piece, x, y = self.get_square_under_mouse()
            if x != None:
                rect = (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                isValid = self.verify_position(x, y, selected_piece[0].x, selected_piece[0].y)
                pygame.draw.rect(screen, (0, 255, 0, 50) if isValid else pygame.Color('red'), rect, 2)

            s1 = font.render(selected_piece[0].type, True, pygame.Color(selected_piece[0].color))
            s2 = font.render(selected_piece[0].type, True, pygame.Color('darkgrey'))
            pos = pygame.Vector2(pygame.mouse.get_pos())
            screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
            screen.blit(s1, s1.get_rect(center=pos))
            selected_rect = pygame.Rect(selected_piece[1] * TILESIZE, selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
            return (x, y)
