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
    visited = set() # to not visit the same state twice

    while queue:
        print("queue size " + str(len(queue)))
        state = queue.pop(0)    # get the first state from the queue
        visited.add(state)  # add the state to the visited set
        if state.board.goal_state():
            return state.move_history

        for child in state.children():
            if child not in visited:
                #print(child.board)
                # add the child state to the queue
                queue.append(child)
            #else:
                #print("HELLO1")
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


def pc_play(sequence, screen, font):
    if sequence:
        count = 1
        for history in sequence:
            screen.fill((0, 0, 0))
            history.draw(screen, count)
            history.draw_pieces(screen, font)
            pygame.display.flip()
            pygame.time.delay(1000)
            count += 1
        history.draw_Goal(screen,True)
        pygame.display.flip()

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
    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
    menu = Menu(SCREEN_SIZE_LVL1)

    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

            if menu.isOpen:
                selected_option = menu.handle_events(events)
                if selected_option == 0 or selected_option == 1:
                    board = Board(LVL1_ROWS,LVL1_COLS)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
                    s1 = pygame.font.SysFont('Arial',TILESIZE//2).render("Loading..." , True, pygame.Color('white'))
                    s1_rect = s1.get_rect()
                    s1_rect.center = screen.get_rect().center
                    screen.blit(s1, s1_rect)
                    pygame.display.update()
                    sequence = bfs(GameState(board)) if selected_option == 0 else a_star_search(GameState(board))
                    pc_play(sequence,screen,font)

                elif selected_option == 2 or selected_option == 3:
                    board = Board(LVL1_ROWS,LVL1_COLS) if selected_option == 2 else Board(LVL2_ROWS,LVL2_COLS)
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1])) if selected_option == 2 else pygame.display.set_mode((SCREEN_SIZE_LVL2[0], SCREEN_SIZE_LVL2[1]))
                    selected_piece = None
                    drop_pos = None
                    count = 0
                    start_time = time.time()
                    menu.isOpen = False

                elif selected_option == 4:
                    return
                selected_option = None

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
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
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
            piece, x, y = board.get_square_under_mouse()
            board.draw_pieces(screen, font, selected_piece)
            board.draw_selector(screen, piece)
            drop_pos = board.draw_drag(screen, font, selected_piece)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()