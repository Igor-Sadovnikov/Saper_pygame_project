# main_programme
import pygame
from board_1 import Minesweeper

if __name__ == '__main__':
    pygame.init()
    board = Minesweeper(10, 15, 10)
    board.set_view(0, 0, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  
                pos = board.get_cell(event.pos)
                if board.open_cell(pos) == -1:
                    board.screen.fill('white')
                    print('game_over')
                    exit()
        board.screen.fill('black')
        board.render()
        pygame.display.flip()