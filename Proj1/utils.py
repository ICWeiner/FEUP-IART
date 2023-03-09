import pygame
from macros import TILESIZE

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board.get_square(y,x), x, y)
    except IndexError: pass
    return None, None, None


def draw_selector(screen, piece):
    if piece != None:
        rect = (piece.x * TILESIZE, piece.y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, board, selected_piece, font):
    if selected_piece:
        piece, x, y = get_square_under_mouse(board)
        if x != None:
            rect = (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, type = (selected_piece[0].color, selected_piece[0].type)
        s1 = font.render(type[0], True, pygame.Color(color))
        s2 = font.render(type[0], True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(selected_piece[1] * TILESIZE, selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (x, y)