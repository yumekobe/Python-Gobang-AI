import pygame
import time
from constants import *
from board import *
from graphics import *
from game import *

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Gobang")
    screen.fill(BOARD_COLOUR)
    game = Gameplay()
    while True:
        game.Start(screen)
        game.Run(screen)
        time.sleep(2)

if __name__ == '__main__':
    main()