import pygame
from board import Board
from constants import *
circle_radius = 12
def draw_board(scr):
    
    scr.fill(BOARD_COLOUR)
    for i in range(1,BLOCKS):
        pygame.draw.line(scr, BLACK, [BLOCK_WIDTH + BLOCK_WIDTH/2, i * BLOCK_WIDTH + BLOCK_WIDTH/2], [BLOCKS * BLOCK_WIDTH - BLOCK_WIDTH/2, i * BLOCK_WIDTH + BLOCK_WIDTH/2], 2)
    for j in range(1,BLOCKS):
        pygame.draw.line(scr, BLACK, [j * BLOCK_WIDTH + BLOCK_WIDTH/2, BLOCK_WIDTH + BLOCK_WIDTH/2], [j * BLOCK_WIDTH + BLOCK_WIDTH/2, BLOCKS * BLOCK_WIDTH - BLOCK_WIDTH/2], 2)
    
    font = pygame.font.SysFont("Consolas", 17)
    for i in range(1,BLOCKS):
        te = str(i)
        text = font.render(te, True, BLACK)
        scr.blit(text,(BLOCK_WIDTH/5, BLOCK_WIDTH/3 + i * BLOCK_WIDTH))
        scr.blit(text,(BLOCK_WIDTH/3 + i * BLOCK_WIDTH, BLOCK_WIDTH/5))
    draw_currencyrent_piece(scr,0)
    pygame.draw.circle(scr, BLACK, (BLOCK_WIDTH * BLOCKS/2 + BLOCK_WIDTH/2 + 1, BLOCK_WIDTH* BLOCKS/2 + BLOCK_WIDTH/2 + 1),4,0)
    pygame.display.update()

def draw_pieces(scr,board:Board):
    #注意黑子是1，白子是2
    for i in range(BLOCKS):
        for j in range(BLOCKS):
            if board.data[i][j] == 1:
                pygame.draw.circle(scr, BLACK, (BLOCK_WIDTH/2 + BLOCK_WIDTH*j + 1, BLOCK_WIDTH/2 + BLOCK_WIDTH*i + 1),circle_radius,0)
            elif board.data[i][j] == 2:
                pygame.draw.circle(scr, WHITE, (BLOCK_WIDTH/2 + BLOCK_WIDTH*j + 1, BLOCK_WIDTH/2 + BLOCK_WIDTH*i + 1),circle_radius,0)
    pygame.display.update()

def draw_currencyrent_piece(scr,game_turn:int):
    if game_turn == 0:
        colourh = BLACK
    else:
        colourh = WHITE
    pygame.draw.circle(scr, colourh, (BLOCK_WIDTH/2 + 1, BLOCK_WIDTH/2 + 1),circle_radius-2,0)
    pygame.display.update()