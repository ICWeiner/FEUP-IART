import pygame
from queue import PriorityQueue
from macros import TILESIZE
from os import sys

class PCPlay:

    def __init__(self, initial_state):
        self.initial_state = initial_state
        #self.buttons = ['Next','Previous']
        #self.selected_option = None


    def bfs(self):
        queue = [self.initial_state]
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


    def dfs(self):
        stack = [self.initial_state]
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


    def greedy_search(self):
        queue = PriorityQueue()
        queue.put((self.initial_state.manhattan_distance_heuristic(), self.initial_state))
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


    def a_star_search(self):
        queue = PriorityQueue()
        queue.put((self.initial_state.manhattan_distance_heuristic(),self.initial_state))
        came_from = {}
        cost_so_far = {}
        cost_so_far[self.initial_state.id] = 0  # Set cost of initial state to zero
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
    

    def draw_loading(self,screen):
        s1 = pygame.font.SysFont('Arial',TILESIZE//2).render("Loading..." , True, pygame.Color('white'))
        s1_rect = s1.get_rect()
        s1_rect.center = screen.get_rect().center
        screen.blit(s1, s1_rect)
        pygame.display.update()


    def delay(self, milliseconds):
        # Wait for the given time period, but handling some events
        now = pygame.time.get_ticks() # zero point
        delay = now + milliseconds # finish time

        while now < delay:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()

            #pygame.display.update()
            pygame.time.wait(300) # save some CPU for a split-second
            now = pygame.time.get_ticks()  


    def next_step():
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    # re-post this to handle in the main loop
                    #pygame.event.post(pygame.event.Event(pygame.QUIT))      
                    #return
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        return
                    

    def draw(self, sequence, screen, font):
        if sequence:
            count = 1
            for history in sequence:
                screen.fill((0, 0, 0))
                history.draw(screen, count)
                history.draw_pieces(screen, font)
                pygame.display.flip()
                count += 1
                #pygame.time.delay(1000)
                self.delay(1000)
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