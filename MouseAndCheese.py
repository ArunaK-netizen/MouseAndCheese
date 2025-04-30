import pygame
import sys
import random

box_width, box_height, box_margin = 50, 50, 10
screen_size = 600
learning_rate = 0.1
gamma = 0.9
epsilon = 0.1
epochs = 1000
grid_size = 10
num_walls = 17

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Q-Learning: Mouse and Cheese")
font = pygame.font.SysFont("courier-new", 12)

mouse_img = pygame.transform.scale(pygame.image.load('assets/mouse.png'), (box_width, box_height))
cheese_img = pygame.transform.scale(pygame.image.load('assets/cheese.png'), (box_width, box_height))
wall_img = pygame.transform.scale(pygame.image.load('assets/wall.png'), (box_width, box_height))

Q = {}

def moves_possible(state):
    x, y = state
    moves = []
    if x > 0: moves.append("up")
    if x < grid_size - 1: moves.append("down")
    if y > 0: moves.append("left")
    if y < grid_size - 1: moves.append("right")
    return moves

def get_next_state(state, action):
    x, y = state
    if action == 'up': x -= 1
    elif action == 'down': x += 1
    elif action == 'left': y -= 1
    elif action == 'right': y += 1
    return (x, y)

def get_reward(state):
    if state in wall_positions:
        return -100
    elif state == goal:
        return 100
    else:
        return -1

def get_random_wall_positions(grid_size, num_walls, forbidden):
    all_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)]
    valid_positions = [pos for pos in all_positions if pos not in forbidden]
    return set(random.sample(valid_positions, num_walls))

grid = []
for row in range(grid_size):
    for col in range(grid_size):
        Q[(row, col)] = {a: 0.0 for a in moves_possible((row, col))}

start = (0, 0)
goal = (grid_size - 1, grid_size - 1)
forbidden = {start, goal}
wall_positions = get_random_wall_positions(grid_size, num_walls, forbidden)

current_state = start
step_counter = 0
epoch = 0

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if epoch < epochs:
        for _ in range(10):
            possible_moves = moves_possible(current_state)
            if random.random() < epsilon:
                action = random.choice(possible_moves)
            else:
                action = max(Q[current_state], key=Q[current_state].get)

            next_state = get_next_state(current_state, action)
            reward = get_reward(next_state)

            if next_state in Q:
                max_future_q = max(Q[next_state].values())
            else:
                max_future_q = 0

            old_q = Q[current_state][action]
            Q[current_state][action] = old_q + learning_rate * (reward + gamma * max_future_q - old_q)

            if next_state in wall_positions or next_state == goal or step_counter > 50:
                current_state = start
                epoch += 1
                step_counter = 0
            else:
                current_state = next_state
                step_counter += 1

    for row in range(grid_size):
        for col in range(grid_size):
            x = col * (box_width + box_margin)
            y = row * (box_height + box_margin)
            rect = pygame.Rect(x, y, box_width, box_height)
            pygame.draw.rect(screen, (255, 255, 255), rect)

            if (row, col) == goal:
                screen.blit(cheese_img, rect)
            elif (row, col) in wall_positions:
                screen.blit(wall_img, rect)
            else:
                best_q = max(Q[(row, col)].values()) if Q[(row, col)] else 0
                q_text = font.render(f"{best_q:.1f}", True, (0, 0, 0))
                text_rect = q_text.get_rect(center=rect.center)
                screen.blit(q_text, text_rect)

    if current_state != start:
        x = current_state[1] * (box_width + box_margin)
        y = current_state[0] * (box_height + box_margin)
        screen.blit(mouse_img, pygame.Rect(x, y, box_width, box_height))

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
sys.exit()
