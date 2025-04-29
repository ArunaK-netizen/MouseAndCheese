import sys, pygame

size = width, height = 800, 600
black = 0, 0, 0
pygame.init()

speed = [1, 1]
screen = pygame.display.set_mode(size)
ball = pygame.image.load('intro_ball.gif')
ball_rect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            sys.exit()

    ball_rect = ball_rect.move(speed)
    if(ball_rect.left < 0 or ball_rect.right > width):
        speed[0] = -speed[0]
    elif(ball_rect.top > height or ball_rect.bottom < 0):
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ball_rect)
    pygame.display.flip()