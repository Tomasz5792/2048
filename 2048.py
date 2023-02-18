import random
import copy

# Tempory filled board
# board = [
#    [0, 0, 2, 2],
#    [2, 2, 4, 0],
#    [4, 0, 0, 4],
#    [0, 2, 0, 0]
# ]


board_size = 4


# display function
def display():
    largest = board[0][0]

    for row in board:
        for column in row:
            if column > largest:
                largest = column

    number_spaces = len(str(largest))

    for row in board:
        current_row = '!'
        for column in row:
            if column == 0:
                current_row += ' ' * number_spaces + '!'
            else:
                current_row += ' ' * (number_spaces - len(str(column))) + str(column) + '!'
        print(current_row)
    print()


# Move left function
def merge_left_one_row(row):
    for number_columns in range(board_size - 1):
        for column in range(board_size - 1, 0, -1):
            if row[column - 1] == 0:
                row[column - 1] = row[column]
                row[column] = 0

    for column in range(board_size - 1):
        if row[column] == row[column + 1]:
            row[column] *= 2
            row[column + 1] = 0

    for column in range(board_size - 1, 0, -1):
        if row[column - 1] == 0:
            row[column - 1] = row[column]
            row[column] = 0

    return row


def merge_left(current_board):
    for row in range(board_size):
        current_board[row] = merge_left_one_row(current_board[row])

    return current_board


# Reverse function
def reverse(row):
    new = []
    for column in range(board_size - 1, -1, -1):
        new.append(row[column])
    return new


def merge_right(current_board):
    for row in range(board_size):
        current_board[row] = reverse(current_board[row])
        current_board[row] = merge_left_one_row(current_board[row])
        current_board[row] = reverse(current_board[row])
    return current_board


# Transpose function
def transpose(current_board):
    for row in range(board_size):
        for column in range(row, board_size):
            if not column == row:
                temp = current_board[row][column]
                current_board[row][column] = current_board[column][row]
                current_board[column][row] = temp
    return current_board


def merge_up(current_board):
    current_board = transpose(current_board)
    current_board = merge_left(current_board)
    current_board = transpose(current_board)
    return current_board


def merge_down(current_board):
    current_board = transpose(current_board)
    current_board = merge_right(current_board)
    current_board = transpose(current_board)
    return current_board


# Generate 2 or 4 1/8 4
def pick_new_value():
    if random.randint(1, 8) == 1:
        return 4
    else:
        return 2


def add_new_value():
    row_number = random.randint(0, board_size-1)
    column_number = random.randint(0, board_size - 1)

    while not board[row_number][column_number] == 0:
        row_number = random.randint(0, board_size - 1)
        column_number = random.randint(0, board_size - 1)

    board[row_number][column_number] = pick_new_value()


def won():
    for row in board:
        if 2048 in row:
            return True
    return False


def no_moves():
    temp_board_1 = copy.deepcopy(board)
    temp_board_2 = copy.deepcopy(board)
    temp_board_1 = merge_left(temp_board_1)
    if temp_board_1 == temp_board_2:
        temp_board_1 = merge_up(temp_board_1)
        if temp_board_1 == temp_board_2:
            temp_board_1 = merge_right(temp_board_1)
            if temp_board_1 == temp_board_2:
                temp_board_1 = merge_down(temp_board_1)
                if temp_board_1 == temp_board_2:
                    return True
    else:
        return False


# Create blank board
board = []
for i in range(board_size):
    row = []
    for j in range(board_size):
        row.append(0)
    board.append(row)


# Add 2 values to random location
num_needed = 2
while num_needed > 0:
    row_number = random.randint(0, board_size-1)
    column_number = random.randint(0, board_size - 1)

    if board[row_number][column_number] == 0:
        board[row_number][column_number] = pick_new_value()
        num_needed -= 1


print('2048\n')


display()

game_over = False

while not game_over:
    move = input('Which way do you want to merge?')

    valid_input = True

    # Create a copy
    temp_board = copy.deepcopy(board)

    if move == 'a':
        board = merge_left(board)
    elif move == 'w':
        board = merge_up(board)
    elif move == 'd':
        board = merge_right(board)
    elif move == 's':
        board = merge_down(board)
    else:
        valid_input = False

    if not valid_input:
        print('Your input was not valid')
    else:
        if board == temp_board:
            print('Try a different direction.')
        else:
            if won():
                display()
                print('You won.')
                game_over = True
            else:
                add_new_value()
                display()
                if no_moves():
                    print('No moves.')
                    game_over = True
