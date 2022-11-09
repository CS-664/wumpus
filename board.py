class Board:
    '''

    '''

    def __init__(self):
        self.map = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    def setlocation(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                self.map[x][y] = {
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