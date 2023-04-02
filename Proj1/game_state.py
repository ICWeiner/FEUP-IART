from copy import deepcopy
from itertools import combinations

class GameState: #class that represents a game state and its various properties

    def __init__(self, board, move_history = [], depth = 0, start_pos=(0,0), cost_so_far=0): #start_pos should match coordinates of an actual piece or else 💀
        self.board = deepcopy(board)
        self.depth = depth #depth of current node, equals number of moves made in this particular state
        if (depth == 0):
            self.move_history = [] + move_history + [deepcopy(self.board)]#add first state to history
        else:
            self.move_history = [] + move_history
        self.cost_so_far = cost_so_far
        self.start_pos = start_pos
        self.id = id(self)
   
   
    def manhattan_distance_heuristic(self): #calculates the total manhattan distance pieces of the same colour and ads them all
        distances = []
        colors = ['red', 'green', 'yellow', 'blue']
        for color in colors:
            color_pieces = [piece for row in self.board.board for piece in row if piece and piece.color == color]
            connected_pieces = set()
            distance = 0

            while color_pieces:
                piece = color_pieces.pop()
                if piece not in connected_pieces:
                    connected_pieces |= piece.get_connected_pieces(self.board)
                    for other_piece in color_pieces:
                        if other_piece not in connected_pieces:
                            #distance += abs(piece.x - other_piece.x) + abs(piece.y - other_piece.y)
                            distance += ((piece.x - other_piece.x) ** 2 + (piece.y - other_piece.y) ** 2) ** 0.5
            distances.append(distance)
        
        return sum(distances)   


    def color_clusters_heuristic(self): #calculates the minimum distance between clusters of different colors
        clusters = {}
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece = self.board.get_square(y,x)
                if piece is not None:
                    if piece.color not in clusters:
                        clusters[piece.color] = []
                    clusters[piece.color].append((piece.x, piece.y))

        if len(clusters) < 2:
            return 0

        cost = 0
        for color1, color2 in combinations(clusters.keys(), 2):
            min_distance = float('inf')
            for x1, y1 in clusters[color1]:
                for x2, y2 in clusters[color2]:
                    distance = abs(x1 - x2) + abs(y1 - y2)
                    if distance < min_distance:
                        min_distance = distance
            cost += min_distance

        return cost


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


    def children(self): #generate all legal child states
        functions = [self.moveUp, self.moveDown, self.moveLeft, self.moveRight]
        children = []
        for func in functions:
            child = func()
            if child is not None:
                child.depth = self.depth + 1
                child.cost_so_far = self.cost_so_far + 1 + child.manhattan_distance_heuristic()
                children.append(child)
        return children
    

    def find_pieces(self): #find all pieces on the board
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
        #print("Up " + str(moved))
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
        #print("Down " + str(moved))
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
        #print("Left " + str(moved))
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
        #print("Right " + str(moved))
        return moved
