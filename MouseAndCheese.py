import pygame
import sys
import random

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

def moves_possible(current_state, grid):
    x, y = current_state
    max_x = len(grid) - 1
    max_y = len(grid[0]) - 1
    moves = []

    if x > 0:
        moves.append("up")
    if x < max_x:
        moves.append("down")
    if y > 0:
        moves.append("left")
    if y < max_y:
        moves.append("right")

    return moves

def get_random_wall_positions(grid_size, num_walls, forbidden):
    all_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)]
    valid_positions = [pos for pos in all_positions if pos not in forbidden]
    return random.sample(valid_positions, num_walls)

def build_walls(grid, wall_positions):
    for x, y in wall_positions:
        grid[x][y].q_value = -100.00

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Cat and Cheese Grid")
    font = pygame.font.SysFont("courier-new", 10)

    grid_size = 10
    num_walls = 7

    grid = []
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            x = col * (box_width + box_margin)
            y = row * (box_height + box_margin)
            box = Box(x, y, box_width, box_height)
            grid_row.append(box)
        grid.append(grid_row)

    forbidden = {(0, 0), (grid_size-1, grid_size-1)}
    wall_positions = get_random_wall_positions(grid_size, num_walls, forbidden)
    build_walls(grid, wall_positions)

    cat_img = pygame.image.load('assets/cat.png')
    cat_img = pygame.transform.scale(cat_img, (box_width, box_height))
    cheese_img = pygame.image.load('assets/cheese.png')
    cheese_img = pygame.transform.scale(cheese_img, (box_width, box_height))
    wall_img = pygame.image.load('assets/wall.png')
    wall_img = pygame.transform.scale(wall_img, (box_width, box_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        for row in range(grid_size):
            for col in range(grid_size):
                box = grid[row][col]
                pygame.draw.rect(screen, (255, 255, 255), box)

                if (row, col) not in wall_positions and (row, col) != (0, 0) and (row, col) != (grid_size-1, grid_size-1):
                    q_value_display = font.render(str(box.q_value), True, (0, 0, 0))
                    text_rect = q_value_display.get_rect(center=box.rect.center)
                    screen.blit(q_value_display, text_rect)

                if (row, col) == (0, 0):
                    screen.blit(cat_img, box.rect)
                elif (row, col) == (grid_size-1, grid_size-1):
                    screen.blit(cheese_img, box.rect)
                elif (row, col) in wall_positions:
                    screen.blit(wall_img, box.rect)

        pygame.display.flip()
