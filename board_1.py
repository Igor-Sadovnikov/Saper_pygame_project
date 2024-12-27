import pygame
from random import randint

COLORS = ['red', 'blue']


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
    
    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.screen, pygame.Color('white'),
                                 (self.left + i * self.cell_size, self.top + j * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                pygame.draw.circle(self.screen, pygame.Color(COLORS[self.board[j][i]]),
                                    ((self.left + i * self.cell_size + self.cell_size // 2,
                                    self.top + j * self.cell_size + self.cell_size // 2)),
                                    self.cell_size // 2 - 4, 0)

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
    def __init__(self, width, height, mines):
        pygame.display.set_caption('Сапёр')
        self.cell_size = 30
        self.board = [['-1'] * (width + 2) for _ in range(height + 2)]
        mn = set()
        while len(mn) < mines:
            koords = tuple([randint(1, height), randint(1, width)])
            mn.add(koords)
        for elem in mn:
            self.board[elem[0]][elem[1]] = '10'
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
    
    def render(self):
        for i in range(1, self.width_cl + 1):
            for j in range(1, self.height_cl + 1):
                pygame.draw.rect(self.screen, pygame.Color('white'),
                    (self.left + i * self.cell_size, self.top + j * self.cell_size,
                    self.cell_size, self.cell_size), 1)
                if int(self.board[j][i]) == 10:
                    pygame.draw.rect(self.screen, pygame.Color('red'),
                                    (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                    self.cell_size - 2, self.cell_size - 2), 0)
                font = pygame.font.Font(None, 20)
                if str(self.board[j][i]) != '-1' and str(self.board[j][i]) != '10':
                    show_text = str(self.board[j][i])
                else:
                    show_text = ''
                text = font.render(show_text, True, 'green')
                text_x = self.cell_size * i + 10
                text_y = self.cell_size * j + 10
                self.screen.blit(text, (text_x, text_y))
    
    def open_cell(self, pos):
        kort = pos
        x = kort[0]
        y = kort[1]
        if x < 0 or x > self.width_cl or y < 0 or y > self.height_cl:
            return
        if (x, y) in self.visited:
            return
        elif self.board[y][x] == '10':
            return self.game_over()
        self.visited.add((x, y))
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
        if self.board[y][x] == '0':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0):
                        pos = (x + dx, y + dy,)
                        self.open_cell(pos)
    
    def game_over(self):
        return -1