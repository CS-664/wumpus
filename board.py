class Board:
    '''

    '''

    def __init__(self, x, y):
        self.startx = 0
        self.starty = 0
        self.map = [[None for x in range(x)]for y in range(y)]
        for i in range(x):
            for j in range(y):
                self.map[i][j] = {
                    "gold": False,
                    "wumpus": False,
                    "breezy": False,
                    "stench": False,
                    "pit": False,

                 }

    def input(self, x, y, info):
        if info in self.map[x][y]:
            self.map[x][y][info] = True
        return self.map


'''
class Location:
    def __init__(self):
        self.gold = False
        self.wumpus = False
        self.breezy = False
        self.stench = False
        self.pit = False
'''