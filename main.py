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
    intro_text = ["САПЕР"]
    fon = pygame.transform.scale(load_image('fon.png'), (600, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10   
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
    board = Minesweeper(10, 10, 10)
    board.set_view(0, 0, 50)
    running = True
    start_screen()
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    pos = board.get_cell(event.pos)
                    board.show_flag(pos)
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