from board import *
from agent import *
import os

def informChecker(w):
    if w == 'G' or 'g':
        return 'gold'
    elif w == 'W' or 'w':
        return 'wumpus'
    elif w == 'B' or 'b':
        return 'breezy'
    elif w == 'S' or 's':
        return 'stench'
    elif w == 'P' or 'p':
        return 'pit'

def InitialBoard():
    fileObject = open('BoardInfrom.txt', "r")
    data = fileObject.read()          # Get the detail of testing board
    BoardInform = data.split();
    TBoard = Board(5,5)                 # initial game board
    for i in range(len(BoardInform)):     # Update information following given map
        iniboard = BoardInform[i].split(",")
        for n in range(2,len(iniboard)):
            TBoard.input(int(iniboard[0]),int(iniboard[1]),informChecker(iniboard[n]))
    return TBoard.map



def main():
#    print(InitialBoard())

    gameBoard = InitialBoard()      # initializate game information
    gameAgent = KBAgent(5,5,0,0)
    gameScore = 100

    print(gameAgent.act())



if __name__ == "__main__":
    main()