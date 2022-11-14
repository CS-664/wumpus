from board import *
from agent import *

def informChecker(w):
    if w == 'G' or w == 'g':
        return 'gold'
    elif w == 'W' or w == 'w':
        return 'wumpus'
    elif w == 'B' or w == 'b':
        return 'breezy'
    elif w == 'S' or w == 's':
        return 'stench'
    elif w == 'P' or w == 'p':
        return 'pit'

def InitialBoard():
    fileObject = open('BoardInfrom.txt', "r")
    data = fileObject.read()          # Get the detail of testing board
    BoardInform = data.split()
    TBoard = Board(5,5)                 # initial game board
    for i in range(len(BoardInform)):     # Update information following given map
        iniboard = BoardInform[i].split(",")
        for n in range(2,len(iniboard)):
            TBoard.input(int(iniboard[0]),int(iniboard[1]),informChecker(iniboard[n]))
    return TBoard.map

# check the direction for current bot
def dChecker (d,a):
    if d == 1:
        if a == 1:
            return 4
        elif a == 2:
            return 2
    elif d == 2:
        if a == 1:
            return 1
        elif a == 2:
            return 3
    elif d == 3:
        if a == 1:
            return 2
        elif a == 2:
            return 4
    elif d == 4:
        if a == 1:
            return 3
        elif a == 2:
            return 1

def main():
#    print(InitialBoard())

    gameBoard = InitialBoard()      # initializate game information
    gameAgent = KBAgent(5,5,0,0)
    gameScore = 100
    actionList = gameAgent.act(gameBoard)
    locx,locy = 0,0
    resultBoard = [[0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0]]
    resultBoard[locx][locy] = 1      # The location of "Enter" has already been reached before starting the game
    agentDirection = 1               # Initional direction for bot is north



    print(gameAgent.act(gameBoard))

'''
    for i in range(len(actionList)):
        if actionList[i] == 1 or actionList[i] == 2:    # No movement, only change the current direction of the bot
            agentDirection = dChecker(agentDirection,actionList[i])
        elif actionList[i] == 3:                        # Bot have movement, mark the location on result board where it has reached by bot
            gameScore -= 1
            if agentDirection == 1:
                locx -= 1
                resultBoard[locx][locy] = 1
            elif agentDirection == 2:
                locy += 1
                resultBoard[locx][locy] = 1
            elif agentDirection == 3:
                locx += 1
                resultBoard[locx][locy] = 1
            elif agentDirection == 4:
                locy -= 1
                resultBoard[locx][locy] = 1
        elif actionList[i] == 6:                 # bot get gold, game over and break the for loop
            gameScore += 1000
            break
        elif actionList[i] == 4:                  # No movement, but game score will be decreased because of shooting action
            gameScore -= 100

    print(gameScore)
    print(resultBoard)                  #   print the result of the game
'''



if __name__ == "__main__":
    main()