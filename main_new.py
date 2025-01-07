import pygame
from main_new import Minesweeper
if __name__ == '__main__':
    pygame.init()
    ch = True
    board = Minesweeper(10, 10, 10)
    board.set_view(0, 0, 50)
    running = True
    while running:
        if ch:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = board.get_cell(event.pos)
                    if board.open_cell(pos) == -1:
                        print('game_over')
                        ch = False
                board.screen.fill('black')
                board.render()
        else:
            board.screen.fill('white')
            pygame.font.init()
            my_font_1 = pygame.font.SysFont('Classy Vogue', 100)
            my_font_2 = pygame.font.SysFont('Classy Vogue', 30)
            text_surface = my_font_1.render('Ты проиграл', False, (0, 0, 0))
            text_surface_restart = my_font_2.render('Начать заново', False, (0, 0, 0))
            text_surface_restart_rect = text_surface_restart.get_rect(topleft=(230, 400))
            board.screen.blit(text_surface, (100, 200))
            board.screen.blit(text_surface_restart, text_surface_restart_rect)
            for event in pygame.event.get():
                if text_surface_restart_rect.collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    ch = True
                    board = Minesweeper(10, 10, 10)
                    board.set_view(0, 0, 50)
        pygame.display.update()