import pygame
import heapq
from queue import PriorityQueue
from macros import TILESIZE
from os import sys
import time
from memory_profiler import profile

class PCPlay: #class responsible for showcasing the solution for the various algorithms

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.selected_option = None


    #@profile
    def bfs(self):
        print("BFS")
        queue = [self.initial_state]
        visited = set() # to avoid visiting the same state twice
        start_time = time.time()
        while queue:
            #print("queue size " + str(len(queue)))
            state = queue.pop(0)    # get the first state from the queue
            visited.add(state)  # add the state to the visited set
            if state.board.goal_state():
                print(time.time()-start_time)
                return state.move_history

            for child in state.children():
                if child not in visited:
                    #print(child.board)
                    queue.append(child) # add the child state to the queue
        return None 


    #@profile
    def dfs(self):
        print("DFS")
        stack = [self.initial_state]
        visited = set()
        start_time = time.time()
        while stack:
            #print("stack size " + str(len(stack)))
            state = stack.pop(0)
            visited.add(state)
            if state.board.goal_state():
                print(time.time()-start_time)
                return state.move_history

            for child in reversed(state.children()):  # traverse children in reverse order
                if child not in visited:
                    stack.append(child)
        return None


    #@profile
    def iterative_deepening_search(self):
        def depth_limited_search(state, depth):
            if state.board.goal_state():
                return state.move_history
            if depth == 0:
                return None
            for child in state.children():
                result = depth_limited_search(child, depth-1)
                if result is not None:
                    return result
            return None

        print("Iterative Deepening")
        start_time = time.time()
        max_depth = 10 # max depth to search
        for depth in range(1, max_depth+1):
            result = depth_limited_search(self.initial_state, depth)
            if result is not None:
                print(time.time()-start_time)
                return result
        return None


    #@profile
    def uniform_cost_search(self):
        print("Uniform Cost")
        queue = [(0, self.initial_state)]
        visited = set()
        start_time = time.time()
        while queue:
            priority, state = heapq.heappop(queue)
            if state.board.goal_state():
                print(time.time()-start_time)
                return state.move_history
            visited.add(state.id)
            for child in state.children():
                if child.id not in visited:
                    child_priority = priority + child.cost_so_far
                    heapq.heappush(queue, (child_priority, child))
        return None


    @profile
    def greedy_search(self, heuristic="manhattan"): #for heuristic write manhattan or colors
        print("Greedy with " + heuristic + " heuristic")
        queue = PriorityQueue()

        if heuristic == "color":
            queue.put((self.initial_state.color_clusters_heuristic(), self.initial_state))
        else:
            queue.put((self.initial_state.manhattan_distance_heuristic(), self.initial_state))
        
        came_from = {}
        start_time = time.time()
        while not queue.empty():
            state = queue.get()[1]
            if state.board.goal_state():
                print(time.time()-start_time)
                return state.move_history
            for child in state.children():
                if child.id not in came_from:
                    if heuristic == "color":
                        priority = child.color_clusters_heuristic()
                    else:
                        priority = child.manhattan_distance_heuristic()
                    queue.put((priority, child))
                    came_from[child.id] = state
        return came_from


    @profile
    def a_star_search(self, heuristic="manhattan"):
        print("A* with " + heuristic + " heuristic")
        queue = PriorityQueue()

        if heuristic == "color":
            queue.put((self.initial_state.color_clusters_heuristic(), self.initial_state))
        else:
            queue.put((self.initial_state.manhattan_distance_heuristic(),self.initial_state))

        came_from = {}
        cost_so_far = {}
        cost_so_far[self.initial_state.id] = 0  # Set cost of initial state to zero
        start_time = time.time()
        while not queue.empty():
            state = queue.get()[1]
            #print(type(state))

            if state.board.goal_state():
                print(time.time()-start_time)
                return state.move_history

            for child in state.children():
                new_cost = cost_so_far[state.id] + 1
                if child.id not in cost_so_far or new_cost < cost_so_far[child.id]:
                    cost_so_far[child.id] = new_cost
                    if heuristic == "color":
                        priority = new_cost + child.color_clusters_heuristic()
                    else:
                        priority = new_cost + child.manhattan_distance_heuristic()
                    queue.put((priority,child))
                    came_from[child.id] = state
        return came_from, cost_so_far


    def next_step(self,screen):
        # Draw buttons
        button1_rect = pygame.Rect((screen.get_width()-70, screen.get_height()-60, 50, 25))
        #button2_rect = pygame.draw.rect(screen, (255, 0, 0), (screen.get_width()-50-10, screen.get_height()-25-10, 50, 25))
        button_surf = pygame.Surface(button1_rect.size)
        button_surf.fill(pygame.Color('darkgrey'))
        text_surf = pygame.font.SysFont('Arial',16).render("Next", True, pygame.Color('black'))
        text_pos = text_surf.get_rect(center=button_surf.get_rect().center)
        button_surf.blit(text_surf, text_pos)
        screen.blit(button_surf, button1_rect)
        pygame.display.flip()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(pygame.mouse.get_pos()):
                        #print("Button 1 clicked!")
                        self.selected_option = 0
                    #elif button2_rect.collidepoint(pygame.mouse.get_pos()):
                        #print("Button 2 clicked!")

                if e.type == pygame.MOUSEBUTTONUP:
                        if self.selected_option is not None:
                            self.selected_option = None
                            return
            

    def draw(self, sequence, screen, font):
        if sequence:
            count = 0
            for history in sequence:
                screen.fill((0, 0, 0))
                history.draw(screen, count)
                history.draw_pieces(screen, font)
                pygame.display.flip()
                count += 1
                self.next_step(screen)
                #self.delay(1000)
        else:
            print("No solution found")

    
    def print_sequence(sequence):
        if sequence:
            print("Solved in :" + str(len(sequence)-1) + " moves")
            #print("Steps:", len(sequence))
            #print()
            #for state in sequence:
            #    print(state)
            #    print()
        else:
            print("No solution found")