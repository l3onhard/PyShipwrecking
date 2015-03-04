# importing functions
from random import randint
from math import ceil

# letting the player choose the size of the board
n_rows = int(raw_input("Number of rows:"))
n_cols = int(raw_input("Number of columns:"))

# letting the player choose the number of battleships
n_ships = 0
while n_ships >= n_rows * n_cols or n_ships <= 0:
    n_ships = int(raw_input("Number of battleships (1 - %s):" % ((n_rows * n_cols) - 1)))

# calculating the number of turns
n_fields = n_rows * n_cols
n_turns = int(ceil(((float(n_ships) / float(n_fields - 1)) ** 0.5) * n_fields))

# generating the board
board = []
row_range = range(n_rows)
col_range = range(n_cols)

for x in row_range:
    board.append(["#"] * n_cols)
    
def print_board(board):
    print "~~~~~~~~~~"
    for row in board:
        print " ".join(row)
    print "~~~~~~~~~~"

board_pc = []
for x in row_range:
    board_pc.append(["#"] * n_cols)

# beginning the game
print "Let's play Battleship!"
print "You have %s turns." % (n_turns)
print_board(board)

# generating the ships
def random_row(board_range):
    return randint(0, len(row_range) - 1)
def random_col(board_range):
    return randint(0, len(col_range) - 1)

for ship in range(n_ships):
    ship_row = random_row(row_range)
    ship_col = random_col(col_range)
    while board_pc[ship_row][ship_col] == "X":
        ship_row = random_row(row_range)
        ship_col = random_col(col_range)
    board_pc[ship_row][ship_col] = "X"

# game-play objects and functions
turn = 0

ships_left = n_ships

def print_turn():
    print ""
    print ">>>>>>>>>> Turn %s <<<<<<<<<<" % (turn + 1)

def request_guess():
    global guess_row
    global guess_col
    guess_row = int(raw_input("Guess Row (1 - %s):" % (n_rows))) - 1
    guess_col = int(raw_input("Guess Col (1 - %s):" % (n_cols))) - 1

def hit_or_miss():
    if (board_pc[guess_row][guess_col] == "X"):
        global ships_left
        ships_left -= 1
        if ships_left > 0:
            print "You sunk one of my battleships!"
            board[guess_row][guess_col] = "X"
            board_pc[guess_row][guess_col] = "O"
            print_board(board)
    else:
        print "You missed my battleships!"
        board[guess_row][guess_col] = "O"
        print_board(board)

def check_guess():
    if (guess_row not in row_range)\
    or (guess_col not in col_range):
        print "Oops, that's not even in the ocean."
    elif (board[guess_row][guess_col] == "O")\
    or (board[guess_row][guess_col] == "X"):
        print "You guessed that one already."
    else:
        global turn
        turn += 1
        hit_or_miss()

# looping through the turns
while turn < n_turns and ships_left > 0:
    print_turn()
    request_guess()
    check_guess()

# ending the game
if ships_left == 0:
    print "Congratulations! You sunk all of my battleships!"
    board[guess_row][guess_col] = "X"
    print_board(board)
elif turn == n_turns:
    print ""
    print ">>>>>>>>>> GAME OVER <<<<<<<<<<"
    print_board(board_pc)
