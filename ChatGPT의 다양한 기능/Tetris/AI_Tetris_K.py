import random

# 게임 보드의 크기
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

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

def create_board():
    # 빈 보드 생성
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    return board

def print_board(board):
    # 보드 출력
    for row in board:
        for cell in row:
            print("■" if cell else "□", end=" ")
        print()
    print()

def generate_shape():
    # 랜덤한 모양 생성
    shape = random.choice(SHAPES)
    return shape

def place_shape(board, shape, row, col):
    # 모양을 보드에 배치
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                board[row + i][col + j] = 1

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

def play_game():
    board = create_board()
    score = 0
    game_over = False

    while not game_over:
        shape = generate_shape()
        row, col = 0, BOARD_WIDTH // 2 - len(shape[0]) // 2

        if is_collision(board, shape, row, col):
            game_over = True
        else:             
            while not is_collision(board, shape, row + 1, col):
                row += 1

            place_shape(board, shape, row, col)
            score += clear_rows(board)
            print_board(board)

            if is_collision(board, shape, 0, col):
                game_over = True

    print("Game Over")
    print("Your score:", score)

# 게임 실행
play_game()

           
