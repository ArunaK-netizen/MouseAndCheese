import pygame
import sys


box_width, box_height, box_margin = 50, 50, 10

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, box_width, box_height, q_value=0.000):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, box_width, box_height)
        self.x = x
        self.y = y
        self.width = box_width
        self.height = box_height
        self.q_value = q_value



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("courier-new", 10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        grid = []

        for row in range(10):
            for col in range(10):

                x = col * (box_width + box_margin)
                y = row * (box_height + box_margin)
                box = Box(x, y, box_width, box_height)
                pygame.draw.rect(screen, (255, 255, 255), box)
                if (row != 9 and col != 0) or (row != 0 and col != 9):
                    q_value_display = font.render(str(box.q_value), True, (0, 0, 0))
                    text_rect = q_value_display.get_rect(center=box.rect.center)
                    screen.blit(q_value_display, text_rect)

                grid.append(box)
                if (row == 0 and col == 0):
                    cat = pygame.image.load('assets/cat.png')
                    cat = pygame.transform.scale(cat, (box_width, box_height))
                    screen.blit(cat, box.rect)

                elif(row == 9 and col == 9):
                    cheese = pygame.image.load('assets/cheese.png')
                    cheese = pygame.transform.scale(cheese, (box_width, box_height))
                    screen.blit(cheese, box.rect)


        pygame.display.flip()
