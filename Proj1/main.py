import pygame
from board import Board
from game_state import GameState
from queue import PriorityQueue
from menu import Menu
from macros import *
import time
from pc_play import PCPlay

# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀      💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀🪟      💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀        💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀  💀  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀

def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', TILESIZE)
    pygame.display.set_caption('Cohesion')
    screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))
    menu = Menu(SCREEN_SIZE_LVL2)

    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

            if menu.isOpen:
                menu.handle_events(events)

                if menu.selected_option == 6:
                    return
                
                elif menu.selected_option == 4 or menu.selected_option == 5:
                    board = Board(LVL1_ROWS,LVL1_COLS) if menu.selected_option == 4 else Board(LVL2_ROWS,LVL2_COLS)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1)) if menu.selected_option == 4 else pygame.display.set_mode((SCREEN_SIZE_LVL2))
                    piece = None
                    selected_piece = None
                    drop_pos = None
                    count = 0
                    start_time = time.time()
                    menu.isOpen = False

                elif menu.selected_option is not None:
                    pc_play = PCPlay(GameState(Board(LVL1_ROWS,LVL1_COLS)))
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1))
                    pc_play.draw_loading(screen)
                    
                    if menu.selected_option == 0:
                        pc_play.draw(pc_play.bfs(),screen,font)
                    elif menu.selected_option == 1:
                        pc_play.draw(pc_play.dfs(),screen,font)
                    elif menu.selected_option == 2:
                        pc_play.draw(pc_play.a_star_search(),screen,font)
                    else:
                        pc_play.draw(pc_play.greedy_search(),screen,font)

                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))
                    
                menu.selected_option = None

            else:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece is not None:
                        selected_piece = piece, x, y

                if e.type == pygame.MOUSEBUTTONUP:
                    set = board.set_position(drop_pos, selected_piece)
                    if set:
                        count += 1
                    selected_piece = None
                    drop_pos = None

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))
                        menu.selected_option = None
                        menu.isOpen = True
        
        screen.fill((0, 0, 0))
        if menu.isOpen:
            menu.draw(screen)
        elif board.goal_state():
            board.draw_Goal(screen,True)
        #elif (count > 5 or time.time()-start_time > 30): #TODO change this later for different levels
            #board.draw_Goal(screen,False)
        else:
            board.draw(screen, count, start_time)
            board.draw_pieces(screen, font, selected_piece)
            piece, x, y = board.get_square_under_mouse()
            board.draw_selector(screen, piece)
            drop_pos = board.draw_drag(screen, font, selected_piece)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()