# import functions
from random import randint
from math import ceil

# define game-play functions
def print_welcome():
    print("\n\n\n\n")
    print("###################################################################")
    print("#####                 Welcome to Battleships!                 #####")
    print("###################################################################")
    print("""\n\tIn this game you have to try to sink all of the battleships 
\tthat were randomly placed by the computer in an ocean.\n""")

def player_chooses_number_of_ships(): 
    ''' 
    The player is asked to choose the number of battleships, 
    she/he will have to sink. 
    '''
    while True:
        nShips = int(input("Choose the number of ships placed by the computer (1 - 7): "))
        if (nShips >= 1) and (nShips <= 7):
            break
    return nShips

def calculate_size_of_board(nShips): 
    '''
    Calculate the number of rows ("nRows") of the board 
    form the number of ships ("nShips").
    '''
    nFields = nShips * 8
    nRows = ceil(nFields ** 0.5)
    return nRows

def create_board(nRows, nCols):
    '''
    Create a board ("board") according to the number of rows ("nRows") 
    and columns ("nCols").
    '''
    board = []
    for x in range(nRows):
        board.append(["#"] * nCols)
    return board

def calculate_number_of_turns(nRows, nCols, nShips):
    nFields = nRows * nCols
    nTurns = ceil(((nShips / (nFields - 1)) ** 0.5) * nFields * (10 + nRows) / 10)
    return nTurns

def place_ships_on_board_invis(nShips, nRows, nCols, boardInvis):
    bI, nR, nC = boardInvis, nRows, nCols

    def randomFromRange(range):
        return randint(0, len(range) - 1)
    for ship in range(nShips):
        shipRow = randomFromRange(range(nRows))
        shipCol = randomFromRange(range(nCols))
        while (boardInvis[shipRow][shipCol] == "X") or (boardInvis[shipRow][shipCol] == "%"):
            shipRow = randomFromRange(range(nRows))
            shipCol = randomFromRange(range(nCols))
        boardInvis[shipRow][shipCol] = "X"
        add_space_around_ships(board = bI, row = shipRow, col = shipCol, symbol = "%", nRows = nR, nCols = nC)

def print_begin_game(boardVisib, nTurns, nShips):
    bV = boardVisib

    print_title("   Let's play!   ")
    print("You have %s turns." % (nTurns))
    print("There are %s ships hiding in the ocean.\n" % (nShips))
    print_board(board = bV)

def print_turn(currentTurn, nTurns):
    print_title(title = (" Turn %s out of %s " % (currentTurn, nTurns)))

def player_guesses(nRows, nCols):
    guessRow, guessCol = -1, -1
    while guessRow not in range(nRows):
        guessRow = int(input("\tGuess Row (1 - %s):" % (nRows))) - 1
    while guessCol not in range(nCols):
        guessCol = int(input("\tGuess Col (1 - %s):" % (nCols))) - 1
    return (guessRow, guessCol)

def check_guessed_already(guessRow, guessCol, boardVisib):
    if (boardVisib[guessRow][guessCol] == "O") or (boardVisib[guessRow][guessCol] == "X"):
        guessedAlready = True
        print("\nYou guessed that one already.")
    else:
        guessedAlready = False
    return guessedAlready

def check_hit_or_miss(nShipsLeft, guessRow, guessCol, boardInvis, boardVisib, nRows, nCols):
    bV, bI, gR, gC, nR, nC = boardVisib, boardInvis, guessRow, guessCol, nRows, nCols

    if (boardInvis[guessRow][guessCol] == "X"): # Hit
        shipHit = True

        nShipsLeft -= 1
        if nShipsLeft > 0:
            print("\nYou sank one of my battleships!")
        edit_boards(trigger = 'Hit', boardVisib = bV, boardInvis = bI, guessRow = gR, guessCol = gC, nRows = nR, nCols = nC)
    
    else:
        shipHit = False

        print("\nYou missed my battleships!")
        edit_boards(trigger = 'Miss', boardVisib = bV, boardInvis = bI, guessRow = gR, guessCol = gC, nRows = nR, nCols = nC)

    return shipHit

def calculate_next_turn_number(currentTurn):
    currentTurn += 1
    return currentTurn

