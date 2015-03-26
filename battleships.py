# import functions
from random import randint
from math import ceil

# define game-play functions
def print_welcome():
    print("\n\n\n\n")
    print("###################################################################")
    print("#####                 Welcome to Battleships!                 #####")
    print("###################################################################")
    print("""\nYou stumble upon a perfectly square ocean. """)


def player_chooses_board_size(): # player chooses the size of the square board (i.e. the number of rows)
    global nRows, nCols, rangeRow, rangeCol
    print("""\nIn this game you have to try to sink all of my battleships. 
My ships are hidden in a perfectly square ocean. 
How long do you want one side of this ocean to be?\n""")
    while True:
        nRows = int(input("\tChoose a number (3 - 9):"))
        if nRows >= 3 and nRows <= 9:
            break
    nCols = nRows
    rangeRow = range(nRows)
    rangeCol = range(nCols)

def create_boards(): # creates two boards (one visible and the other invisible to the player)
    global boardVisib, boardInvis
    boardVisib = []
    for x in rangeRow:
        boardVisib.append(["#"] * nCols)
    boardInvis = []
    for x in rangeRow:
        boardInvis.append(["#"] * nCols)

def calculate_size_of_board(): # calculate the number of battleships
    global nShips, nShipsLeft
    nShips = ceil(nRows * nCols / 8)
    nShipsLeft = ceil(nRows * nCols / 8)

def calculate_number_of_turns():
    global nTurns, currentTurn
    nFields = nRows * nCols
    nTurns = ceil(((nShips / (nFields - 1)) ** 0.5) * nFields * (10 + nRows) / 10)
    currentTurn = 1

def place_ships_on_board_invis():
    global rangeRow, rangeCol, boardInvis
    def randomFromRange(range):
        return randint(0, len(range) - 1)
    for ship in range(nShips):
        shipRow = randomFromRange(rangeRow)
        shipCol = randomFromRange(rangeCol)
        while boardInvis[shipRow][shipCol] == "X" or boardInvis[shipRow][shipCol] == "%":
            shipRow = randomFromRange(rangeRow)
            shipCol = randomFromRange(rangeCol)
        boardInvis[shipRow][shipCol] = "X"
        add_space_around_ships(board = boardInvis, row = shipRow, col = shipCol, symbol = "%")

def print_begin_game():
    print_title("   Let's play!   ")
    print("You have %s turns." % (nTurns))
    print("There are %s ships hiding in the ocean.\n" % (nShips))
    print_board(boardVisib)

def print_turn():
    print_title(title = (" Turn %s out of %s " % (currentTurn, nTurns)))

def player_guesses():
    global guessRow
    guessRow = -1
    global guessCol
    guessCol = -1
    while guessRow not in rangeRow:
        guessRow = int(input("\tGuess Row (1 - %s):" % (nRows))) - 1
    while guessCol not in rangeCol:
        guessCol = int(input("\tGuess Col (1 - %s):" % (nCols))) - 1

def check_guessed_already():
    global guessedAlready
    if (boardVisib[guessRow][guessCol] == "O") or (boardVisib[guessRow][guessCol] == "X"):
        guessedAlready = True
        print("\nYou guessed that one already.")
    else:
        guessedAlready = False

def check_hit_or_miss():
    if (boardInvis[guessRow][guessCol] == "X"): # Hit
        global nShipsLeft
        nShipsLeft -= 1
        if nShipsLeft > 0:
            print("\nYou sank one of my battleships!")
        edit_boards(trigger = 'Hit')
    else:
        print("\nYou missed my battleships!")
        edit_boards(trigger = 'Miss')

def calculate_next_turn_number():
    global currentTurn
    currentTurn += 1

def check_win_or_lose(): # Have all ships been sunken?
    if nShipsLeft > 0: # Lose
        print_title("    GAME OVER    ")
        if nShipsLeft == 1:
            print("\nThere is one survivor:")
        else:
            print("\nThere are a few survivors:")
        edit_boards(trigger = 'GameOver') # edit the invisible board before showing it to the player
        print_board(boardInvis)
    elif nShipsLeft == 0: # Win
        print_title("     YOU WON!     ")
        print("Congratulations! You sank all of my battleships!\n\n")

def player_wants_to_play_again():
    while True:
        playerInput = input("\tDo you want to play again? (yes or no?):").lower()
        if playerInput == "yes" or playerInput == "y":
            return True
            break
        elif playerInput == "no" or playerInput == "n":
            return False
            break

# define helper functions

def print_title(title):
    print("\n>>>>>>>>>>>>>>>>", title, "<<<<<<<<<<<<<<<<")

def print_board(board):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for row in board:
        print(" ".join(row))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

def add_space_around_ships(board, row, col, symbol): # inserts a "symbol" in all fields that boarder the ship (located with "row" and "col")
    shipSpace = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]
    for i in range(8):
        shipSpace[0][i] = row + shipSpace[0][i]
        shipSpace[1][i] = col + shipSpace[1][i]
    for i in range(8):
        if (shipSpace[0][i] in rangeRow) and (shipSpace[1][i] in rangeCol):
            board[shipSpace[0][i]][shipSpace[1][i]] = symbol

def edit_boards(trigger): 
    if trigger == 'Hit':
        boardVisib[guessRow][guessCol] = "X"
        boardInvis[guessRow][guessCol] = "O"
        # Uncover the fields on the visible board that boarder the sunken ship
        add_space_around_ships(board = boardVisib, row = guessRow, col = guessCol, symbol = "O")
    elif trigger == 'Miss':
        boardVisib[guessRow][guessCol] = "O"
        boardInvis[guessRow][guessCol] = "O"
    elif trigger == 'GameOver':   
        for row in rangeRow:
            for col in rangeCol:
                if boardInvis[row][col] == "%" or boardInvis[row][col] == "#":
                    boardInvis[row][col] = "O"
# define the game

def runGame():
    print_welcome()
    player_chooses_board_size()
    create_boards()
    calculate_size_of_board()
    calculate_number_of_turns()
    place_ships_on_board_invis()
    print_begin_game()

        # loop through the turns
    while currentTurn <= nTurns and nShipsLeft > 0:
        print_turn()
        while True:
            player_guesses()
            check_guessed_already()
            if not guessedAlready:
                break
        check_hit_or_miss()
        print_board(boardVisib)
        calculate_next_turn_number()

    check_win_or_lose()
  

############################## GAME EXECUTION #################################
while True:
    runGame()
    playAgain = player_wants_to_play_again()
    if playAgain == False:
        break
