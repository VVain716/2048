"""
        NAME: VED VAINATEYA | VINU VAINATEYA
        DATE: APRIL, 23, 2024
     PURPOSE: DESIGN AND IMPLEMENT A SNAKE GAME IN PYTHON
     VERSION: PYTHON 3.9
CODE VERSION: VERSION 1

"""


import pygame
import time
import random
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
BLOCK_SIZE=100
BLACK, WHITE, GREEN, RED = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0)
GAME_SPEED = 0.1
# SPRITE_FILENAME = 'right_head.png'
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True
# head = pygame.image.load(SPRITE_FILENAME)
# head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))
class Snake():
    #Class will contain player_pos_list, apple_pos, all the movement functions and more
    def __init__(self) -> None:
        self.player_pos_list = [pygame.Vector2(0, 0)]
        self.apple_pos = pygame.Vector2(700, 700)
        self.move = self.Movement(self)
        self.score = 0
        self.ui = False
    def update(self) -> None:
        self.player_pos_list.append(pygame.Vector2(self.player_pos_list[-1].x - BLOCK_SIZE, self.player_pos_list[-1].y))
        self.apple_pos.x, self.apple_pos.y = (random.randrange(8)*BLOCK_SIZE, random.randrange(8)*BLOCK_SIZE)
        while self.apple_pos in self.player_pos_list:
            self.apple_pos.x, self.apple_pos.y = (random.randrange(8)*BLOCK_SIZE, random.randrange(8)*BLOCK_SIZE)
        self.score += 1
    def death(self) -> None:
        self.ui = True
    class Movement():
        def __init__(self, snake) -> None:
            self.player_pos_list = snake.player_pos_list
            self.last_coordinates = None
            self.current_key_pressed = -1
            #current_key_pressed can be 0, 1, 2, 3: 0 left, 1 right, 2 up, 3 down
        def left(self):
            #left is correct
            self.current_key_pressed = 0
            for i in range(len(self.player_pos_list)):
                if self.last_coordinates:
                    tmp = self.last_coordinates
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x, self.player_pos_list[i].y = tmp
                    if self.player_pos_list[i].x < 0:
                        self.player_pos_list[i].x = 0
                        snake.death()
                else:
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x -= BLOCK_SIZE
                    if self.player_pos_list[i].x < 0:
                        self.player_pos_list[i].x = 0
                        snake.death()
            self.last_coordinates = None
        def right(self):
            self.current_key_pressed = 1
            for i in range(len(self.player_pos_list)):
                if self.last_coordinates:
                    tmp = self.last_coordinates
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x, self.player_pos_list[i].y = tmp
                    if self.player_pos_list[i].x >= WINDOW_WIDTH:
                        self.player_pos_list[i].x = WINDOW_WIDTH - BLOCK_SIZE
                        snake.death()

                else:
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x+= BLOCK_SIZE
                    if self.player_pos_list[i].x >= WINDOW_WIDTH:
                        self.player_pos_list[i].x = WINDOW_WIDTH - BLOCK_SIZE
                        snake.death()
            self.last_coordinates = None
        def up(self):
            self.current_key_pressed = 2
            for i in range(len(self.player_pos_list)):
                if self.last_coordinates:
                    tmp = self.last_coordinates
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x, self.player_pos_list[i].y = tmp
                    if self.player_pos_list[i].y < 0:
                        self.player_pos_list[i].y = 0
                        snake.death()
                else:
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].y -= BLOCK_SIZE
                    if self.player_pos_list[i].y < 0:
                        self.player_pos_list[i].y = 0
                        snake.death()
            self.last_coordinates = None
        def down(self):
            self.current_key_pressed = 3
            for i in range(len(self.player_pos_list)):
                if self.last_coordinates:
                    tmp = self.last_coordinates
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].x, self.player_pos_list[i].y = tmp
                    if self.player_pos_list[i].y >= WINDOW_WIDTH:
                        self.player_pos_list[i].y = WINDOW_WIDTH - BLOCK_SIZE
                        snake.death()
                else:
                    self.last_coordinates = (self.player_pos_list[i].x, self.player_pos_list[i].y)
                    self.player_pos_list[i].y += BLOCK_SIZE
                    if self.player_pos_list[i].y >= WINDOW_WIDTH:
                        self.player_pos_list[i].y = WINDOW_WIDTH - BLOCK_SIZE
                        snake.death()
            self.last_coordinates = None
snake = Snake()
def UI(score):
    #returns text and text_rect, which can be used by screen.blit(text, text_rect)
    font = pygame.font.Font("Helvetica.ttf", 64)
    score_str = "Apples eaten: " + str(score)
    score_text = font.render(score_str, True, WHITE, BLACK)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8)
    play_again_text = font.render("Play Again", True, BLACK, WHITE)
    play_again_text_rect = play_again_text.get_rect()
    play_again_text_rect.center = (WINDOW_WIDTH // 2, 3 * WINDOW_HEIGHT // 4)
    return score_text, score_text_rect, play_again_text, play_again_text_rect

def drawGrid() -> None:
    blocksize = BLOCK_SIZE
    for x in range(0, WINDOW_WIDTH, blocksize):
        for y in range(0, WINDOW_HEIGHT, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            pygame.draw.rect(screen, WHITE, rect, 1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and snake.ui == True:
            x, y = pygame.mouse.get_pos()
            if play_again_text_rect.collidepoint(x, y):
                snake.ui = False
                snake = Snake()
    screen.fill("black")

    if not snake.ui:
        for player_pos in snake.player_pos_list:
            if player_pos == snake.player_pos_list[0]:
                # Code for head
                # screen.blit(head, (player_pos.x, player_pos.y))

                # Current code

                rect = pygame.Rect(player_pos.x, player_pos.y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GREEN, rect, BLOCK_SIZE)
            else:
                rect = pygame.Rect(player_pos.x, player_pos.y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GREEN, rect, BLOCK_SIZE)
        apple = pygame.Rect(snake.apple_pos.x, snake.apple_pos.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, apple, BLOCK_SIZE)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (snake.move.current_key_pressed != 3 or snake.score == 0):
            snake.move.up()
        elif keys[pygame.K_s] and (snake.move.current_key_pressed != 2 or snake.score == 0):
            snake.move.down()
        elif keys[pygame.K_a] and (snake.move.current_key_pressed != 1 or snake.score == 0):
            snake.move.left()
        elif keys[pygame.K_d] and (snake.move.current_key_pressed != 0 or snake.score == 0):
            snake.move.right()
        else:
            #given current_key_pressed var, execute one of the functions
            #current_key_pressed can be 0, 1, 2, 3: 0 left, 1 right, 2 up, 3 down
            if snake.move.current_key_pressed == 0:
                snake.move.left()
            elif snake.move.current_key_pressed == 1:
                snake.move.right()
            elif snake.move.current_key_pressed == 2:
                snake.move.up()
            elif snake.move.current_key_pressed == 3:
                snake.move.down()
        if snake.apple_pos in snake.player_pos_list:
            snake.update()
        drawGrid()
    else:      
        score_text, score_text_rect, play_again_text, play_again_text_rect = UI(snake.score)
        screen.blit(score_text, score_text_rect)
        screen.blit(play_again_text, play_again_text_rect)
    pygame.display.flip()

    clock.tick(60)
    time.sleep(GAME_SPEED)
pygame.quit()