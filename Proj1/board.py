import pygame
from piece import Piece
from macros import TILESIZE
import time

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.pieces = {}

        self.board = []
        for y in range(self.cols):
            self.board.append([])
            for x in range(self.rows):
                self.board[y].append(None)

        self.add_piece('red',3,3)
        self.add_piece('red',0,0)
        self.add_piece('red',1,0)
        self.add_piece('red',1,1)
        self.add_piece('green',0,1)
        self.add_piece('yellow',0,3)
        self.add_piece('green',2,2)
        self.add_piece('green',2,3)
        self.add_piece('green',3,2)
        #self.add_piece('red',3,0)
        #self.add_piece('yellow',3,2)


    def __eq__(self, other):
        if isinstance(other, Board):
            return self.rows == other.rows and self.cols == other.cols and self.board == other.board
        return False
    
    def __hash__(self):
        rows = [tuple(row) for row in self.board]
        return hash(tuple(rows))
    
    def __str__(self):
        res = ""
        for y in range(self.rows):
            for x in range(self.cols):
                res += str(self.board[y][x]) + " "
            res += "\n"
        return res
    
    '''
    def __str__ (self):
        text=""
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece =self.board[y][x]
                if piece:
                    text.join(piece)
        return text
    '''

    
    def add_piece(self,color,x,y):
        piece = Piece(color,x,y)
        self.board[x][y] = piece
        if piece:
            if piece.color not in self.pieces:
                #self.pieces[piece.color] = set()
                self.pieces[piece.color]=1
            else:
                self.pieces[piece.color]+=1


    def draw(self, screen, count, start_time=None):
        board_surf = pygame.Surface((TILESIZE * self.rows, TILESIZE * self.cols))

        for y in range(self.cols):
            for x in range(self.rows):
                rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(board_surf, pygame.Color('darkgrey'), rect, 1)

        screen.blit(board_surf, (0, 0))
        
        #Moves
        font = pygame.font.SysFont('Arial', TILESIZE//3)
        s1 = font.render("Moves: " + str(count), True, pygame.Color('white'))
        s1_rect = s1.get_rect()
        s1_rect.bottomleft = (20, screen.get_height()-30)
        screen.blit(s1, s1_rect)

        #Time
        if start_time is not None:
            elapsed_time = time.time() - start_time
            timer_text = font.render("Time: {:.2f}s".format(elapsed_time), True, (255, 255, 255))
            screen.blit(timer_text, (screen.get_width() - timer_text.get_width() - 20, screen.get_height() - timer_text.get_height() - 30))
    

    def draw_pieces(self, screen, font, selected_piece=None):
        sx, sy = None, None
        selected = False
        if selected_piece:
            piece, sx, sy = selected_piece

        for y in range(self.cols):
            for x in range(self.rows): 
                piece = self.board[y][x]
                if piece:
                    if selected_piece: selected = x == sx and y == sy
                    piece.draw(screen, font, selected)
    
    
    def verify_position(self, new_x, new_y, old_x, old_y):
        if new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows:
            return False
        return not (self.get_square(new_y, new_x) is not None 
            or (new_x == old_x and new_y == old_y)
            or abs(new_x - old_x) > 1 or abs(new_y - old_y) > 1
            or abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1
            )


    def set_position(self, drop_pos, selected_piece):
        if not drop_pos or not selected_piece: return False
        
        new_x, new_y = drop_pos
        piece, old_x, old_y = selected_piece
        connected_pieces = piece.get_connected_pieces(self)
        old_connected_pieces = set(connected_pieces)

        for connected_piece in connected_pieces:
            self.set_square(connected_piece.y, connected_piece.x, None)

        for connected_piece in connected_pieces:
            if not self.verify_position(connected_piece.x + new_x - old_x, connected_piece.y + new_y - old_y, connected_piece.x, connected_piece.y):
                for old_connected_piece in old_connected_pieces:
                    self.set_square(old_connected_piece.y, old_connected_piece.x, old_connected_piece)
                return False

        for connected_piece in connected_pieces:    
            self.set_square(connected_piece.y + new_y - old_y, connected_piece.x + new_x - old_x, connected_piece)
        return True
    

    def get_square(self, y, x):
        return self.board[y][x]


    def set_square(self, y, x, piece):
        self.board[y][x] = piece
        if piece != None:
            piece.set_piece(y,x)
            

################################## Goal

    def goal_state(self):
        pieces = {}
        for y in range(self.rows):
            for x in range(self.cols):
                piece = self.get_square(y, x)
                if piece:
                    if piece.color not in pieces:
                        pieces[piece.color] = set()
                    pieces[piece.color].add(piece)

        for color, pieces_set in pieces.items():
            visited = set()
            stack = [pieces_set.pop()]
            while stack:
                piece = stack.pop()
                visited.add(piece)
                for connected_piece in piece.get_connected_pieces(self):
                    if connected_piece in pieces_set:
                        stack.append(connected_piece)
                        pieces_set.remove(connected_piece)
            if pieces_set:
                return False
        return True


    def draw_Goal(self, screen, win):
        font = pygame.font.SysFont('Arial', TILESIZE//2)
        if win:
            s1 = font.render("You Won! :)" , True, pygame.Color('white'))
        else:
            s1 = font.render("Game Over! :(" , True, pygame.Color('white')) #TODO add why (moves or time)

        s1_rect = s1.get_rect()
        s1_rect.center = screen.get_rect().center
        screen.blit(s1, s1_rect)
        pygame.display.update()


##################################


    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        x, y = [int(v // TILESIZE) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (self.get_square(y,x), x, y)
        except IndexError: pass
        return None, None, None
    

    def draw_selector(self, screen, piece):
        if piece != None:
            connected_pieces = piece.get_connected_pieces(self)
            for piece in connected_pieces:
                rect = (piece.x * TILESIZE, piece.y * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)  #FIXME fix color
    

    def draw_drag(self, screen, selected_piece, font):
        if selected_piece:
            piece, x, y = self.get_square_under_mouse()
            if x != None:
                rect = (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                isValid = self.verify_position(x, y, selected_piece[0].x, selected_piece[0].y)
                pygame.draw.rect(screen, (0, 255, 0, 50) if isValid else pygame.Color('red'), rect, 2)  #FIXME fix color

            s1 = font.render('■', True, pygame.Color(selected_piece[0].color))
            s2 = font.render('■', True, pygame.Color('darkgrey'))
            pos = pygame.Vector2(pygame.mouse.get_pos())
            screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
            screen.blit(s1, s1.get_rect(center=pos))
            selected_rect = pygame.Rect(selected_piece[1] * TILESIZE, selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
            return (x, y)
        return (None,None)
