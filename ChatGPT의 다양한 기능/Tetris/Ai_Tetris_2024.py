import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Function to draw a shape on the grid
def draw_shape(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        (position[0] + x) * GRID_SIZE,
                        (position[1] + y) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )

# Function to check if a move is valid
def is_valid_move(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if (
                cell
                and (
                    position[0] + x < 0
                    or position[0] + x >= GRID_WIDTH
                    or position[1] + y >= GRID_HEIGHT
                )
            ):
                return False
    return True

# Function to rotate a shape
def rotate(shape):
    return [list(row) for row in zip(*reversed(shape))]

# Main game loop
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 1  # Increase for faster falling
current_shape = random.choice(SHAPES)
current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Handle user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and is_valid_move(current_shape, [current_position[0] - 1, current_position[1]]):
            current_position[0] -= 1
        if keys[pygame.K_RIGHT] and is_valid_move(current_shape, [current_position[0] + 1, current_position[1]]):
            current_position[0] += 1
        if keys[pygame.K_DOWN] and is_valid_move(current_shape, [current_position[0], current_position[1] + 1]):
            current_position[1] += 1
        if keys[pygame.K_UP]:
            rotated_shape = rotate(current_shape)
            if is_valid_move(rotated_shape, current_position):
                current_shape = rotated_shape

    # Update game state
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time > 1000 / fall_speed:
        if is_valid_move(current_shape, [current_position[0], current_position[1] + 1]):
            current_position[1] += 1
        else:
            # Lock the shape in place
            for y, row in enumerate(current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        screen.set_at(
                            (
                                (current_position[0] + x) * GRID_SIZE,
                                (current_position[1] + y) * GRID_SIZE,
                            ),
                            WHITE,
                        )

            # Check for completed lines and clear them
            for y in range(GRID_HEIGHT):
                if all(screen.get_at((x * GRID_SIZE, y * GRID_SIZE)) == WHITE for x in range(GRID_WIDTH)):
                    for yy in range(y, 0, -1):
                        for x in range(GRID_WIDTH):
                            screen.set_at(
                                (x * GRID_SIZE, yy * GRID_SIZE),
                                screen.get_at((x * GRID_SIZE, (yy - 1) * GRID_SIZE)),
                            )

            # Spawn a new shape
            current_shape = random.choice(SHAPES)
            current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]

        fall_time = 0

    # Draw the game
    screen.fill(BLACK)
    draw_grid()
    draw_shape(current_shape, current_position)

    # Update the display
    pygame.display.flip()
