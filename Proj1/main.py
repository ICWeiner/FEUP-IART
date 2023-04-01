import pygame
from board import Board
from game_state import GameState
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

def draw_string(screen,string,size):
    s1 = pygame.font.SysFont('Arial',size).render(string, True, pygame.Color('white'))
    s1_rect = s1.get_rect()
    s1_rect.center = screen.get_rect().center
    screen.blit(s1, s1_rect)
    pygame.display.update()


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
                if menu.selected_option == 10:
                    return
                
                elif menu.selected_option == 8 or menu.selected_option == 9:
                    #print(menu.selected_option)
                    board = Board(LVL1_ROWS,LVL1_COLS) if menu.selected_option == 8 else Board(LVL2_ROWS,LVL2_COLS)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1)) if menu.selected_option == 8 else pygame.display.set_mode((SCREEN_SIZE_LVL2))
                    piece = None
                    selected_piece = None
                    drop_pos = None
                    count = 0
                    start_time = time.time()
                    mode = "UserLvl1" if menu.selected_option == 8 else "UserLvl2"
                    menu.isOpen = False

                elif menu.selected_option is not None:
                    #print(menu.selected_option)
                    if menu.selected_option == 0 or menu.selected_option == 1 or menu.selected_option == 2 or menu.selected_option == 3:
                        pc_play = PCPlay(GameState(Board(LVL1_ROWS,LVL1_COLS)))
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL1))
                    else:
                        pc_play = PCPlay(GameState(Board(LVL2_ROWS,LVL2_COLS)))
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))

                    draw_string(screen,"Loading...",TILESIZE//2)
                    
                    if menu.selected_option == 0 or menu.selected_option == 4:
                        pc_play.draw(pc_play.bfs(),screen,font)
                    elif menu.selected_option == 1 or menu.selected_option == 5:
                        pc_play.draw(pc_play.dfs(),screen,font)
                    elif menu.selected_option == 2  or menu.selected_option == 6:
                        pc_play.draw(pc_play.a_star_search(),screen,font)
                    else:
                        pc_play.draw(pc_play.greedy_search(),screen,font)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))
                    mode = "PC"
                    menu.isOpen = False
                    
                menu.selected_option = None

            else:
                if mode == "UserLvl1" or mode == "UserLvl2":
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
        elif mode == "UserLvl1" or mode == "UserLvl2":
            if board.goal_state():
                board.draw_Goal(screen,True)
            elif mode == "UserLvl1" and (count > 10 or time.time()-start_time > 30): #TODO change this later for different levels
                board.draw_Goal(screen,False)
            #elif mode == "UserLvl2" and (count > 30 or time.time()-start_time > 60):
                #board.draw_Goal(screen,False)
            elif menu.isOpen == False:
                board.draw(screen, count, start_time)
                board.draw_pieces(screen, font, selected_piece)
                piece, x, y = board.get_square_under_mouse()
                board.draw_selector(screen, piece)
                drop_pos = board.draw_drag(screen, font, selected_piece)
        else:
            draw_string(screen,"Press 'Esc' to access the menu",TILESIZE//3)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()