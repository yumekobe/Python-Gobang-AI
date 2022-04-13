import pygame
import time
from constants import *
from board import *
from graphics import *
from ai import *
def terminate():
    pygame.quit()
    exit()
class Gameplay:
    def player_turn(self,board:Board,is_running:bool):
        x = 0
        y = 0
        pos_i = -1
        pos_j = -1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_running = False
                        terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        pos_j = x // BLOCK_WIDTH
                        pos_i = y // BLOCK_WIDTH
                        if pos_i > 0 and pos_j > 0 and pos_i < BLOCKS and pos_j < BLOCKS:
                            if board.data[pos_i][pos_j] == 0:
                                break
                            else:
                                continue
                        else:
                            continue
            if pos_i > 0 and pos_j > 0 and pos_i < BLOCKS and pos_j < BLOCKS:
                if board.data[pos_i][pos_j] == 0:
                    break
        board.place_piece(self.game_turn + 1,pos_i,pos_j)
        #aitest = AIplayer()
        #scoretest = aitest.evaluate(board,0)
        #print(scoretest)
        #print(self.negamax(board,0,NEG_INF,POS_INF,1))
        #print(self.step_gen(board))
        #testhere = 12
        self.game_turn += 1
        self.game_turn = self.game_turn % 2

    def judge(self,board:Board)->bool:
        for i in range(1,BLOCKS):
            tempmsg = False
            for j in range(1,BLOCKS):
                if board.data[i][j] == 0:
                    tempmsg = True
                    break
            if tempmsg:
                break
            if i == BLOCKS - 1:
                return False
        for i in range(1,BLOCKS):
            for j in range(1,BLOCKS):
                if board.data[i][j] != 0:
                    count = 0
                    #判断列是否满足
                    if i < BLOCKS - 4:
                        for k in range(5):
                            if board.data[i][j] == board.data[i+k][j]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
                    count = 0
                    if j < BLOCKS - 4:
                        for k in range(5):
                            if board.data[i][j] == board.data[i][j+k]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
                    count = 0
                    if i < BLOCKS - 4 and j < BLOCKS - 4:
                        for k in range(5):
                            if board.data[i][j] == board.data[i+k][j+k]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
                    count = 0
                    if  j < BLOCKS - 4 and i > 4:
                        for k in range(5):
                            if board.data[i][j] == board.data[i-k][j+k]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
        return False
        
    def Start(self,screen):
        screen.fill(BOARD_COLOUR)
        tip_str1 = 'Press any key to start'
        tip_str2 = 'Press ESC to quit'
        tip_str3 = 'Press R to restart'
        font = pygame.font.SysFont("Consolas", 30)
        tip = font.render(tip_str1, True, BLACK)  
        tip2 = font.render(tip_str2, True, BLACK)
        tip3 = font.render(tip_str3, True, BLACK)
        screen.blit(tip, (40, SCREEN_HEIGHT/3 + 0)) 
        screen.blit(tip2, (80, SCREEN_HEIGHT/3 + 50))
        screen.blit(tip3, (70, SCREEN_HEIGHT/3 + 100))
        pygame.display.update()
        while True:                                     #键盘监听事件
            for event in pygame.event.get():            #关闭窗口
                if event.type == pygame.QUIT:
                    terminate()   
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):  #按下ESC键
                        terminate()
                    else:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        return
    def choose_p(self,screen):
        screen.fill(BOARD_COLOUR)
        msg1 = 'Press 1 to choose BLACK'
        msg2 = 'Press 2 to choose WHITE'
        font = pygame.font.SysFont("Consolas", 30)
        tip = font.render(msg1, True, BLACK)
        tip2 = font.render(msg2, True, BLACK)
        screen.blit(tip, (40, SCREEN_HEIGHT/3 + 30)) 
        screen.blit(tip2, (40, SCREEN_HEIGHT/3 + 80))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_1) :
                        self.player = 0
                    elif (event.key == pygame.K_2):
                        self.player = 1
                    return
        pass
    def Run(self,screen):
        is_running = True
        draw_board(screen)
        board = Board([])
        #board.data[8][8] = 1 
        #board.data[8][9] = 1 
        #board.data[8][10] = 1 
        #board.data[8][11] = 1  #测试用代码
        #board.data[4][4] = 2     #测试用代码
        game_turn = [0]
        self.game_turn = 0
        draw_pieces(screen,board)
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_running = 0
            if self.game_turn == self.player:
                self.player_turn(board,is_running)
            else:
                self.computer_turn(board,is_running)
            draw_pieces(screen,board)
            
            draw_currencyrent_piece(screen,self.game_turn)
            pygame.display.update()
            time.sleep(0.1)
            if_continue = self.judge(board)
            if if_continue:
                self.Win(screen)
                return
        
    def Win(self,screen):
        screen.fill(BOARD_COLOUR)
        winner = ''
        if self.game_turn == 1:
            winner = 'BLACK'
        elif self.game_turn == 0:
            winner = 'WHITE'
        msg = f'{winner} won the game'
        font = pygame.font.SysFont("Consolas", 30)
        msg1 = font.render(msg, True, BLACK)
        screen.blit(msg1, (75, SCREEN_HEIGHT/3 + 50))  
        pygame.display.update()  
    
    
    
    def computer_turn(self,board:Board,is_running:bool):
        
        com_player = AIplayer()
        pos = com_player.aimove(board,self.game_turn)
        board.place_piece(self.game_turn+1,pos[0],pos[1])
        self.game_turn += 1
        self.game_turn = self.game_turn % 2
                
    def step_gen(self,board:Board)->list:   #生成当前合理落子位置
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
                                steps.append((i,j))
                                tempmsg = True
                                break
                        if temmsg:
                            break
        if len(steps) == 0:
            centre = (BLOCKS//2,BLOCKS//2)
            steps.append(centre)
        return set(steps)