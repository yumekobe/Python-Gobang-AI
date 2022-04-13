from constants import *
P1_TYPE = 1
P2_TYPE = 2
class Board:
    def __init__(self,data):
        if len(data) == 0:
            self.data = data
            for i in range(BLOCKS):
                self.data.append([-1])
            for i in range(1,BLOCKS):
                self.data[0].append(-1)
            for i in range(1,BLOCKS):
                for j in range(1,BLOCKS):
                    self.data[i].append(0)
        else:
            self.data = data
    
    def place_piece(self,piece_type:int,position_i,position_j):
        self.data[position_i][position_j] = piece_type
    
    def copy(self):
        res = Board(self.data)
        return res
    
    
                