'''
Import here
'''

def InitialBoard():
    fileObject = open('BoardInfrom.txt', "r")
    data = fileObject.read()          # Get the detail of testing board
    BoardInform = data.split();
    TBoard = [['','','','',''],
              ['','','','',''],
              ['','','','',''],
              ['','','','',''],
              ['','','','','']]                       # Initialize testing board
    for i in range(len(BoardInform)-1):                                      # Set Special elements into initial board
        iniboard = BoardInform[i].split(",")
        if len(iniboard) == 3:
            TBoard[int(iniboard[0])][int(iniboard[1])] = iniboard[2]
        else:
            TBoard[int(iniboard[0])][int(iniboard[1])] = iniboard[2] + ',' + iniboard[3]
    return TBoard             # return testing board


def main():
    a = InitialBoard()
    print(a)


if __name__ == "__main__":
    main()