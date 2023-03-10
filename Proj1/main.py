import pygame
from board import Board
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
        piece, x, y = board.get_square_under_mouse()
        events = pygame.event.get()
        
        for e in events:
            if e.type == pygame.QUIT:
                return
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, x, y

            if e.type == pygame.MOUSEBUTTONUP:
                board.set_position(drop_pos, selected_piece)
                selected_piece = None
                drop_pos = None

        screen.blit(board_surf, (0, 0))
        board.draw_pieces(screen, font, selected_piece)
        board.draw_selector(screen, piece)
        drop_pos = board.draw_drag(screen, selected_piece, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

