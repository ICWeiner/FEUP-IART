from board import Board
from copy import deepcopy

class GameState:

    def __init__(self, board, move_history = []):
        self.board = deepcopy(board)
        self.selected_piece = self.find_piece()
        self.x = self.selected_piece[1]
        self.y = self.selected_piece[2]
        #self.move_history = [] + move_history + [deepcopy(self.board)]
        self.move_history = [] + move_history



    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash((str(self.board)))
    

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
                            children.append(child)
                self.selected_piece , self.x ,self.y = (None,None,None)
        #print("hello")
        #print(len(children))
        return children

    

    def find_piece(self):
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece = self.board.get_square(y,x)
                if piece:
                    if len(piece.get_connected_pieces(self.board)) < self.board.pieces[piece.color]:
                        return (self.board.get_square(y,x),x,y)
        return (None,None,None)
    

    def move(func):
        def wrapper(self):
            state = GameState(self.board, self.move_history)
            move_made = func(state)
            if move_made:
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
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved up" )
            self.y -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Up " + str(moved))
        return moved


    @move
    def moveDown(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x, self.y+1), self.selected_piece)
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved down" )
            self.y += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Down " + str(moved))
        return moved


    @move
    def moveLeft(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x-1, self.y), self.selected_piece)
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved left" )
            self.x -= 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Left " + str(moved))
        return moved


    @move
    def moveRight(self):
        if not self.selected_piece[0]: return False
        moved = self.board.set_position((self.x+1, self.y), self.selected_piece)
        if moved:
            self.move_history.append("Piece at coordinates x:" + str(self.x) + " y:" + str(self.y) +" moved right" )
            self.x += 1
            self.selected_piece = (self.board.get_square(self.y,self.x),self.x,self.y)
        #print("Right " + str(moved))
        return moved
    
    
