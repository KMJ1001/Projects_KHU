import pygame
import random

# Set up the game window
pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

NEXT_X = 400  # X-coordinate of the "Next" block display area
NEXT_Y = 100  # Y-coordinate of the "Next" block display area

# Define game variables
BLOCK_SIZE = 30
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = 10, 20
PLAY_AREA_X, PLAY_AREA_Y = 50, 50
FONT_SIZE = 40
FPS = 60
SCORE = 0

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define shapes
S_SHAPE = [['.....',
            '.....',
            '..xx.',
            '.xx..',
            '.....'],
           ['.....',
            '..x..',
            '..xx.',
            '...x.',
            '.....']]
Z_SHAPE = [['.....',
            '.....',
            '.xx..',
            '..xx.',
            '.....'],
           ['.....',
            '..x..',
            '.xx..',
            '.x...',
            '.....']]
I_SHAPE = [['..x..',
            '..x..',
            '..x..',
            '..x..',
            '.....'],
           ['.....',
            '.....',
            'xxxx.',
            '.....',
            '.....']]
O_SHAPE = [['.....',
            '.....',
            '.xx..',
            '.xx..',
            '.....']]
J_SHAPE = [['.....',
            '.x...',
            '.xxx.',
            '.....',
            '.....'],
           ['.....',
            '..xx.',
            '..x..',
            '..x..',
            '.....'],
           ['.....',
            '.....',
            '.xxx.',
            '...x.',
            '.....'],
           ['.....',
            '..x..',
            '..x..',
            '.xx..',
            '.....']]
L_SHAPE = [['.....',
            '...x.',
            '.xxx.',
            '.....',
            '.....'],
           ['.....',
            '..x..',
            '..x..',
            '..xx.',
            '.....'],
           ['.....',
            '.....',
            '.xxx.',
            '.x...',
            '.....'],
           ['.....',
            '.xx..',
            '..x..',
            '..x..',
            '.....']]
T_SHAPE = [['.....',
            '..x..',
            '.xxx.',
            '.....',
            '.....'],
           ['.....',
            '..x..',
            '..xx.',
            '..x..',
            '.....'],
           ['.....',
            '.....',
            '.xxx.',
            '..x..',
            '.....'],
           ['.....',
            '..x..',
            '.xx..',
            '..x..',
            '.....']]

SHAPES = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE]

def get_new_block():
    """Create a new block with a random shape and color"""
    shape = random.choice(SHAPES)
    color = random.choice([RED, GREEN, BLUE, YELLOW])
    block = {"shape": shape, "color": color, "x": int(PLAY_AREA_WIDTH / 2), "y": 0, "rotation": 0}
    return block

def draw_text(text, font, color, x, y):
    """Draw text on the screen"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    WIN.blit(text_surface, text_rect)

def draw_block(x, y, color):
    """Draw a block on the screen"""
    pygame.draw.rect(WIN, color, (PLAY_AREA_X + x * BLOCK_SIZE, PLAY_AREA_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_play_area(play_area):
    """Draw the play area on the screen"""
    for y, row in enumerate(play_area):
        for x, color in enumerate(row):
            if color:
                draw_block(x, y, color)

def get_rotated_shape(shape, rotation):
    """Rotate the shape by the given amount"""
    return shape[rotation % len(shape)]

def is_valid_position(play_area, block, offset):
    """Check if the block is in a valid position"""
    for y, row in enumerate(get_rotated_shape(block["shape"], block["rotation"])):
        for x, value in enumerate(row):
            if value == "x":
                if x + block["x"] + offset < 0 or x + block["x"] + offset >= PLAY_AREA_WIDTH:
                    return False
                if y + block["y"] >= PLAY_AREA_HEIGHT or play_area[y + block["y"]][x + block["x"] + offset]:
                    return False
    return True

def add_block_to_play_area(play_area, block):
    """Add the block to the play area"""
    for y, row in enumerate(get_rotated_shape(block["shape"], block["rotation"])):
        for x, value in enumerate(row):
            if value == "x":
                play_area[y + block["y"]][x + block["x"]] = block["color"]

def remove_complete_rows(play_area):
    """Remove any complete rows and update the score"""
    global SCORE
    new_play_area = []
    num_complete_rows = 0
    for row in play_area:
        if not all(row):
            new_play_area.append(row)
        else:
            SCORE += 10
            num_complete_rows += 1
    for _ in range(num_complete_rows):
        new_play_area.insert(0, [0] * PLAY_AREA_WIDTH)
    return new_play_area

def game_over(play_area):
    """Check if the game is over"""
    return any(play_area[0])

def main():
    """Main function for running the game"""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)

    play_area = [[0] * PLAY_AREA_WIDTH for _ in range(PLAY_AREA_HEIGHT)]
    block = get_new_block()
    next_block = get_new_block()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move the block down
        if is_valid_position(play_area, block, 0):
            block["y"] += 1
        else:
            add_block_to_play_area(play_area, block)
            play_area = remove_complete_rows(play_area)
            if game_over(play_area):
                draw_text("Game Over", font, RED, WIDTH / 2, HEIGHT / 2)
                pygame.display.update()
                pygame.time.wait(2000)
                main()
            block = next_block
            next_block = get_new_block()

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and is_valid:
            (play_area, block, -1)
        if keys[pygame.K_RIGHT] and is_valid_position(play_area, block, 1):
            move_block(play_area, block, 1)
        if keys[pygame.K_DOWN] and is_valid_position(play_area, block, 0):
            block["y"] += 1

        # Rotate the block
        if keys[pygame.K_UP]:
            rotated_shape = get_rotated_shape(block["shape"], block["rotation"] + 1)
            if is_valid_position(play_area, {"x": block["x"], "y": block["y"], "shape": rotated_shape, "color": block["color"], "rotation": block["rotation"] + 1}, 0):
                block["rotation"] += 1
                block["shape"] = rotated_shape

        # Clear the screen and draw the play area and block
        WIN.fill(BLACK)
        draw_play_area(play_area)
        for y, row in enumerate(get_rotated_shape(block["shape"], block["rotation"])):
            for x, value in enumerate(row):
                if value == "x":
                    draw_block(block["x"] + x, block["y"] + y, block["color"])

        # Draw the score and the next block
        draw_text(f"Score: {SCORE}", font, WHITE, 50, 20)
        draw_text("Next:", font, WHITE, NEXT_X, NEXT_Y - 30)
        for y, row in enumerate(get_rotated_shape(next_block["shape"], next_block["rotation"])):
            for x, value in enumerate(row):
                if value == "x":
                    draw_block(NEXT_X + x, NEXT_Y + y, next_block["color"])

        # Update the screen
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    main()