import random
import pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

# Set up the game variables
clock = pygame.time.Clock()
BLOCK_SIZE = 30
BLOCK_COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0)]
shapes = [[[1, 1, 1], [0, 1, 0]], [[2, 2], [2, 2]], [[3, 0], [3, 3], [0, 3]], [[0, 4, 4], [4, 4, 0]], [[5, 5, 0], [0, 5, 5]], [[6, 6, 6, 6]], [[7, 7], [7, 7]]]
shape_positions = {'x': 5, 'y': 0}
current_shape = random.choice(shapes)
next_shape = random.choice(shapes)

# Define the game functions
def draw_board(board):
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            pygame.draw.rect(game_display, BLOCK_COLORS[block], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
def check_collision(board, shape, position):
    for y, row in enumerate(shape):
        for x, block in enumerate(row):
            if block:
                if (y + position['y'] >= len(board) or x + position['x'] < 0 or x + position['x'] >= len(board[0]) or
                        board[y + position['y']][x + position['x']]):
                    return True
    return False

            
def rotate_shape(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

def create_board():
    return [[0 for x in range(10)] for y in range(20)]

def remove_rows(board):
    new_board = [row for row in board if 0 not in row]
    rows_removed = len(board) - len(new_board)
    return [[0 for x in range(10)]] * rows_removed + new_board
    
def get_new_shape():
    global next_shape
    current_shape = next_shape
    next_shape = random.choice(shapes)
    return current_shape

def main():
    global current_shape
    board = create_board()
    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, current_shape, {'x': shape_positions['x'] - 1, 'y': shape_positions['y']}):
                        shape_positions['x'] -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, current_shape, {'x': shape_positions['x'] + 1, 'y': shape_positions['y']}):
                        shape_positions['x'] += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(board, rotated_shape, shape_positions):
                                                current_shape = rotated_shape
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current_shape, {'x': shape_positions['x'], 'y': shape_positions['y'] + 1}):
                        shape_positions['y'] += 1

        # Update the game state
        if check_collision(board, current_shape, {'x': shape_positions['x'], 'y': shape_positions['y'] + 1}):
            for y, row in enumerate(current_shape):
                for x, block in enumerate(row):
                    if block:
                        board[y + shape_positions['y']][x + shape_positions['x']] = block
            board = remove_rows(board)
            current_shape = get_new_shape()
            shape_positions['x'] = 5
            shape_positions['y'] = 0
            if check_collision(board, current_shape, shape_positions):
                game_over = True
        else:
            shape_positions['y'] += 1

        # Draw the game
        game_display.fill((255, 255, 255))
        draw_board(board)
        for y, row in enumerate(next_shape):
            for x, block in enumerate(row):
                pygame.draw.rect(game_display, BLOCK_COLORS[block], (WINDOW_WIDTH - 150 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        clock.tick(30)

    # Quit the game
    pygame.quit()

if __name__ == '__main__':
    main()

