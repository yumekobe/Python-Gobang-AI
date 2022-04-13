from constants import *
from board import *

class AIplayer():
    def __init__(self):
        self.record = [[[0,0,0,0] for x in range(BLOCKS)] for y in range(BLOCKS)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
    def step_gen(self,board:Board,turn)->list:   #生成当前合理落子位置
        S_AREA = 1
        steps = []
        for i in range(1,BLOCKS):
            for j in range(1,BLOCKS):
                if board.data[i][j] != 0:
                    continue
                else:
                    if i > S_AREA:
                        lef_i = S_AREA
                    else:
                        lef_i = i - 1
                    if j > S_AREA:
                        lef_j = S_AREA
                    else:
                        lef_j = j - 1
                    if i + S_AREA < BLOCKS:
                        rig_i = S_AREA
                    else:
                        rig_i = BLOCKS - 1 - i
                    if j + S_AREA < BLOCKS:
                        rig_j = S_AREA
                    else:
                        rig_j = BLOCKS - 1 - j
                    for i1 in range(i - lef_i, i + rig_i + 1):
                        temmsg = False
                        for j1 in range(j - lef_j, j + rig_j + 1):
                            if board.data[i1][j1] != 0:
                                board.data[i][j] = turn + 1
                                #score = self.evaluate(board,turn)
                                #steps.append((score,j,i))
                                steps.append((j,i))
                                board.data[i][j] = 0
                                tempmsg = True
                                break
                        if temmsg:
                            break
        if len(steps) == 0:
            centre = (BLOCKS//2,BLOCKS//2)
            steps.append(centre)
        steps.sort(reverse=True)
        return set(steps)


    def step_gen2(self,board:Board):
        steps = []
        for i in range(1,16):
            for j in range(1,16):
                if board.data[i][j] == 0:
                    steps.append((i,j))
        return steps


    def minmax(self,board:Board,turn,depth,alpha = -Infinity,beta = Infinity):
        score = self.evaluate(board,turn)
        if depth <= 0 or score == Infinity or -score == Infinity:
            return score
        
        steps = self.step_gen(board,turn)
        best = None

        for x,y in steps:
            board.data[y][x] = turn + 1
            if turn + 1 == P1_TYPE:
                oppo_turn = P2_TYPE - 1
            else:
                oppo_turn = P1_TYPE - 1
            score = -self.minmax(board,oppo_turn,depth -1,-beta,-alpha)

            board.data[y][x] = 0
            if score > alpha:
                alpha = score
                best = (x,y)
                if alpha >= beta:
                    break
        if depth == AI_DEPTH and best != None:
            self.best = best
        
        return alpha
    
    def aimove(self,board:Board,turn):
        self.best = None
        score = self.minmax(board,turn,AI_DEPTH)
        x = self.best[0]
        y = self.best[1]
        return (y,x)

        pass
    def reset(self):
        for y in range(BLOCKS):
            for x in range(BLOCKS):
                for dir_index in range(4):
                    self.record[y][x][dir_index] = 0
        for dir_index in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[dir_index][j] = 0
        
    def evaluate(self,board:Board,turn):
        self.reset()
        if turn == 0:
            mine = 1
            opponent = 2
        elif turn == 1:
            mine = 2
            opponent = 1
        
        for y in range(1,16):
            for x in range(1,16):
                if board.data[y][x] == mine:
                    self.evaluatePoint(board,x,y,mine,opponent)
                elif board.data[y][x] == opponent:
                    self.evaluatePoint(board,x,y,opponent,mine)
        
        mine_count = self.count[mine-1]
        oppo_count = self.count[opponent - 1]
        minescore, opposcore = self.getScore(mine_count, oppo_count)
        return minescore-opposcore
    
    def evaluatePoint(self,board:Board,x,y,mine,opponent):
        victors = [(1,0),(0,1),(1,1),(1,-1)]
        for dir_index in range(4):
            if self.record[y][x][dir_index] == 0:
                self.analyseLine(board,x,y,dir_index,victors[dir_index],mine,opponent,self.count[mine-1])

    def getLine(self,board:Board,x, y, victor, mine, opponent):
        line = []
        for i in range(9):
            line.append(0)
        x_now = x - 5 * victor[0]
        y_now = y - 5 * victor[1]
        for i in range(9):
            x_now += victor[0]
            y_now += victor[1]
            if x_now not in range(1,16) or y_now not in range(1,16):
                line[i] = opponent
            else:
                line[i] = board.data[y_now][x_now]
        return line
    
    def dRecord(self, x, y, left, right, dir_index, victor):
        x_now = x + (-5 + left)*victor[0]
        y_now = y + (-5 + left)*victor[1]
        for k in range(left,right+1):
            x_now += victor[0]
            y_now += victor[1]
            self.record[y_now][x_now][dir_index] = 1
                
    def analyseLine(self,board:Board,x,y,dir_index,victor,mine,opponent,count):
        left_mine = 4
        right_mine = 4
        line = self.getLine(board,x,y,victor,mine,opponent)
        line_str = ''
        for num in line:
            if num == 0:
                line_str += 'E' #E for empty
            elif num == mine:
                line_str += 'M' #M for mine
            elif num == opponent:
                line_str += 'P'
        while left_mine > 0:
            if line[left_mine-1] != mine:
                break
            else:
                left_mine -= 1
        while right_mine < 8:
            if line[right_mine+1] != mine:
                break
            else:
                right_mine += 1
        mine_range = right_mine - left_mine + 1

        left_me = left_mine
        right_me = right_mine
        while right_me < 8:
            if line[right_me + 1] == opponent:
                break
            right_me += 1
        while left_me > 0:
            if line[left_me - 1] == opponent:
                break
            left_me -= 1
        me_range = right_me - left_me + 1
        if me_range <= 4:
            self.dRecord(x,y,left_me,right_me,dir_index,victor)
            return None
        
        self.dRecord(x,y,left_mine,right_mine,dir_index,victor)


        if mine_range == 4:
            if line_str.find('EMMMME') != -1:
                count[FOUR] += 1
            elif line_str.find('EMMMMP') != -1 or line_str.find('PMMMME') != -1:
                count[SFOUR] += 1

        # Chong Four : MXMMM, MMMXM, the two types can both exist
		# Live Three : XMMMXX, XXMMMX
		# Sleep Three : PMMMX, XMMMP, PXMMMXP        
        elif mine_range == 3:
            if line_str.find('MEMMM') != -1:
                self.dRecord(x,y,left_mine - 2, left_mine - 1, dir_index,victor)
                count[SFOUR]+= 1
            if line_str.find('MMMEM') != -1:
                self.dRecord(x, y, right_mine+1, right_mine+2, dir_index, victor)
                count[SFOUR]+= 1
            elif line_str.find('EMMMEE') != -1 or line_str.find('EEMMME') != -1:
                count[THREE] += 1
            elif line_str.find('PEMMMEP')!= -1:
                count[STHREE] += 1
            elif line_str.find('PMMME') != -1 or line_str.find('EMMMP') != -1:
                count[STHREE] += 1
            
        # Chong Four: MMXMM, only check right direction
		# Live Three: XMXMMX, XMMXMX the two types can both exist
		# Sleep Three: PMXMMX, XMXMMP, PMMXMX, XMMXMP
		# Live Two: XMMX
		# Sleep Two: PMMX, XMMP
        elif mine_range == 2:
            if line_str[left_mine:].find('MMEMM') != -1:
                #self.dRecord(x, y, right_mine+1, right_mine+2, dir_index, victor)
                count[SFOUR] += 1
            if line_str.find('EMEMME') != -1:
                self.dRecord(x, y, left_mine-2, left_mine-1, dir_index, victor)
                count[THREE] += 1
            if line_str.find('EMMEME') != -1:
                count[THREE] += 1
            elif line_str.find('PMEMME') != -1:
                self.dRecord(x, y, left_mine-2, left_mine-1, dir_index, victor)
                count[STHREE] += 1
            elif line_str.find('EMEMMP') != -1:
                self.dRecord(x, y, left_mine-2, left_mine-1, dir_index, victor)
                count[STHREE] += 1
            elif line_str.find('PMMEME') != -1:
                self.dRecord(x, y, right_mine+1, right_mine+2, dir_index, victor)
                count[STHREE] += 1
            elif line_str.find('EMMEMP') != -1:
                self.dRecord(x, y, right_mine+1, right_mine+2, dir_index, victor)
                count[STHREE] += 1
            elif line_str.find('EMME') != -1:
                count[TWO] += 1
            elif line_str.find('PMME') != -1:
                count[STWO] += 1
            elif line_str.find('EMMP') != -1:
                count[STWO] += 1
        # Live Two: XMXMX, XMXXMX only check right direction
		# Sleep Two: PMXMX, XMXMP
        elif mine_range == 1:
            if line_str[left_mine:].find('EMEME') != -1:
                self.dRecord(x, y, right_mine, right_mine+2, dir_index, victor)
                count[TWO] += 1
            elif line_str.find('PMEME') != -1:
                self.dRecord(x, y, right_mine, right_mine+2, dir_index, victor)
                count[STWO] += 1
            elif line_str[left_mine:].find('EMEEME') != -1:
                count[TWO] += 1
            elif line_str.find('EMEMP') != -1:
                count[STWO] +=1
                pass

        elif mine_range == 5:
            count[FIVE] += 1
                

    def getScore(self, mine_count, opponent_count):
        minescore, opposcore = 0, 0
        if mine_count[FIVE] > 0:
            return (Infinity, 0)
        if opponent_count[FIVE] > 0:
            return (0, Infinity)
                
        if mine_count[SFOUR] >= 2:
            mine_count[FOUR] += 1
            
        if opponent_count[FOUR] > 0:
            return (0, 9050)
        if opponent_count[SFOUR] > 0:
            return (0, 9040)

        if mine_count[FOUR] > 0:
            return (9030, 0)
        if mine_count[SFOUR] > 0 and mine_count[THREE] > 0:
            return (9020, 0)
            
        if opponent_count[THREE] > 0 and mine_count[SFOUR] == 0:
            return (0, 9010)
            
        if (mine_count[THREE] > 1 and opponent_count[THREE] == 0 and opponent_count[STHREE] == 0):
            return (9000, 0)

        if mine_count[SFOUR] > 0:
            minescore += 2000

        if mine_count[THREE] > 1:
            minescore += 500
        elif mine_count[THREE] > 0:
            minescore += 100
            
        if opponent_count[THREE] > 1:
            opposcore += 2000
        elif opponent_count[THREE] > 0:
            opposcore += 400

        if mine_count[STHREE] > 0:
            minescore += mine_count[STHREE] * 10
        if opponent_count[STHREE] > 0:
            opposcore += opponent_count[STHREE] * 10
            
        if mine_count[TWO] > 0:
            minescore += mine_count[TWO] * 4
        if opponent_count[TWO] > 0:
            opposcore += opponent_count[TWO] * 4
                
        if mine_count[STWO] > 0:
            minescore += mine_count[STWO] * 4
        if opponent_count[STWO] > 0:
            opposcore += opponent_count[STWO] * 4

        return (minescore, opposcore)