import pygame
import os
import sys
from board_1 import Minesweeper


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 500, 500
tile_width = tile_height = 50
screen = pygame.display.set_mode(size)
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    global count_of_mines
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    ch = True
    running = True
    start_screen()
    while True:
        try:
            count_of_mines = int(input('Введите количество мин:'))
            if 1 < count_of_mines < 100:
                break
        except Exception:
            print('Число введено неверно')
    board = Minesweeper(10, 10, count_of_mines)
    board.set_view(0, 0, 50)
    while running:
        if ch:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = board.get_cell(event.pos)
                    if board.open_cell(pos) == -1:
                        print('game_over')
                        ch = False
                        res = False
                    if board.win() == 1:
                        print('You win')
                        ch = False
                        res = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    pos = board.get_cell(event.pos)
                    board.show_flag(pos)
                    if board.win() == 1:
                        print('You win')
                        ch = False
                        res = True
                board.screen.fill('black')
                board.render()
        else:
            board.screen.fill('white')
            pygame.font.init()
            my_font_1 = pygame.font.SysFont('Classy Vogue', 100)
            my_font_2 = pygame.font.SysFont('Classy Vogue', 30)
            if res == True:
                text_surface = my_font_1.render('Ты выиграл', False, (0, 0, 0))
                board.screen.blit(text_surface, (100, 200))
            else:
                fon_end = pygame.transform.scale(load_image('loss_fon.png'), (600, 600))
                board.screen.blit(fon_end, (0, 0))
                # text_surface = my_font_1.render('Ты проиграл', False, (0, 0, 0))
            text_surface_restart = my_font_2.render('Начать заново', False, (0, 0, 0))
            text_surface_restart_rect = text_surface_restart.get_rect(topleft=(230, 400))
            # board.screen.blit(text_surface, (100, 200))
            board.screen.blit(text_surface_restart, text_surface_restart_rect)
            for event in pygame.event.get():
                if text_surface_restart_rect.collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    ch = True
                    board = Minesweeper(10, 10, 10)
                    board.set_view(0, 0, 50)
        pygame.display.update()