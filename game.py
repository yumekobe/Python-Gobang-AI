import pygame
import time
from constants import *
from board import *
from graphics import *
def terminate():
    pygame.quit()
    exit()
class Gameplay:
    def player_turn(self,game_turn,board:Board,is_running:bool):
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
                        if pos_i > 0 and pos_j > 0 and pos_i < 16 and pos_j < 16:
                            if board.data[pos_i][pos_j] == 0:
                                break
                            else:
                                continue
                        else:
                            continue
            if pos_i > 0 and pos_j > 0 and pos_i < 16 and pos_j < 16:
                if board.data[pos_i][pos_j] == 0:
                    break
        board.place_piece(game_turn[0] + 1,pos_i,pos_j)
        game_turn[0] += 1
        game_turn[0] = game_turn[0] % 2

    def judge(self,board:Board)->bool:
        for i in range(1,16):
            for j in range(1,16):
                if board.data[i][j] != 0:
                    count = 0
                    #判断列是否满足
                    if i < 12:
                        for k in range(5):
                            if board.data[i][j] == board.data[i+k][j]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
                    count = 0
                    if j < 12:
                        for k in range(5):
                            if board.data[i][j] == board.data[i][j+k]:
                                count += 1
                            else:
                                break
                        if count == 5:
                            return True
                    count = 0
                    if i < 12 and j < 12:
                        for k in range(5):
                            if board.data[i][j] == board.data[i+k][j+k]:
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
        font = pygame.font.SysFont("Consolas", 30)
        tip = font.render(tip_str1, True, BLACK)  
        tip2 = font.render(tip_str2, True, BLACK)
        screen.blit(tip, (40, SCREEN_HEIGHT/3 + 30)) 
        screen.blit(tip2, (80, SCREEN_HEIGHT/3 + 80))
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
    def Run(self,screen):
        is_running = True
        draw_board(screen)
        board = Board([])
        #board.data[3][3] = 1     #测试用代码
        #board.data[4][4] = 2     #测试用代码
        game_turn = [0]
        draw_pieces(screen,board)
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_running = 0
            self.player_turn(game_turn,board,is_running)
            draw_pieces(screen,board)
            draw_current_piece(screen,game_turn[0])
            pygame.display.update()
            time.sleep(0.1)
            if_continue = self.judge(board)
            if if_continue:
                self.Win(screen,game_turn[0])
                return
        
    def Win(self,screen,game_turn:int):
        screen.fill(BOARD_COLOUR)
        winner = ''
        if game_turn == 1:
            winner = 'BLACK'
        elif game_turn == 0:
            winner = 'WHITE'
        msg = f'{winner} won the game'
        font = pygame.font.SysFont("Consolas", 30)
        msg1 = font.render(msg, True, BLACK)
        screen.blit(msg1, (75, SCREEN_HEIGHT/3 + 50))  
        pygame.display.update()  