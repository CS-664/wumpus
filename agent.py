import enum 

__all__ = [
    'Actions',
    'KBAgent',
    'KB',
    'Directions',
]
class Actions(enum.Enum):
   left = 1 
   right = 2
   forward = 3
   grab = 4
   release = 5
   shoot = 6

class Directions(enum.Enum):
    North = 1
    East = 2
    South = 3
    West = 4

class KBAgent:
    def __init__(self, x, y, xstart,ystart):
        self.kb = KB(xstart, ystart, x, y)# knowledge base
        self.t = 0 #time counter

    def perceive(self, gameboard):
        if gameboard[self.kb.x][self.kb.y]["stench"]:
            self.tell(self.kb.x, self.kb.y, 's')
        if gameboard[self.kb.x][self.kb.y]["breezy"]:
            self.tell(self.kb.x, self.kb.y, 'b')
        if gameboard[self.kb.x][self.kb.y]["gold"]:
            self.tell(self.kb.x, self.kb.y, 'g')
        self.kb.update()

    def act(self, gameboard):
        #print(self.kb.safe)
        #print(self.kb.pit)
        #print(self.kb.wumpus)
        self.perceive(gameboard)
        actions = self.ask()
        for action in actions:
            self.tell(0,0,action)
        return actions
    
    def tell(self, x, y, z):
        if z == 's':
            self.kb.stench[x][y] = True
        elif z == 'b':
            self.kb.breeze[x][y] = True
        elif z == 'g':
            self.kb.gold[x][y] = True
        elif z == Actions.left:
            if self.kb.dir == Directions.North:
                self.kb.dir = Directions.West
            elif self.kb.dir == Directions.West:
                self.kb.dir = Directions.South
            elif self.kb.dir == Directions.South:
                self.kb.dir = Directions.East 
            else:
                self.kb.dir = Directions.North
        elif z == Actions.right:
            if self.kb.dir == Directions.North:
                self.kb.dir = Directions.East
            elif self.kb.dir == Directions.East:
                self.kb.dir = Directions.South
            elif self.kb.dir == Directions.South:
                self.kb.dir = Directions.West
            else:
                self.kb.dir = Directions.North
        elif z == Actions.forward:
            if self.kb.dir == Directions.North:
                self.kb.x = self.kb.x - 1
            elif self.kb.dir == Directions.East:
                self.kb.y = self.kb.y + 1
            elif self.kb.dir == Directions.South:
                self.kb.x = self.kb.x + 1
            else:
                self.kb.y = self.kb.y - 1
        elif z == Actions.shoot:
            self.kb.shoot()

    def ask(self):
        k = self.kb 
        x ,y = self.kb.x, self.kb.y 
        #Gold
        if k.gold[x][y] == True:
            return [Actions.grab]
        locations = self.potential_loc()
        if len(locations) != 0:
            for loc in locations:
                return self.findPath(x,y,loc[0],loc[1])
        else:
            wx, wy = -1, -1
            for i in range(len(self.kb.safe)):
                for j in range(len(self.kb.safe[0])):
                    if self.kb.wumpus[i][j] == 1.0:
                        wx, wy = i, j
            if wx == -1:
                return []
            else:
                for loc in self.kb.neighbor(wx,wy):
                    if self.kb.safe[loc[0]][loc[1]]:
                        path = self.findPath(self.kb.x, self.kb.y, loc[0], loc[1])
                        curdir = self.kb.dir
                        for dir in path:
                            if dir == Actions.right:
                                if curdir == Directions.North:
                                    curdir = Directions.East
                                elif curdir == Directions.East:
                                    curdir = Directions.South
                                elif curdir == Directions.South:
                                    curdir = Directions.West
                                else:
                                    curdir = Directions.North
                            if dir == Actions.left:
                                if curdir == Directions.North:
                                    curdir = Directions.West
                                elif curdir == Directions.West:
                                    curdir = Directions.South
                                elif curdir == Directions.South:
                                    curdir = Directions.East
                                else:
                                    curdir = Directions.North
                        if loc[0] == wx:
                            if loc[1] == wy + 1:
                                if curdir == Directions.North:
                                    path.extend([Actions.left,Actions.shoot])
                                elif curdir == Directions.West:
                                    path.append(Actions.shoot)
                                elif curdir == Directions.East:
                                    path.extend([Actions.left,Actions.left,Actions.shoot])
                                elif curdir == Directions.South:
                                    path.extend([Actions.right,Actions.shoot])
                            else:
                                if curdir == Directions.North:
                                    path.extend([Actions.right,Actions.shoot])
                                elif curdir == Directions.East:
                                    path.append(Actions.shoot)
                                elif curdir == Directions.West:
                                    path.extend([Actions.left,Actions.left,Actions.shoot])
                                elif curdir == Directions.South:
                                    path.extend([Actions.left,Actions.shoot])
                        else:
                            if loc[0] == wx + 1:
                                if curdir == Directions.West:
                                    path.extend([Actions.right,Actions.shoot])
                                elif curdir == Directions.North:
                                    path.append(Actions.shoot)
                                elif curdir == Directions.South:
                                    path.extend([Actions.left,Actions.left,Actions.shoot])
                                elif curdir == Directions.East:
                                    path.extend([Actions.left,Actions.shoot])
                            else:
                                if curdir == Directions.East:
                                    path.extend([Actions.right,Actions.shoot])
                                elif curdir == Directions.South:
                                    path.append(Actions.shoot)
                                elif curdir == Directions.North:
                                    path.extend([Actions.left,Actions.left,Actions.shoot])
                                elif curdir == Directions.West:
                                    path.extend([Actions.left,Actions.shoot])
                        return path
                return []


    def findPath(self,startx, starty, endx, endy):
        oldPath = []
        newPath = []
        xxx = 0
        yyy = 0
        xx = startx
        yy = starty

        print(startx, starty, endx, endy)
        while not (xx == endx and yy == endy):

            if xx != endx:
                if xx+1 <= (len(self.kb.safe)) and self.kb.safe[xx+1][yy] == True and self.kb.safe[xx-1][yy] == True:
                    if xx > endx:
                        xx -= 1
                        oldPath.append(1)  # south
                    if xx < endx:
                        xx += 1
                        oldPath.append(3)  # north


                elif xx+1 <= (len(self.kb.safe)) and self.kb.safe[xx+1][yy] == True:
                    xx+=1
                    oldPath.append(3)#north


                elif self.kb.safe[xx-1][yy] == True:
                    xx-=1
                    oldPath.append(1)#south


            if yy != endy:
                if yy+1 < len(self.kb.safe[xx]) and self.kb.safe[xx][yy+1] == True and self.kb.safe[xx][yy-1] == True:
                    if yy > endy:
                        yy -= 1
                        oldPath.append(4)  # west
                    if yy < endy:
                        yy += 1
                        oldPath.append(2)  # east
                elif yy+1 < len(self.kb.safe[xx]) and self.kb.safe[xx][yy+1] == True :

                    yy+=1
                    oldPath.append(2)#east

                elif self.kb.safe[xx][yy-1] == True:
                    yy-=1

                    oldPath.append(4)#west

        curdir = self.kb.dir 
        for num in oldPath:
            if curdir == Directions.North:
                if num == 1:
                    newPath.append(Actions.forward)
                elif num == 2:
                    newPath.extend([Actions.right,Actions.forward])
                    curdir = Directions.East
                elif num == 3:
                    newPath.extend([Actions.right,Actions.right,Actions.forward])
                    curdir = Directions.South
                elif num == 4:
                    newPath.extend([Actions.left,Actions.forward])
                    curdir = Directions.West

            elif curdir == Directions.South:
                if num == 1:
                    newPath.extend([Actions.left,Actions.left,Actions.forward])
                    curdir = Directions.North
                elif num == 4:
                    newPath.extend([Actions.right,Actions.forward])
                    curdir = Directions.West
                elif num == 3:
                    newPath.append(Actions.forward)
                elif num == 2:
                    newPath.extend([Actions.left,Actions.forward])
                    curdir = Directions.East

            elif curdir == Directions.East:
                if num == 1:
                    newPath.extend([Actions.left,Actions.forward])
                    curdir = Directions.North
                elif num == 2:
                    newPath.append(Actions.forward)
                elif num == 4:
                    newPath.extend([Actions.right,Actions.right,Actions.forward])
                    curdir = Directions.West
                elif num == 3:
                    newPath.extend([Actions.right,Actions.forward])
                    curdir = Directions.South

            elif curdir == Directions.West:
                if num == 4:
                    newPath.append(Actions.forward)
                elif num == 2:
                    newPath.extend([Actions.left,Actions.left,Actions.forward])
                    curdir = Directions.East
                elif num == 3:
                    newPath.extend([Actions.left,Actions.forward])
                    curdir = Directions.South
                elif num == 1:
                    newPath.extend([Actions.right,Actions.forward])
                    curdir = Directions.North
        return newPath

    #need to implement possibility of killing wumpus to get potential loc
    def potential_loc(self):
        res = []
        for i in range(len(self.kb.safe)):
            for j in range(len(self.kb.safe[0])):
                if self.kb.safe[i][j] and not self.kb.visited[i][j]:
                    res.append([i,j])
        return res

    
