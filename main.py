import pygame
import random
import time
import copy

WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
BLOCK_SIZE = WINDOW_WIDTH // 4
BLACK, WHITE, GREEN, RED = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0)
LINES, TILES = (185, 173, 161), (202, 193, 181)
WHITE_TILE = (248, 246, 242)
BLACK_TILE = (117, 110, 102)
pygame.init()
FONT = pygame.font.Font("ClearSans-Bold.ttf", 64)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True
colors = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8:(242, 177, 121),
    16:(245, 149, 99),
    32:(246, 124, 95),
    64:(246, 94, 59),
    128:(237, 207, 114),
    256:(237, 204, 97),
    512:(237, 200, 80),
    1024:(237, 197, 63),
    2048:(237, 194, 46),
}
class Block():
    def __init__(self, val: int, position=None) -> None:
        self.val = val
        if position:
            self.position = pygame.Vector2(position[0], position[1])
        else:
            self.position = pygame.Vector2(0, 0)
        self.prev_position = None
    def draw_block(self):
        if self.val != 0: 
            color = colors.get(self.val)
            color = color if color else BLACK
            text_color = BLACK_TILE if self.val <= 4 else WHITE_TILE
            rect = pygame.rect.Rect(self.position.x * BLOCK_SIZE, self.position.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, rect)
            val = str(self.val)
            text = FONT.render(val, True, text_color, color)
            text_rect = text.get_rect()
            text_rect.center = (self.position.x * BLOCK_SIZE + BLOCK_SIZE // 2, self.position.y * BLOCK_SIZE + BLOCK_SIZE // 2)      
            screen.blit(text, text_rect)

class Board():
    def __init__(self) -> None:
        self.board = self.populate_board()
        self.prev_board = copy.deepcopy(self.board)

        self.move = self.Movement(self)
    def populate_board(self):
        board = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(Block(0, (i, j)))
            board.append(tmp)
        return board
    def draw_board(self):
        for i in range(4):
            for j in range(4):
                print(str(self.board[i][j].val) + "    " + str(self.board[i][j].position), end="")
            print()
        print()
    def display_board(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j].draw_block()
                print(self.board[i][j].val)
    def set_board(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j] = Block(self.board[i][j].val, (j, i))
    def random_index(self):
        x, y = random.randint(0, 3), random.randint(0, 3)
        while self.board[x][y].val != 0:
            x, y = random.randint(0, 3), random.randint(0, 3)
        self.board[x][y].val = 2
    class Movement():
        def __init__(self, board_class) -> None:
            self.board_class = board_class
        def left(self):
            def merge(row: list):
                for i in range(3):
                    if row[i].val == row[i+1].val:
                        row[i].val *= 2
                        row.pop(i+1)
                        row.append(Block(0))
                return row
            for i in range(4):
                count = 0
                row = self.board_class.board[i]
                for j in range(4):
                    if row[j].val != 0:
                        row[count] = row[j]
                        count += 1
                while count < 4:
                    row[count] = Block(0, None)
                    count += 1
                
                row = merge(row)
                self.board_class.board[i] = row 
            self.board_class.set_board()
        def right(self):
            def merge(row: list):
                for i in range(3):
                    if row[i].val == row[i+1].val:
                        row[i].val *= 2
                        row.pop(i+1)
                        row.append(Block(0))
                return row
            for i in range(4):
                count = 0
                row = self.board_class.board[i]
                row.reverse()
                for j in range(4):
                    if row[j].val != 0:
                        row[count] = row[j]
                        count += 1
                while count < 4:
                    row[count] = Block(0, None)
                    count += 1
                
                row = merge(row)
                row.reverse()
                self.board_class.board[i] = row 

            self.board_class.set_board()
        def up(self):
            def merge(row: list):
                for i in range(3):
                    if row[i].val == row[i+1].val:
                        row[i].val *= 2
                        row.pop(i+1)
                        row.append(Block(0))
                return row
            for j in range(4):
                count = 0
                col = [self.board_class.board[i][j] for i in range(4)]
                for i in range(4):
                    if col[i].val != 0:
                        col[count] = col[i]
                        count += 1
                while count < 4:
                    col[count] = Block(0)
                    count += 1
                col = merge(col)
                for i in range(4):
                    self.board_class.board[i][j] = col[i]
            self.board_class.set_board()
        def down(self):
            def merge(row: list):
                for i in range(3):
                    if row[i].val == row[i+1].val:
                        row[i].val *= 2
                        row.pop(i+1)
                        row.append(Block(0))
                return row
            for j in range(4):
                count = 0
                col = [self.board_class.board[i][j] for i in range(4)]
                col.reverse()
                for i in range(4):
                    if col[i].val != 0:
                        col[count] = col[i]
                        count += 1
                while count < 4:
                    col[count] = Block(0, None)
                    count += 1
                merge(col)
                col.reverse()
                for i in range(4):
                    self.board_class.board[i][j] = col[i]
            self.board_class.set_board()

board_class = Board()
board_class.random_index()
board_class.random_index()
board_class.set_board()
def drawGrid():
    blocksize = BLOCK_SIZE
    for x in range(0, WINDOW_WIDTH, blocksize):
        for y in range(0, WINDOW_HEIGHT, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            pygame.draw.rect(screen, LINES, rect, 15)

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not left_pressed:
                    left_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    print(prev_board == board_class.board)
                    print(board_class.board)
                    board_class.move.left()
                    if prev_board != board_class.board:
                        board_class.random_index()
                    else:
                        print('Hi')
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not right_pressed:
                    right_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.right()
                    if prev_board != board_class.board:
                        board_class.random_index()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if not up_pressed:
                    up_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.up()
                    if prev_board != board_class.board:
                        board_class.random_index()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not down_pressed:
                    down_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.down()
                    if prev_board != board_class.board:
                        board_class.random_index()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left_pressed = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right_pressed = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                up_pressed = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down_pressed = False

    screen.fill(TILES)
    for i in range(4):
        for j in range(4):
            board_class.board[i][j].draw_block()
    drawGrid()
    pygame.display.flip()
    clock.tick(60)
