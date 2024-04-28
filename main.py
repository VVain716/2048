import pygame
import random
import time
import copy

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
BLOCK_SIZE = WINDOW_WIDTH // 4
BLACK, WHITE, GREEN, RED = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0)
LINES, TILES = (185, 173, 161), (202, 193, 181)
WHITE_TILE = (248, 246, 242)
BLACK_TILE = (117, 110, 102)
GAME_OVER_COLOR = (139,69,19)
SCORE_COLOR = (185, 173, 161)
pygame.init()
BIG_FONT = pygame.font.Font("ClearSans-Bold.ttf", 80)
MEDIUM_FONT = pygame.font.Font("ClearSans-Bold.ttf", 64)
SMALL_FONT = pygame.font.Font("ClearSans-Bold.ttf", 56)
GAME_OVER_FONT = pygame.font.Font("ClearSans-Bold.ttf", 30)
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
colors_death = {
    2: (248, 238, 228),
    4: (247, 234, 210),
    8:(252, 187, 131),
    16:(255, 159, 109),
    32:(255, 134, 105),
    64:(255, 104, 69),
    128:(247, 217, 124),
    256:(247, 214, 107),
    512:(247, 210, 90),
    1024:(247, 207, 73),
    2048:(247, 204, 56),
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
            font = SMALL_FONT if self.val > 512 else (MEDIUM_FONT if 512 >= self.val >= 128 else BIG_FONT)
            val = str(self.val)
            text = font.render(val, True, text_color, color)
            text_rect = text.get_rect()
            text_rect.center = (self.position.x * BLOCK_SIZE + BLOCK_SIZE // 2, self.position.y * BLOCK_SIZE + BLOCK_SIZE // 2)      
            screen.blit(text, text_rect)
class Board():
    def __init__(self) -> None:
        self.board = self.populate_board()
        self.prev_board = copy.deepcopy(self.board)
        self.score = 0
        self.move = self.Movement(self)
    def compare(self, board1, board2):
        for i in range(4):
            for j in range(4):
                if board1[i][j].val != board2[i][j].val:
                    return False
        return True
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
    def set_board(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j] = Block(self.board[i][j].val, (j, i))
    def random_index(self):
        x, y = random.randint(0, 3), random.randint(0, 3)
        while self.board[x][y].val != 0:
            x, y = random.randint(0, 3), random.randint(0, 3)
        self.board[x][y].val = 2
    def game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j].val == 0:
                    return False
        for i in range(3):
            for j in range(3):
                if self.board[i][j].val == self.board[i][j + 1].val or self.board[i][j].val == self.board[i + 1][j].val:
                    return False
        for i in range(3):
            if self.board[3][i].val == self.board[3][i + 1].val or self.board[i][3].val == self.board[i + 1][3].val:
                return False
        return True
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
                        row[count].prev_position = row[count].position
                        count += 1
                while count < 4:
                    row[count] = Block(0, None)
                    count += 1
                
                row = merge(row)
                self.board_class.board[i] = row 
            self.board_class.set_board()
            return self.board_class.board
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
            return self.board_class.board
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
            return self.board_class.board
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
            return self.board_class.board
        
board_class = Board()

# board_class.random_index()
# board_class.random_index()
board_class.board = [
    [Block(2), Block(4), Block(8), Block(16)],
    [Block(16), Block(8), Block(4), Block(2)],
    [Block(2), Block(4), Block(8), Block(16)],
    [Block(16), Block(8), Block(4), Block(2)]
]   
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
game_over_ui = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over_ui:
            x, y = pygame.mouse.get_pos()
            if play_again_text_rect.collidepoint(x, y):
                board_class.board = board_class.populate_board()
                board_class.random_index()
                board_class.random_index()
                board_class.set_board()
                game_over_ui = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not left_pressed:
                    left_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.left()
                    if not board_class.compare(prev_board, board_class.board):
                        board_class.random_index()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not right_pressed:
                    right_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.right()
                    if not board_class.compare(prev_board, board_class.board):
                        board_class.random_index()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if not up_pressed:
                    up_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.up()
                    if not board_class.compare(prev_board, board_class.board):
                        board_class.random_index()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not down_pressed:
                    down_pressed = True
                    prev_board = copy.deepcopy(board_class.board)
                    board_class.move.down()
                    if not board_class.compare(prev_board, board_class.board):
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
    if board_class.game_over():
        dim_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        dim_surface.set_alpha(64)
        dim_surface.fill((0, 0, 0))
        screen.blit(dim_surface, (0, 0))

        text = MEDIUM_FONT.render("Game Over!", True, (210, 210, 210))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        play_again_text = GAME_OVER_FONT.render("Play Again", True, WHITE, GAME_OVER_COLOR)
        play_again_text_rect = play_again_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(text, text_rect)
        screen.blit(play_again_text, play_again_text_rect)
        game_over_ui = True

    pygame.display.flip()
    clock.tick(60)