class KB:
    def __init__(self, x, y, boardx, boardy):
        # -1 for unknow; 0 for False; 0-1 for probability; 1 for True
        self.wumpus = [[-1.0 for x in range(boardx)] for y in range(boardy)]
        self.pit = [[-1.0 for x in range(boardx)] for y in range(boardy)]
        self.breeze = [[False for x in range(boardx)] for y in range(boardy)]
        self.stench = [[False for x in range(boardx)] for y in range(boardy)]
        self.gold = [[False for x in range(boardx)] for y in range(boardy)]
        self.safe = [[False for x in range(boardx)] for y in range(boardy)]
        self.visited = [[False for x in range(boardx)] for y in range(boardy)]
        self.arrow = True
        self.x = x
        self.y = y
        self.dir = Directions.North
    
    def update(self):
        x, y = self.x, self.y
        if self.visited[x][y]:
            return 
        self.visited[x][y] = True
        self.safe[x][y] = True
        #Case 1: No Stench or Breeze
        #Do I need check current pit/wumpus possibility? 72 and 79
        if not self.stench[x][y] and not self.breeze[x][y]:

            if self.pit[x][y] == -1.0:
                self.pit[x][y] = 0.0
            elif self.pit[x][y] > 0.0:
                self.pit[x][y] = 0.0
                for s in self.breeze_neighbor(x,y):
                    self.cal_pit(s[0],s[1]) 

            if self.wumpus[x][y] == -1.0:
                self.wumpus[x][y] = 0.0
            elif self.wumpus[x][y] > 0.0:
                self.wumpus[x][y] = 0.0
                for s in self.stench_neighbor(x,y):
                    self.cal_wumpus(s[0],s[1])

            for loc in self.neighbor(x,y):
                nx, ny = loc[0], loc[1]
                if self.pit[nx][ny] == -1.0:
                    self.pit[nx][ny] = 0.0
                elif self.pit[nx][ny] > 0.0:
                    self.pit[nx][ny] = 0.0
                    for s in self.breeze_neighbor(nx,ny):
                        self.cal_pit(s[0],s[1]) 

                if self.wumpus[nx][ny] == -1.0:
                    self.wumpus[nx][ny] = 0.0
                elif self.wumpus[nx][ny] > 0.0:
                    self.wumpus[nx][ny] = 0.0
                    for s in self.stench_neighbor(nx,ny):
                        self.cal_wumpus(s[0],s[1])
                print()
                self.safe[loc[0]][loc[1]] = True 
        #Case 2: Stench and Breeze
        elif self.stench[x][y] and self.breeze[x][y]:
            #Probably have to check pit prob and wumpus prob of current loc
            self.locate_wumpus(x, y)
            stench_candidate = []
            breeze_candidate = []
            for loc in self.neighbor(x,y):
                nx, ny = loc[0], loc[1]
                if self.pit[nx][ny] == -1.0 or 0.0 < self.pit[nx][ny] < 1.0:
                    breeze_candidate.append([nx,ny])
                if self.wumpus[nx][ny] == -1.0 or 0.0 < self.wumpus[nx][ny] < 1.0:
                    stench_candidate.append([nx,ny])
            for i in range(len(stench_candidate)):
                self.wumpus[stench_candidate[i][0]][stench_candidate[i][1]] = 1/len(stench_candidate)
            for i in range(len(breeze_candidate)):
                self.pit[breeze_candidate[i][0]][breeze_candidate[i][1]] = 1/len(breeze_candidate)
        #Case 3: Breeze
        elif self.breeze[x][y]:
            #Probably have to check pit prob and wumpus prob of current loc
            candidate = []
            for loc in self.neighbor(x,y):
                nx, ny = loc[0], loc[1]
                if self.pit[nx][ny] == -1.0 or 0.0 < self.pit[nx][ny] < 1.0:
                    candidate.append([nx,ny])
                #clear wumpus probability
                self.wumpus[nx][ny] = 0.0 #changed
                for s in self.stench_neighbor(nx,ny):
                    self.cal_wumpus(s[0],s[1])
            for i in range(len(candidate)):
                self.pit[candidate[i][0]][candidate[i][1]] = 1/len(candidate)
        #Case 4: Stench
        elif self.stench[x][y]:
            #Probably have to check pit prob and wumpus prob of current loc
            candidate = []
            self.locate_wumpus(x, y)
            for loc in self.neighbor(x,y):
                nx, ny = loc[0], loc[1]
                if self.wumpus[nx][ny] == -1.0 or 0.0 < self.wumpus[nx][ny] < 1.0:
                    candidate.append([nx,ny])
                #clear pit probability
                self.pit[nx][ny] = 0.0 #changed
                for s in self.breeze_neighbor(nx,ny):
                    self.cal_pit(s[0],s[1])
            for i in range(len(candidate)):
                self.wumpus[candidate[i][0]][candidate[i][1]] = 1/len(candidate)
        self.checksafe(len(self.pit),len(self.pit[0]))
        
    def shoot(self):
        if self.arrow == False:
            return
        if self.dir == Directions.North:
            self.wumpus[self.x-1][self.y] = 0.0
            self.safe[self.x-1][self.y] = True
        elif self.dir == Directions.South:
            self.wumpus[self.x+1][self.y] = 0.0
            self.safe[self.x+1][self.y] = True
        elif self.dir == Directions.East:
            self.wumpus[self.x][self.y+1] = 0.0
            self.safe[self.x][self.y+1] = True
        else:
            self.wumpus[self.x][self.y-1] = 0.0
            self.safe[self.x][self.y-1] = True
        self.arrow = False  
            
    def cal_wumpus(self,x,y): 
        #recalculate the probability of wumpus around the stench
        potential_neighbor = self.neighbor(x,y)
        legal_wumpus = []
        for loc in potential_neighbor:
            nx, ny = loc[0], loc[1]
            if 0.0 < self.wumpus[nx][ny] < 1.0 or self.wumpus[nx][ny] == -1.0:
                legal_wumpus.append([nx,ny])
        for i in range(len(legal_wumpus)):
            self.wumpus[legal_wumpus[i][0]][legal_wumpus[i][1]] = 1/len(legal_wumpus)

    def cal_pit(self,x,y):
        #recalculate the probability of pit around the breeze
        potential_neighbor = self.neighbor(x,y)
        legal_pit = []
        for loc in potential_neighbor:
            nx, ny = loc[0], loc[1]
            if 0.0 < self.pit[nx][ny] < 1.0 or self.wumpus[nx][ny] == -1.0:
                legal_pit.append([nx,ny])
        for i in range(len(legal_pit)):
            self.pit[legal_pit[i][0]][legal_pit[i][1]] = 1/len(legal_pit)

    def stench_neighbor(self,x,y):
        res = []
        dir = [-1, 0, 1, 0, -1]
        for i in range(4):
            nx = x + dir[i]
            ny = y + dir[i+1]
            if 0 <= nx <= len(self.safe)-1 and 0 <= ny <= len(self.safe)-1 and self.stench[nx][ny]:
                res.append([nx, ny])
        return res

    def breeze_neighbor(self,x,y):
        res = []
        dir = [-1, 0, 1, 0, -1]
        for i in range(4):
            nx = x + dir[i]
            ny = y + dir[i+1]
            if 0 <= nx <= len(self.safe)-1 and 0 <= ny <= len(self.safe)-1 and self.breeze[nx][ny]:
                res.append([nx, ny])
        return res

    def neighbor(self,x,y):
        res = []
        dir = [-1, 0, 1, 0, -1]
        for i in range(4):
            nx = x + dir[i]
            ny = y + dir[i+1]
            if 0 <= nx <= len(self.safe)-1 and 0 <= ny <= len(self.safe)-1:
                res.append([nx, ny])
        return res
    
    def locate_wumpus(self,x,y):
        x2, y2 = -1, -1
        if 0 < x-1 < len(self.safe)-1 and 0 < y-1 < len(self.safe)-1 and self.stench[x-1][y-1]:
            x2, y2 = x-1, y-1
        elif 0 < x-1 < len(self.safe)-1 and 0 < y+1 < len(self.safe)-1 and self.stench[x-1][y+1]:
            x2, y2 = x-1, y+1
        elif 0 < x+1 < len(self.safe)-1 and 0 < y-1 < len(self.safe)-1 and self.stench[x+1][y-1]:
            x2, y2 = x+1, y-1
        elif 0 < x+1 < len(self.safe)-1 and 0 < y+1 < len(self.safe)-1 and self.stench[x+1][y+1]:
            x2, y2 = x+1, y+1
        if x2 == -1:
            return 
        else:
            if self.safe[x][y2]:
                for i in range(len(self.safe)):
                    for j in range(len(self.safe[0])):
                        self.wumpus[i][j] = 0.0
                        if self.pit[i][j] == 0.0:
                            self.safe[i][j] = True
                self.wumpus[x2][y] = 1.0
            elif self.safe[x2][y]:
                for i in range(len(self.safe)):
                    for j in range(len(self.safe[0])):
                        self.wumpus[i][j] = 0.0
                        if self.pit[i][j] == 0.0:
                            self.safe[i][j] = True
                self.wumpus[x][y2] = 1.0

    #Can be modified
    def checksafe(self,x,y):
        for i in range(x):
            for j in range(y):
                if self.pit[i][j] == 0.0 and self.wumpus[i][j] == 0.0:
                    self.safe[i][j] = True
                else:
                    self.safe[i][j] = False