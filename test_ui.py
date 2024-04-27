import pygame

running = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,800))
font = pygame.font.Font("Helvetica.ttf", 64)
text = font.render("Hello my name is Ved", True, (0, 0, 0), (255, 255, 255))
text_rect = text.get_rect()
text_rect.center = (400, 400)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if text_rect.collidepoint(x, y):
                print("HELLO WORLD")
    screen.fill("black")
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)