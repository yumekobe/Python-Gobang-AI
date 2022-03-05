from constants import *
class Board:
    def __init__(self,data):
        self.data = data
        for i in range(BLOCKS):
            self.data.append([-1])
        for i in range(1,BLOCKS):
            self.data[0].append(-1)
        for i in range(1,BLOCKS):
            for j in range(1,BLOCKS):
                self.data[i].append(0)
    
    def place_piece(self,piece_type:int,position_i,position_j):
        self.data[position_i][position_j] = piece_type