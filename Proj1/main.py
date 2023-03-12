import pygame
from board import Board
from menu import Menu
from macros import SCREEN_SIZE, TILESIZE, ROWS, COLS

def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', TILESIZE)
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))

    menu = Menu(SCREEN_SIZE)
    
    board = Board(ROWS,COLS)
    
    selected_piece = None
    drop_pos = None

    while True:
        piece, x, y = board.get_square_under_mouse()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return

            if menu.isOpen:
                selected_option = menu.handle_events(events)
                if selected_option == 0:
                    menu.setIsOpen(False)
                elif selected_option == 1:
                    return
                selected_option = None

            else:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece is not None:
                        selected_piece = piece, x, y

                if e.type == pygame.MOUSEBUTTONUP:
                    board.set_position(drop_pos, selected_piece)
                    selected_piece = None
                    drop_pos = None

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        menu.setIsOpen(True)

        screen.fill((0, 0, 0))
        if menu.isOpen:
            menu.draw(screen)
        else:
            board.draw(screen)
            board.draw_pieces(screen, font, selected_piece)
            board.draw_selector(screen, piece)
            drop_pos = board.draw_drag(screen, selected_piece, font)

        pygame.display.flip()

if __name__ == '__main__':
    main()