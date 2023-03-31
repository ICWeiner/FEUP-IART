import pygame
from board import Board
from game_state import GameState
from queue import PriorityQueue
from menu import Menu
from macros import *
import time

# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀      💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀🪟      💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀        💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀  💀  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
# 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀

def bfs(initial_state):
    queue = [initial_state]
    visited = set() # to avoid visit the same state twice

    while queue:
        print("queue size " + str(len(queue)))
        state = queue.pop(0)    # get the first state from the queue
        visited.add(state)  # add the state to the visited set
        if state.board.goal_state():
            return state.move_history

        for child in state.children():
            if child not in visited:
                #print(child.board)
                queue.append(child) # add the child state to the queue
    return None 

def dfs(initial_state):
    stack = [initial_state]
    visited = set()

    while stack:
        print("stack size " + str(len(stack)))
        state = stack.pop()
        visited.add(state)
        if state.board.goal_state():
            return state.move_history

        for child in reversed(state.children()):  # traverse children in reverse order
            if child not in visited:
                stack.append(child)

    return None



def greedy_search(initial_state):
    queue = PriorityQueue()
    queue.put((initial_state.manhattan_distance_heuristic(), initial_state))
    came_from = {}
    while not queue.empty():
        state = queue.get()[1]
        if state.board.goal_state():
            return state.move_history
        for child in state.children():
            if child.id not in came_from:
                priority = child.manhattan_distance_heuristic()
                queue.put((priority, child))
                came_from[child.id] = state
    return came_from


def a_star_search(initial_state):
    queue = PriorityQueue()
    queue.put((initial_state.manhattan_distance_heuristic(),initial_state))
    came_from = {}
    cost_so_far = {}
    cost_so_far[initial_state.id] = 0  # Set cost of initial state to zero
    while not queue.empty():
        state = queue.get()[1]
        print(type(state))

        if state.board.goal_state():
            return state.move_history

        for child in state.children():
            new_cost = cost_so_far[state.id] + 1
            if child.id not in cost_so_far or new_cost < cost_so_far[child.id]:
                cost_so_far[child.id] = new_cost
                priority = new_cost + child.manhattan_distance_heuristic()
                queue.put((priority,child))
                came_from[child.id] = state
    return came_from, cost_so_far


def delay(milliseconds):
    # Wait for the given time period, but handling some events
    now = pygame.time.get_ticks() # zero point
    delay = now + milliseconds # finish time

    while now < delay:
        for e in pygame.event.get():
            if (e.type == pygame.QUIT):
                # re-post this to handle in the main loop
                pygame.event.post(pygame.event.Event(pygame.QUIT))      
                return

        pygame.display.update()
        pygame.time.wait(300) # save some CPU for a split-second
        now = pygame.time.get_ticks() 


def next_step():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # re-post this to handle in the main loop
                pygame.event.post(pygame.event.Event(pygame.QUIT))      
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    return


def pc_play(sequence, screen, font):
    if sequence:
        count = 1
        for history in sequence:
            screen.fill((0, 0, 0))
            history.draw(screen, count)
            history.draw_pieces(screen, font)
            pygame.display.flip()
            count += 1
            delay(1000)
            #next_step()
    else:
        print("No solution found")


def print_sequence(sequence):
    if sequence:
        print("Solved in :" + str(len(sequence)) + " moves")
        #print("Steps:", len(sequence))
        #print()
        #for state in sequence:
        #    print(state)
        #    print()
    else:
        print("No solution found")


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
                    board = Board(LVL1_ROWS,LVL1_COLS)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1))
                    s1 = pygame.font.SysFont('Arial',TILESIZE//2).render("Loading..." , True, pygame.Color('white'))
                    s1_rect = s1.get_rect()
                    s1_rect.center = screen.get_rect().center
                    screen.blit(s1, s1_rect)
                    pygame.display.update()
                    if menu.selected_option == 0:
                        sequence = bfs(GameState(board))
                    elif menu.selected_option == 1:
                        sequence = dfs(GameState(board))
                    elif menu.selected_option == 2:
                        sequence = a_star_search(GameState(board))
                    else:
                        sequence = greedy_search(GameState(board))
                    pc_play(sequence,screen,font)
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