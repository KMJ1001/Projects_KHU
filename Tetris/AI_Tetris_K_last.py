import pygame
import random

# 게임 보드의 크기
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# 테트리스 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# 색상 정의 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# 블록 색상 매핑
SHAPE_COLORS = [CYAN, YELLOW, BLUE, ORANGE, GREEN, RED, MAGENTA]

def create_board():
    # 빈 보드 생성
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    return board

def draw_board(screen, board):
    # 보드 그리기
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            draw_block(screen, col, row, board[row][col])

def draw_block(screen, x, y, color):
    # 블록 그리기
    pygame.draw.rect(screen, SHAPE_COLORS[color], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def generate_shape():
    # 랜덤한 모양 생성
    shape = random.choice(SHAPES)
    return shape

def place_shape(board, shape, row, col, color):
    # 모양을 보드에 배치
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                board[row + i][col + j] = color

def is_collision(board, shape, row, col):
    # 충돌 체크
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] and (row + i >= BOARD_HEIGHT or col + j < 0 or col + j >= BOARD_WIDTH or board[row + i][col + j]):
                return True
    return False

def clear_rows(board):
    # 행이 꽉 찼는지 확인하고 삭제
    full_rows = []
    for i in range(BOARD_HEIGHT):
        if all(board[i]):
            full_rows.append(i)
    for row in full_rows:
        del board[row]
        board.insert(0, [0] * BOARD_WIDTH)
    return len(full_rows)

def main():
    pygame.init()

    screen = pygame.display.set_mode((BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Tetris Game")

    clock = pygame.time.Clock()

    board = create_board()
    score = 0
    game_over = False

    current_shape = generate_shape()
    current_shape_color = random.randint(0, len(SHAPE_COLORS) - 1)
    current_row, current_col = 0, BOARD_WIDTH // 2 - len(current_shape[0]) // 2

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not is_collision(board, current_shape, current_row, current_col - 1):
                        current_col -= 1
                elif event.key == pygame.K_RIGHT:
                    if not is_collision(board, current_shape, current_row, current_col + 1):
                        current_col += 1
                elif event.key == pygame.K_DOWN:
                    if not is_collision(board, current_shape, current_row + 1, current_col):
                        current_row += 1
                elif event.key == pygame.K_SPACE:
                    rotated_shape = list(zip(*reversed(current_shape)))
                    if not is_collision(board, rotated_shape, current_row, current_col):
                        current_shape = rotated_shape

        if not is_collision(board, current_shape, current_row + 1, current_col):
            current_row += 1
        else:
            place_shape(board, current_shape, current_row, current_col, current_shape_color)
            rows_cleared = clear_rows(board)
            score += rows_cleared
            current_shape = generate_shape()
            current_shape_color = random.randint(0, len(SHAPE_COLORS) - 1)
            current_row, current_col = 0, BOARD_WIDTH // 2 - len(current_shape[0]) // 2

            if is_collision(board, current_shape, current_row, current_col):
                game_over = True

        screen.fill(BLACK)
        draw_board(screen, board)
        pygame.display.flip()
        clock.tick(3)  # 블록이 떨어지는 속도 조절 (초당 블록 이동 횟수)

    print("Game Over")
    print("Your score:", score)

    pygame.quit()

# 게임 실행
if __name__ == "__main__":
    main()

