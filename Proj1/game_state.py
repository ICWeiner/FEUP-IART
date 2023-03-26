from board import Board
from copy import deepcopy
from os import sys

class GameState:

    def __init__(self, board, move_history = [],depth = 0,start_pos=(0,0)): #start_pos should match coordinates of an actual piece or else 💀
        self.board = deepcopy(board)
        self.selected_piece = self.find_piece()
        self.depth = depth
        self.x = self.selected_piece.x
        self.y = self.selected_piece.y
        #self.move_history = [] + move_history + [deepcopy(self.board)]
        self.move_history = [] + move_history
        self.start_pos = start_pos
        self.cost_so_far = {start_pos: 0}

    def manhattan_distance_heuristic(self):
    # Find the nearest unconnected piece of the same color and shape
        nearest_dist = float('inf')
        for j in range(self.board.cols):
            for i in range(self.board.rows):
                if self.board.board[i][j] is not None and self.board.board[i][j].color == self.selected_piece.color and not self.board.board[i][j].connected:
                    dist = abs(i - self.board.board[i][j].row) + abs(j - self.board.board[i][j].col)
                    if dist < nearest_dist:
                        nearest_dist = dist
        return nearest_dist
    
    def get_cost_so_far(self, pos):
        return self.cost_so_far.get(pos, float('inf'))  # Return infinity if pos has not been visited yet

    def set_cost_so_far(self, pos, cost):
        self.cost_so_far[pos] = cost


    def __eq__(self, other):
        return isinstance(other, GameState) and self.board == other.board and self.selected_piece == other.selected_piece
    
    def __hash__(self):
        return hash((self.board, self.selected_piece))
    
    def __str__(self):
        return self.board

    def children(self):
        functions = [self.moveUp, self.moveDown, self.moveLeft, self.moveRight]
        children = []
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                self.selected_piece = self.board.get_square(y,x)
                if self.selected_piece:
                    self.x = self.selected_piece.x
                    self.y = self.selected_piece.y
                    for func in functions:
                        child = func()
                        if child:#TODO: Verificar se movimento é possivel
                            child.selected_piece = self.selected_piece
                            child.x = self.selected_piece.x
                            child.y = self.selected_piece.y
                            #child.depth+=1
                            children.append(child)
                self.selected_piece , self.x ,self.y = (None,None,None)
        #print("hello")
        print("current node has " + str(len(children)) + " children")
        print(str(self.depth) + " depth")
        #for child in children:
            #print(child.selected_piece)
        #sys.exit()
        return children

    

    def find_piece(self):
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece = self.board.get_square(y,x)
                if piece:
                    if len(piece.get_connected_pieces(self.board)) < self.board.pieces[piece.color]:
                        return self.board.get_square(y,x)
        return None
    

    def move(func):
        def wrapper(self):
            exp_state = GameState(self.board, self.move_history,self.depth +1)
            move_made = func(exp_state)
            if move_made:
                new_state = GameState(self.board, self.move_history,self.depth +1, (exp_state.x, exp_state.y))
                move_made = func(new_state)
                return new_state
            else:
                return None
        return wrapper
    

    #Operators
    @move
    def moveUp(self):
        if not self.selected_piece: return False
        moved = self.board.set_position((self.x, self.y-1), (self.selected_piece,self.x, self.y))
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved up" )
            self.y -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Up " + str(moved))
        return moved


    @move
    def moveDown(self):
        if not self.selected_piece: return False
        moved = self.board.set_position((self.x, self.y+1), (self.selected_piece,self.x, self.y))
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved down" )
            self.y += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Down " + str(moved))
        return moved


    @move
    def moveLeft(self):
        if not self.selected_piece: return False
        moved = self.board.set_position((self.x-1, self.y), (self.selected_piece,self.x, self.y))
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved left" )
            self.x -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Left " + str(moved))
        return moved


    @move
    def moveRight(self):
        if not self.selected_piece: return False
        moved = self.board.set_position((self.x+1, self.y), (self.selected_piece,self.x, self.y))
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved right" )
            self.x += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Right " + str(moved))
        return moved
    
    