def check_win_or_lose(nShipsLeft, boardVisib, boardInvis, guessRow, guessCol, nRows, nCols):
    bV, bI, gR, gC, nR, nC = boardVisib, boardInvis, guessRow, guessCol, nRows, nCols
    '''
    Check whether all ships have been sunken.
    '''
    if nShipsLeft > 0: # Lose
        print_title("    GAME OVER    ")
        if nShipsLeft == 1:
            print("\nThere is one survivor:")
        else:
            print("\nThere are a few survivors:")

        # edit the invisible board before showing it to the player
        edit_boards(trigger = 'GameOver', boardVisib = bV, boardInvis = bI, guessRow = gR, guessCol = gC, nRows = nR, nCols = nC)

        print_board(board = bI)
    elif nShipsLeft == 0: # Win
        print_title("     YOU WON!     ")
        print("Congratulations! You sank all of my battleships!\n\n")

def player_wants_to_play_again():
    print("\n###################################################################")
    while True:
        playerInput = input("\n\nDo you want to play again? (yes or no?):").lower()
        if (playerInput == "yes") or (playerInput == "y"):
            return True
            break
        elif (playerInput == "no") or (playerInput == "n"):
            return False
            break

# define helper functions

def print_title(title):
    print("\n\n>>>>>>>>>>>>>>>>", title, "<<<<<<<<<<<<<<<<")

def print_board(board):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for row in board:
        print(" ".join(row))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

def add_space_around_ships(board, row, col, symbol, nRows, nCols):
    '''
    Insert a "symbol" in all fields that boarder the ship. 
    The ship is located with "row" and "col".
    '''
    shipSpace = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]

    for i in range(8):
        shipSpace[0][i] = row + shipSpace[0][i]
        shipSpace[1][i] = col + shipSpace[1][i]

    for i in range(8):
        if (shipSpace[0][i] in range(nRows)) and (shipSpace[1][i] in range(nCols)):
            board[shipSpace[0][i]][shipSpace[1][i]] = symbol

def edit_boards(trigger, boardVisib, boardInvis, guessRow, guessCol, nRows, nCols):
    bV, gR, gC, nR, nC = boardVisib, guessRow, guessCol, nRows, nCols

    if trigger == 'Hit':
        boardVisib[guessRow][guessCol] = "X"
        boardInvis[guessRow][guessCol] = "O"
        # Uncover the fields on the visible board that boarder the sunken ship
        add_space_around_ships(board = bV, row = gR, col = gC, symbol = "O", nRows = nR, nCols = nC)

    elif trigger == 'Miss':
        boardVisib[guessRow][guessCol] = "O"
        boardInvis[guessRow][guessCol] = "O"

    elif trigger == 'GameOver':   
        for row in range(nRows):
            for col in range(nCols):
                if (boardInvis[row][col] == "%") or (boardInvis[row][col] == "#"):
                    boardInvis[row][col] = "O"

# define the game execution

def run_game():

    print_welcome()

    nShips = player_chooses_number_of_ships()
    nShipsLeft = nShips

    nRows = calculate_size_of_board(nShips)
    nCols = nRows

    # create two boards; one visible and one invisible to the player
    boardVisib, boardInvis = create_board(nRows, nCols), create_board(nRows, nCols)

    nTurns = calculate_number_of_turns(nRows,nCols, nShips)
    currentTurn = 1

    place_ships_on_board_invis(nShips, nRows, nCols, boardInvis)

    print_begin_game(boardVisib, nTurns, nShips)

    while (currentTurn <= nTurns) and (nShipsLeft > 0):
        '''
        Loop through each turn.
        '''
        print_turn(currentTurn, nTurns)

        while True:

            guessRow, guessCol = player_guesses(nRows, nCols)

            guessedAlready = check_guessed_already(guessRow, guessCol, boardVisib)
            if not guessedAlready:
                break

        shipHit = check_hit_or_miss(nShipsLeft, guessRow, guessCol, boardInvis, boardVisib, nRows, nCols)
        if shipHit:
            nShipsLeft -= 1

        print_board(boardVisib)

        currentTurn = calculate_next_turn_number(currentTurn)

    check_win_or_lose(nShipsLeft, boardVisib, boardInvis, guessRow, guessCol, nRows, nCols)
  

############################## GAME EXECUTION #################################

while True:

    run_game()

    playAgain = player_wants_to_play_again()
    if playAgain == False:
        break
