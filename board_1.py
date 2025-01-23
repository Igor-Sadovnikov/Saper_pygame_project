import pygame
import sys
import os
import sqlite3
from random import randint

COLORS = ['red', 'blue']


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


class Board:
    def __init__(self, width, height, mines):
        pygame.display.set_caption('Сапёр')
        self.cell_size = 30
        self.size = width * self.cell_size * 2, height * self.cell_size * 2
        self.width, self.height = width, height
        self.board = []
        count_0, count_1 = 0, 0
        for i in range(self.height):
            sp = []
            for j in range(self.width):
                ch = randint(0, 1)
                if ch == 0:
                    count_0 += 1
                else:
                    count_1 += 1
                sp.append(ch)
            self.board.append(sp)
            if count_0 == 0:
                self.board[0][0] = 1
            elif count_1 == 0:
                self.board[0][0] = 1
        self.left = 10
        self.top = 10
        self.screen = pygame.display.set_mode(self.size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
                
    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if x >= self.width or y >= self.height:
            return None
        elif x < 0 or y < 0:
            return None
        return x, y

    def change_cell(self, pos):
        kort = self.get_cell(pos)
        if kort is not None:
            x, y = kort[0], kort[1]
            for i in range(len(self.board[x])):
                self.board[y][i] = self.board[y][x]
            for i in range(len(self.board)):
                if i != y:
                    self.board[i][x] = self.board[y][x]


class Minesweeper(Board):
    def __init__(self, width, height, mines, username):
        pygame.display.set_caption('Сапёр')
        self.cell_size = 30
        self.w = width
        self.h = height
        self.mines = mines
        self.username = username
        self.count_true_mines = 0
        self.board = [['-1'] * (width + 2) for _ in range(height + 2)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.flag = 1
        self.width_cl = width
        self.height_cl = height
        self.width = width * self.cell_size * 2
        self.height = height * self.cell_size * 2
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.visited = set()
        self.flags = set()
    
    def render(self):
        image = load_image('bomb.png')
        image_flag = load_image('flag.png')
        for i in range(1, self.width_cl + 1):
            for j in range(1, self.height_cl + 1):
                pygame.draw.rect(self.screen, pygame.Color('white'),
                    (self.left + i * self.cell_size, self.top + j * self.cell_size,
                    self.cell_size, self.cell_size), 1)
                if int(self.board[j][i]) == 10:
                    self.screen.blit(image, (self.left + i * self.cell_size + 5, self.top + j * self.cell_size))    
                font = pygame.font.Font(None, 20)
                if str(self.board[j][i]) != '-1' and str(self.board[j][i]) != '10':
                    show_text = str(self.board[j][i])
                else:
                    show_text = ''
                text = font.render(show_text, True, 'green')
                text_x = self.cell_size * i + 10
                text_y = self.cell_size * j + 10
                self.screen.blit(text, (text_x, text_y))
                if tuple([j, i]) in self.flags:
                    self.screen.blit(image_flag, (self.left + i * self.cell_size + 2, self.top + j * self.cell_size))
                mines_left = str(self.mines - len(self.flags))
                font = pygame.font.Font(None, 40)
                text = font.render(mines_left, True, 'red')
                self.screen.blit(text, (10, 10))
     
    def open_cell(self, pos):
        kort = pos
        x = kort[0]
        y = kort[1]
        kort = tuple([y, x])
        if len(self.visited) == 0:
            self.mn = set()
            while len(self.mn) < self.mines:
                koords = tuple([randint(1, self.h), randint(1, self.w)])
                if koords != kort:
                    self.mn.add(koords)
            for elem in self.mn:
                self.board[elem[0]][elem[1]] = '10'
        if x < 0 or x > self.width_cl or y < 0 or y > self.height_cl:
            return
        if (x, y) in self.visited:
            return
        elif self.board[y][x] == '10':
            return self.game_over()
        kort = (x, y,)
        print(kort)
        count = 0
        if self.board[kort[1]][kort[0]] != '10':
            if self.board[kort[1]][kort[0] - 1] == '10':
                count += 1
            if self.board[kort[1] - 1][kort[0] - 1] == '10':
                count += 1
            if self.board[kort[1] + 1][kort[0] - 1] == '10':
                count += 1
            if self.board[kort[1] - 1][kort[0]] == '10':
                count += 1
            if self.board[kort[1] + 1][kort[0]] == '10':
                count += 1
            if self.board[kort[1]][kort[0] + 1] == '10':
                count += 1
            if self.board[kort[1] - 1][kort[0] + 1] == '10':
                count += 1
            if self.board[kort[1] + 1][kort[0] + 1] == '10':
                count += 1
            self.board[kort[1]][kort[0]] = str(count)
            if self.board[y][x] != '10':
                self.visited.add((x, y))
        if self.board[y][x] == '0':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0):
                        pos = (x + dx, y + dy,)
                        self.open_cell(pos)
    
    def show_flag(self, pos):
        kort = pos
        x = kort[0]
        y = kort[1]
        kort1 = tuple([y, x])
        if kort1 in self.flags:
            self.flags.discard(kort1)
        else:
            self.flags.add(kort1)
    
    def game_over(self):
        self.count_true_mines = len(self.flags & self.mn)
        self.place = self.get_results()
        return -1
    
    def win(self):
        for i in range(1, 11):
            for j in range(1, 11):
                if self.board[i][j] == '-1':
                    self.place = self.get_results()
                    return 0
        print(self.flags)
        print(self.mn)
        self.count_true_mines = len(self.flags & self.mn)
        self.place = self.get_results()
        if self.flags == self.mn:
            return 1
        return 0
    
    def get_results(self):
        con = sqlite3.connect('database_saper.sqlite3')
        cur = con.cursor()
        data1 = cur.execute(f"""SELECT *
                               FROM table_main
                               WHERE username = '{self.username}'""")
        data = []
        for elem in data1:
            data.append(elem)
        if len(data) != 0:
            cur.execute(f"""
                    UPDATE table_main
                    SET last_result = '{self.count_true_mines}'
                    WHERE username = '{self.username}'
                    """)
            con.commit()
            if int(data[0][3]) > int(data[0][2]):
                cur.execute(f"""
                    UPDATE table_main
                    SET best_result = '{self.count_true_mines}'
                    WHERE username = '{self.username}'
                    """)
                con.commit()
        else:
            cur.execute(f"""INSERT INTO table_main(username,best_result,last_result)
                        VALUES('{self.username}', '{self.count_true_mines}',  '{self.count_true_mines}')""")
            con.commit()
        data2 = cur.execute(f"""SELECT *
                                FROM table_main""")
        data = []
        for elem in data2:
            data.append(elem)
        data1 = cur.execute(f"""SELECT *
                               FROM table_main
                               WHERE username = '{self.username}'""")
        data_user = []
        for elem in data1:
            data_user.append(elem)
        data = sorted(data, key=lambda x: x[2])
        data.reverse()
        place = data.index(data_user[0]) + 1
        data = data[:3]
        con.close()
        return [place, (data[0][0], data[0][1]), (data[1][0], data[1][1]), (data[2][0], data[2][1])]