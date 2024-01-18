import pygame
import random

# 초기화
pygame.init()
clock = pygame.time.Clock()

# 게임 창 설정
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris Game")

# 블록 색깔
block_colors = {
    "I": (135, 206, 235),   # 하늘색
    "J": (0, 0, 255),       # 파란색
    "L": (255, 140, 0),     # 주황색
    "S": (50, 205, 50),     # 연두색
    "Z": (255, 0, 0)        # 빨간색
}

# 게임 실행 변수
running = False
score = 0

# 게임 상태 변수
game_over = False
game_started = False

# 블록 크기
block_size = 30

# 게임 보드
board_width = 10
board_height = 20
board = [[0] * board_width for _ in range(board_height)]

# 블록 모양
block_shapes = {
    "I": [
        [1, 1, 1, 1]
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1]
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1]
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0]
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1]
    ]
}

# 게임 보드 초기화
board = [[0] * board_width for _ in range(board_height)]

# 현재 블록
current_block = {
    "shape": None,
    "x": 0,
    "y": 0
}

# 타이틀 화면
def show_title_screen():
    window.fill((0, 0, 0))
    font = pygame.font.Font(None, 60)
    title_text = font.render("Tetris Game", True, (255, 255, 255))
    start_text = font.render("Press Spacebar to Start", True, (255, 255, 255))
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
    window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, 300))
    pygame.display.update()

# 새로운 블록 생성
def create_new_block():
    global current_block
    current_block["shape"] = block_shapes[random.choice(list(block_shapes.keys()))]
    current_block["x"] = window_width // 2 - block_size // 2
    current_block["y"] = 0

# 충돌 검사 함수
def check_collision():
    for row in range(len(current_block["shape"])):
        for col in range(len(current_block["shape"][0])):
            if (
                current_block["shape"][row][col]
                and (
                    current_block["y"] // block_size + row >= board_height
                    or current_block["x"] // block_size + col < 0
                    or current_block["x"] // block_size + col >= board_width
                    or board[current_block["y"] // block_size + row][current_block["x"] // block_size + col] != 0
                )
            ):
                return True
    return False


# 떨어지는 블록 그리기
def draw_falling_block():
    for row in range(len(current_block["shape"])):
        for col in range(len(current_block["shape"][0])):
            if current_block["shape"][row][col]:
                pygame.draw.rect(
                    window,
                    block_colors[current_block["shape"]],
                    (
                        current_block["x"] + col * block_size,
                        current_block["y"] + row * block_size,
                        block_size,
                        block_size,
                    ),
                )

# 게임 보드 그리기
def draw_board():
    for row in range(board_height):
        for col in range(board_width):
            if board[row][col]:
                pygame.draw.rect(
                    window,
                    block_colors["I"],
                    (
                        col * block_size,
                        row * block_size,
                        block_size,
                        block_size,
                    ),
                )

# 행 제거
def remove_rows():
    rows_to_remove = []
    for row in range(board_height):
        if all(board[row]):
            rows_to_remove.append(row)

    for row in rows_to_remove:
        del board[row]
        board.insert(0, [0] * board_width)

    return len(rows_to_remove)

# 게임 루프
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                    running = True
                    create_new_block()

    if not game_started:
        show_title_screen()
        pygame.display.update()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if running:
            # 블록 이동
            current_block["y"] += block_size

            # 충돌 검사
            if check_collision():
                # 블록이 바닥에 도달한 경우
                for row in range(len(current_block["shape"])):
                    for col in range(len(current_block["shape"][0])):
                        if current_block["shape"][row][col]:
                            board[current_block["y"] // block_size + row][current_block["x"] // block_size + col] = 1

                # 행 제거 및 점수 증가
                num_rows_removed = remove_rows()
                score += num_rows_removed

                # 새로운 블록 생성
                create_new_block()

                # 게임 종료 검사
                if check_collision():
                    running = False
                    game_over = True

            # 화면 지우기
            window.fill((0, 0, 0))

            # 떨어지는 블록 그리기
            draw_falling_block()

            # 게임 보드 그리기
            draw_board()

            # 스코어 표시
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            window.blit(score_text, (10, 10))

            # 게임 속도 조절
            clock.tick(10)

            pygame.display.update()

pygame.quit()
