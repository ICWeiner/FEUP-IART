from board import Board
from copy import deepcopy

class GameState:

    def __init__(self, board, move_history=[]):
        self.board = deepcopy(board)
        self.piece = self.board.get_square(0,0)
        self.x = 0
        self.y = 0
        self.selected_piece = (self.piece, self.x, self.y)
        self.move_history = [] + move_history + [deepcopy(self.board)]


    def __eq__(self, other):
        return self.board == other.board


    def __hash__(self):
        return hash((str(self.board)))
    

    def children(self):
        functions = [self.moveUp, self.moveDown, self.moveLeft, self.moveRight]
        children = []
        for func in functions:
            child = func()
            if child:
                children.append(child)
        return children


    def move(func):
        def wrapper(self):
            state = GameState(self.board, self.move_history)
            move_made = func(state)
            if move_made:
                state.move_history.append(move_made)
                return state
            else:
                return None
        return wrapper
    

    #Operators
    @move
    def moveUp(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x, self.y-1), self.selected_piece)
        if moved:
            self.y -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        print("Up " + str(moved))
        return moved


    @move
    def moveDown(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x, self.y+1), self.selected_piece)
        if moved:
            self.y += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        print("Down " + str(moved))
        return moved


    @move
    def moveLeft(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x+1, self.y), self.selected_piece)
        if moved:
            self.x += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        print("Left " + str(moved))
        return moved


    @move
    def moveRight(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x-1, self.y), self.selected_piece)
        if moved:
            self.x -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        print("Right " + str(moved))
        return moved


    #TODO Colocar goal_state function aqui
    # ...


    
