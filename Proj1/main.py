
import pygame
from board import Board
from game_state import GameState
from menu import Menu
from macros import *
from pc_play import PCPlay
import time

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
    menu1 = Menu(SCREEN_SIZE_LVL2,['New Game 4x4','New Game 6x6','Quit'])
    menu2 = Menu(SCREEN_SIZE_LVL2,['Play','BFS','DFS','A*','Greedy','Quit'])
    menu3 = Menu(SCREEN_SIZE_LVL2,['Manhattan','Colour Cluster','Quit'])
    menu2.isOpen = False
    menu3.isOpen = False
    score = 0

    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

            elif menu1.isOpen:
                menu1.handle_events(events)
                if menu1.selected_option == 2:
                    return
                
                elif menu1.selected_option is not None:
                    board = Board(LVL1_ROWS,LVL1_COLS) if menu1.selected_option == 0 else Board(LVL2_ROWS,LVL2_COLS)
                    menu1.isOpen = False
                    menu2.isOpen = True
                    events = []

            elif menu2.isOpen:
                menu2.handle_events(events)

                if menu2.selected_option == 5:
                    return
                
                elif menu2.selected_option == 0:
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1)) if menu1.selected_option == 0 else pygame.display.set_mode((SCREEN_SIZE_LVL2))
                    piece = None
                    selected_piece = None
                    drop_pos = None
                    moves = 0
                    start_time = time.time()
                    mode = "UserLvl1" if menu1.selected_option == 0 else "UserLvl2"
                    menu2.isOpen = False
                    menu1.selected_option = None
                    menu2.selected_option = None
                
                elif menu2.selected_option is not None:
                    if menu2.selected_option == 3 or menu2.selected_option == 4:
                        menu3.isOpen = True
                        events = []

                    else:
                        if menu1.selected_option == 0:
                            pc_play = PCPlay(GameState(Board(LVL1_ROWS,LVL1_COLS)))
                            screen = pygame.display.set_mode((SCREEN_SIZE_LVL1))

                        elif menu1.selected_option == 1:
                            pc_play = PCPlay(GameState(Board(LVL2_ROWS,LVL2_COLS)))
                            screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))

                        draw_string(screen,"Loading...",TILESIZE//2)

                        if menu2.selected_option == 1:
                            pc_play.draw(pc_play.bfs(),screen,font)

                        elif menu2.selected_option == 2:
                            pc_play.draw(pc_play.dfs(),screen,font)

                        menu1.selected_option = None
                        menu2.selected_option = None
                    menu2.isOpen = False
                    mode = "PC"

            elif menu3.isOpen:
                menu3.handle_events(events)
                if menu3.selected_option == 2:
                    return
                
                elif menu3.selected_option is not None:
                    if menu1.selected_option == 0:
                            pc_play = PCPlay(GameState(Board(LVL1_ROWS,LVL1_COLS)))
                            screen = pygame.display.set_mode((SCREEN_SIZE_LVL1))

                    elif menu1.selected_option == 1:
                            pc_play = PCPlay(GameState(Board(LVL2_ROWS,LVL2_COLS)))
                            screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))

                    draw_string(screen,"Loading...",TILESIZE//2)

                    if menu2.selected_option == 3:
                        if menu3.selected_option == 0:
                            pc_play.draw(pc_play.a_star_search(),screen,font)
                        else:
                            pc_play.draw(pc_play.a_star_search("color"),screen,font)
                    else:
                        if menu2.selected_option == 4:
                            if menu3.selected_option == 0:
                                pc_play.draw(pc_play.greedy_search(),screen,font)
                            else:
                                pc_play.draw(pc_play.greedy_search("color"),screen,font)
                    menu3.isOpen = False
                    menu2.selected_option = None
                    menu1.selected_option = None
                menu3.selected_option = None

            else:
                if mode == "UserLvl1" or mode == "UserLvl2":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if piece is not None:
                            selected_piece = piece, x, y

                    if e.type == pygame.MOUSEBUTTONUP:
                        set = board.set_position(drop_pos, selected_piece)
                        if set:
                            moves += 1
                        selected_piece = None
                        drop_pos = None

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL2))
                        menu1.selected_option = None
                        menu1.isOpen = True
        
        screen.fill((0, 0, 0))
        if menu1.isOpen:
            menu1.draw(screen)
        elif menu2.isOpen:
            menu2.draw(screen)
        elif menu3.isOpen:
            menu3.draw(screen)
        elif mode == "UserLvl1" or mode == "UserLvl2" or mode == "Goal":
            if board.goal_state():
                if mode != "Goal": score = int(((500-moves)+(500-(time.time()-start_time)*20))) if score >= 0 else 0
                board.draw_Goal(screen,True,score)
                mode = "Goal"
            elif (mode == "UserLvl1" and (moves > 10 or time.time()-start_time > 30) or
                  mode == "UserLvl2" and (moves > 30 or time.time()-start_time > 80)):
                board.draw_Goal(screen,False)
            else:
                board.draw(screen, moves, start_time)
                board.draw_pieces(screen, font, selected_piece)
                piece, x, y = board.get_square_under_mouse()
                board.draw_selector(screen, piece)
                drop_pos = board.draw_drag(screen, font, selected_piece)
        else:
            draw_string(screen,"Press 'Esc' to access the menu",TILESIZE//4)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()