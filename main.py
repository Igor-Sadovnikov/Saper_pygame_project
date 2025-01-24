import pygame
import os
import sys
from board_1 import Minesweeper
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QLCDNumber, QPushButton, QInputDialog


class Input_dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 500, 400, 250)
        self.setWindowTitle('Сапёр')
        self.count_mines = 10
        self.input_name = QLineEdit(self)
        self.input_name.move(200, 50)
        self.label_name = QLabel(self)
        self.label_name.setText('Введите имя пользователя')
        self.label_name.move(10, 50)
        self.LCD_count = QLCDNumber(self)
        self.LCD_count.move(120, 100)
        self.LCD_count.display(self.count_mines)
        self.label_count = QLabel(self)
        self.label_count.move(10, 100)
        self.label_count.setText('Количество мин:')
        self.change_btn = QPushButton(self)
        self.change_btn.move(50, 150)
        self.change_btn.setText('Изменить кол-во мин')
        self.change_btn.clicked.connect(self.dialog)
        self.ok_button = QPushButton(self)
        self.ok_button.move(50, 200)
        self.ok_button.setText('ОК')
        self.ok_button.clicked.connect(self.run_game)

    def dialog(self):
        new_count, ok_pressed = QInputDialog.getInt(
    self, "Введите количество мин", "Введите количество мин",
    10, 10, 99, 1)
        self.count_mines = new_count
        self.LCD_count.display(self.count_mines)

    def run_game(self):
        self.close()
        main_start_game(self.count_mines, self.input_name.text())


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
    color = (255, 150, 150)
    rect_position = [280, 430, 200, 50]
    pygame.draw.rect(screen, color, rect_position)
    pygame.font.init()
    font_new_game = pygame.font.SysFont('Classy Vogue', 50)
    text_surface_restart = font_new_game.render('Новая игра', False, (0, 0, 0))
    text_surface_restart_rect = text_surface_restart.get_rect(topleft=(285, 440))
    screen.blit(text_surface_restart, text_surface_restart_rect)
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_surface_restart_rect.collidepoint(mouse_pos):
                    running = False  # начинаем игру
        if running == True:
            pygame.display.flip()
        clock.tick(FPS)


def main_start_game(count_of_mines, username):
    ch = True
    running = True
    board = Minesweeper(10, 10, count_of_mines, username)
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
            font_1 = pygame.font.SysFont('Classy Vogue', 100)
            font_2 = pygame.font.SysFont('Classy Vogue', 30)
            if res == True:
                fon_end = pygame.transform.scale(load_image('win_fon.png'), (600, 600))
                board.screen.blit(fon_end, (0, 0))
            else:
                fon_end = pygame.transform.scale(load_image('loss_fon.png'), (600, 600))
                board.screen.blit(fon_end, (0, 0))
            text_surface_restart = font_2.render('Начать заново', False, (0, 0, 0))
            text_count_mines = font_2.render(f'Обезврежено мин: {board.count_true_mines} из {board.mines}', False, (0, 0, 0))
            results = board.get_results()
            text_place = font_2.render(f'Ваше место в рейтинге: {results[0]}', False, (0, 0, 0))
            text_1_place = font_2.render(f'1 место: {results[1][1]} ({results[1][0]})', False, (0, 0, 0))
            text_2_place = font_2.render(f'2 место: {results[2][1]} ({results[2][0]})', False, (0, 0, 0))
            text_3_place = font_2.render(f'3 место: {results[3][1]} ({results[3][0]})', False, (0, 0, 0))
            color = (255, 150, 150)
            rect_position = [220, 510, 170, 35]
            pygame.draw.rect(screen, color, rect_position) 
            text_surface_restart_rect = text_surface_restart.get_rect(topleft=(230, 520))
            board.screen.blit(text_surface_restart, text_surface_restart_rect)
            board.screen.blit(text_count_mines, (50, 30))
            board.screen.blit(text_place, (50, 60))
            board.screen.blit(text_1_place, (50, 90))
            board.screen.blit(text_2_place, (50, 120))
            board.screen.blit(text_3_place, (50, 150))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_surface_restart_rect.collidepoint(event.pos):
                        ch = True
                        board = Minesweeper(10, 10, count_of_mines, username)
                        board.set_view(0, 0, 50)
        if running:
            pygame.display.update()


def main():
    start_screen()
    start()


def start():
    app = QApplication(sys.argv)
    ex = Input_dialog()
    ex.show()
    app.exec()


def restart():
    ex = Input_dialog()
    ex.show()

if __name__ == '__main__':
    main()