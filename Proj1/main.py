import pygame
from board import Board
from utils import get_square_under_mouse, draw_selector, draw_drag
from macros import SCREEN_SIZE, TILESIZE, ROWS, COLS

def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', TILESIZE)
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))

    board = Board(ROWS,COLS)
    board_surf = board.create_board_surf()

    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    while True:
        piece, x, y = get_square_under_mouse(board)
        events = pygame.event.get()
        
        for e in events:
            if e.type == pygame.QUIT:
                return
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, x, y

            if e.type == pygame.MOUSEBUTTONUP:
                board.verify_and_set_position(drop_pos, selected_piece)
                selected_piece = None
                drop_pos = None

        screen.blit(board_surf, (0, 0))
        board.draw_pieces(screen, font, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

