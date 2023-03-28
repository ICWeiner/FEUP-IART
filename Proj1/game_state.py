from copy import deepcopy
from os import sys

class GameState:

    def __init__(self, board, move_history = [], depth = 0, start_pos=(0,0), cost_so_far=0): #start_pos should match coordinates of an actual piece or else 💀
        self.board = deepcopy(board)
        self.depth = depth
        #self.move_history = [] + move_history + [deepcopy(self.board)]
        self.move_history = [] + move_history
        self.cost_so_far = cost_so_far
        self.start_pos = start_pos
        self.id = id(self)
   

    def manhattan_distance_heuristic(self):
        # Find the nearest unconnected piece of the same color 
        nearest_dist = float('inf')
        for j in range(self.board.cols):
            for i in range(self.board.rows):
                piece = self.board.get_square(j,i)
                if piece is not None and not piece.connected:
                    dist = abs(i - piece.y) + abs(j - piece.x)
                    print(dist)
                    if dist < nearest_dist:
                        nearest_dist = dist
        print(nearest_dist)
        sys.exit()
        return nearest_dist
    

    def disconnected_squares_heuristic(state):
        board = state.board
        goal_state = board.goal_state()
        if state == goal_state:
            return 0
        
        num_disconnected_squares = 0
        total_distance = 0
        
        for row in range(board.size):
            for col in range(board.size):
                piece = board.get_square(row, col)
                if not piece:
                    continue
                if piece.color != goal_state.board.get_square(row, col).color:
                    num_disconnected_squares += 1
                    total_distance += state.manhattan_distance((row, col), goal_state.get_color_goal(piece.color))
                    
        return num_disconnected_squares * board.size + total_distance
    

    def get_cost_so_far(self, pos):
        return self.cost_so_far.get(pos, float('inf'))  # Return infinity if pos has not been visited yet

    def set_cost_so_far(self, pos, cost):
        self.cost_so_far[pos] = cost

    def __lt__(self, other):
        return self.cost_so_far < other.cost_so_far

    def __eq__(self, other):
        return self.board == other.board and self.start_pos == other.start_pos
    
    def __hash__(self):
        return hash((self.board, self.start_pos))
    
    def __str__(self):
        return self.board


    def children(self):
        functions = [self.moveUp, self.moveDown, self.moveLeft, self.moveRight]
        children = []
        for func in functions:
            child = func()
            if child is not None:
                child.depth = self.depth + 1
                children.append(child)
        return children
    

    def find_pieces(self):
        pieces = []
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece = self.board.get_square(y,x)
                if piece:
                    coords = (piece.x,piece.y)
                    pieces.append(coords)
        return pieces
    
    
    def move(func):
        def wrapper(self):
            pieces = self.find_pieces()
            for piece_coords in pieces:
                state = GameState(self.board, self.move_history, self.depth+1, piece_coords)
                move_made = func(state)
                if move_made:
                    return state
            return None
        return wrapper
    

    #Operators
    @move
    def moveUp(self):
        selected_piece = self.board.get_square(self.start_pos[1],self.start_pos[0])
        if not selected_piece: return False
        x, y = self.start_pos
        moved = self.board.set_position((x, y-1), (selected_piece,x,y))
        if moved:
            self.start_pos = (self.start_pos[0],self.start_pos[1] - 1)
            self.move_history.append(deepcopy(self.board))
        print("Up " + str(moved))
        return moved


    @move
    def moveDown(self):
        selected_piece = self.board.get_square(self.start_pos[1],self.start_pos[0])
        if not selected_piece: return False
        x, y = self.start_pos
        moved = self.board.set_position((x, y+1), (selected_piece,x, y))
        if moved:
            self.start_pos = (self.start_pos[0],self.start_pos[1] + 1)
            self.move_history.append(deepcopy(self.board))
        print("Down " + str(moved))
        return moved


    @move
    def moveLeft(self):
        selected_piece = self.board.get_square(self.start_pos[1],self.start_pos[0])
        if not selected_piece: return False
        x, y = self.start_pos
        moved = self.board.set_position((x - 1, y), (selected_piece,x,y))
        if moved:
            self.start_pos = (self.start_pos[0] - 1,self.start_pos[1])
            self.move_history.append(deepcopy(self.board))
        print("Left " + str(moved))
        return moved


    @move
    def moveRight(self):
        selected_piece = self.board.get_square(self.start_pos[1],self.start_pos[0])
        if not selected_piece: return False
        x, y = self.start_pos
        moved = self.board.set_position((x+1, y), (selected_piece,x, y))
        if moved:
            self.start_pos = (self.start_pos[0] + 1,self.start_pos[1])
            self.move_history.append(deepcopy(self.board))
        print("Right " + str(moved))
        return moved
