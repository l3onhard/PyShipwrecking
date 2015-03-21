# import functions
from random import randint
from math import ceil

# define game-play functions
def printWelcome():
    print("###################################################################")
    print("#####                Welcome to Battleships!                  #####")
    print("###################################################################")

def playerChooseBoardSize(): # player chooses the size of the square board (i.e. the number of rows)
    global nRows, nCols, rangeRow, rangeCol
    print("\nHow big do you want the square board to be?\n")
    while True:
        nRows = int(input("Choose the number of rows (3 - 9):"))
        if nRows >= 3 and nRows <= 9:
            break
    nCols = nRows
    rangeRow = range(nRows)
    rangeCol = range(nCols)

def createBoards(): # creates two boards (one visible and the other invisible to the player)
    global boardVisib, boardInvis
    boardVisib = []
    for x in rangeRow:
        boardVisib.append(["#"] * nCols)
    boardInvis = []
    for x in rangeRow:
        boardInvis.append(["#"] * nCols)

def calculateNumberOfShips(): # calculate the number of battleships
    global nShips, nShipsLeft
    nShips = ceil(nRows * nCols / 8)
    nShipsLeft = ceil(nRows * nCols / 8)

def calculateNumberOfTurns():
    global nTurns, currentTurn
    nFields = nRows * nCols
    nTurns = ceil(((nShips / (nFields - 1)) ** 0.5) * nFields * (10 + nRows) / 10)
    currentTurn = 1

def placeShipsOnBoardInvis():
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
        shipSpacing(board = boardInvis, row = shipRow, col = shipCol, symbol = "%")

def printBeginGame():
    printTitle("   Let's play!   ")
    print("You have %s turns." % (nTurns))
    print("There are %s ships.\n" % (nShips))
    printBoard(boardVisib)

def printTurn():
    printTitle(title = (" Turn %s out of %s " % (currentTurn, nTurns)))

def playerGuess():
    global guessRow
    guessRow = -1
    global guessCol
    guessCol = -1
    while guessRow not in rangeRow:
        guessRow = int(input("Guess Row (1 - %s):" % (nRows))) - 1
    while guessCol not in rangeCol:
        guessCol = int(input("Guess Col (1 - %s):" % (nCols))) - 1

def checkGuessedAlready():
    global guessedAlready
    if (boardVisib[guessRow][guessCol] == "O") or (boardVisib[guessRow][guessCol] == "X"):
        guessedAlready = True
        print("\nYou guessed that one already.")
    else:
        guessedAlready = False

def checkHitOrMiss():
    if (boardInvis[guessRow][guessCol] == "X"): # Hit
        global nShipsLeft
        nShipsLeft -= 1
        if nShipsLeft > 0:
            print("\nYou sank one of my battleships!")
        editBoards(trigger = 'Hit')
    else:
        print("\nYou missed my battleships!")
        editBoards(trigger = 'Miss')

def calculateNextTurnNumber():
    global currentTurn
    currentTurn += 1

def checkWinOrLose(): # Have all ships been sunken?
    if nShipsLeft > 0: # Lose
        printTitle("    GAME OVER    ")
        if nShipsLeft == 1:
            print("\nThere is one survivor:")
        else:
            print("\nThere are a few survivors:")
        editBoards(trigger = 'GameOver') # edit the invisible board before showing it to the player
        printBoard(boardInvis)
    elif nShipsLeft == 0: # Win
        printTitle("     YOU WON!     ")
        print("Congratulations! You sank all of my battleships!\n\n")


# define helper functions

def printTitle(title):
    print("\n>>>>>>>>>>>>>>>>", title, "<<<<<<<<<<<<<<<<")

def printBoard(board):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for row in board:
        print(" ".join(row))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

def shipSpacing(board, row, col, symbol): # inserts a "symbol" in all fields that boarder the ship (located with "row" and "col")
    shipSpace = [[-1, 0, 1, 1, 1, 0, -1, -1], [1, 1, 1, 0, -1, -1, -1, 0]]
    for i in range(8):
        shipSpace[0][i] = row + shipSpace[0][i]
        shipSpace[1][i] = col + shipSpace[1][i]
    for i in range(8):
        if (shipSpace[0][i] in rangeRow) and (shipSpace[1][i] in rangeCol):
            board[shipSpace[0][i]][shipSpace[1][i]] = symbol

def editBoards(trigger): 
    if trigger == 'Hit':
        boardVisib[guessRow][guessCol] = "X"
        boardInvis[guessRow][guessCol] = "O"
        # Uncover the fields on the visible board that boarder the sunken ship
        shipSpacing(board = boardVisib, row = guessRow, col = guessCol, symbol = "O")
    elif trigger == 'Miss':
        boardVisib[guessRow][guessCol] = "O"
        boardInvis[guessRow][guessCol] = "O"
    elif trigger == 'GameOver':   
        for row in rangeRow:
            for col in rangeCol:
                if boardInvis[row][col] == "%" or boardInvis[row][col] == "#":
                    boardInvis[row][col] = "O"

############################## GAME EXECUTION #################################
printWelcome()
playerChooseBoardSize()
createBoards()
calculateNumberOfShips()
calculateNumberOfTurns()
placeShipsOnBoardInvis()
printBeginGame()

    # loop through the turns
while currentTurn <= nTurns and nShipsLeft > 0:
    printTurn()
    while True:
        playerGuess()
        checkGuessedAlready()
        if not guessedAlready:
            break
    checkHitOrMiss()
    printBoard(boardVisib)
    calculateNextTurnNumber()

checkWinOrLose()
