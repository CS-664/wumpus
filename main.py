from board import *
from agent import *
import time

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
            if iniboard[n] == 'E' or iniboard[n] == 'e':
                TBoard.startx = int(iniboard[0])
                TBoard.starty = int(iniboard[1])
    return TBoard

# check the direction for current bot
def dChecker (d,a):
    if d == Directions.North:
        if a == Actions.left:
            return Directions.West
        elif a == Actions.right:
            return Directions.East
    elif d == Directions.East:
        if a == Actions.left:
            return Directions.North
        elif a == Actions.right:
            return Directions.South
    elif d == Directions.South:
        if a == Actions.left:
            return Directions.East
        elif a == Actions.right:
            return Directions.West
    elif d == Directions.West:
        if a == Actions.left:
            return Directions.South
        elif a == Actions.right:
            return Directions.North

#Print current game Board to check the location which was reached and the current location of the Bot
def boardPrinter(Board):
    for row in range(len(Board)):
        for col in range(len(Board[row])):
            if col%5 != 4:
                print(Board[row][col]+'|', end = '')
            else:
                print(Board[row][col] + '|')
        print('----------')

def main():
#    print(InitialBoard())

    gameBoard = InitialBoard()      # initializate game information
    gameAgent = KBAgent(5,5,0,0)
    gameScore = 100
    locx,locy = gameBoard.startx, gameBoard.starty
    resultBoard = [['0','0','0','0','0'],
                   ['0','0','0','0','0'],
                   ['0','0','0','0','0'],
                   ['0','0','0','0','0'],
                   ['0','0','0','0','0']]
    resultBoard[locx][locy] = '1'      # The location of "Enter" has already been reached before starting the game
    agentDirection = Directions.North               # Initional direction for bot is north
    g = 0
    while g < 10:
        actionList = gameAgent.act(gameBoard.map)
        print(actionList)

        for i in range(len(actionList)):
            if actionList[i] == Actions.left or actionList[i] == Actions.right:    # No movement, only change the current direction of the bot
                agentDirection = dChecker(agentDirection,actionList[i])
            elif actionList[i] == Actions.forward:                        # Bot have movement, mark the location on result board where it has reached by bot
                gameScore -= 1
                time.sleep(2)
                if agentDirection == Directions.North:
                    resultBoard[locx][locy] = '1'
                    locx -= 1
                    resultBoard[locx][locy] = 'B'
                elif agentDirection == Directions.East:
                    resultBoard[locx][locy] = '1'
                    locy += 1
                    resultBoard[locx][locy] = 'B'
                elif agentDirection == Directions.South:
                    resultBoard[locx][locy] = '1'
                    locx += 1
                    resultBoard[locx][locy] = 'B'
                elif agentDirection == Directions.West:
                    resultBoard[locx][locy] = '1'
                    locy -= 1
                    resultBoard[locx][locy] = 'B'
                boardPrinter(resultBoard)          # Print the Updating game board
                print(" ")            #No meaning

            elif actionList[i] == Actions.grab:                 # bot get gold, game over and break the for loop
                gameScore += 1000
                print('Bingo! You get the gold!')
                break
            elif actionList[i] == Actions.shoot:                  # No movement, but game score will be decreased because of shooting action
                print('Arrow being used!')
                gameScore -= 100

        print(gameScore)  #Print Final Score of the game

        g += 1




if __name__ == "__main__":
    main()