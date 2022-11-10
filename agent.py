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
    def __init__(self, x, y, board_size):
        self.kb = KB(x, y, board_size)# knowledge base
        self.t = 0 #time counter

    def perceive(self):
        curloc = self.loc 
        if curloc.stench:
            self.tell(curloc.x, curloc.y, 's')
        if curloc.breeze:
            self.tell(curloc.x, curloc.y, 'b')
        if curloc.glitter:
            self.tell(curloc.x, curloc.y, 'g')
        self.kb.update()

    def act(self):
        self.perceive()
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
        if self.gold[x][y] == True:
            return [Actions.grab]
        locations = self.potential_loc()
        if len(locations) != 0:
            for loc in locations:
                return self.findPath(x,y,loc[0],loc[1])
        else:
            #Find and kill wumpus
            return []


    def findPath(self,startx, starty, endx, endy):
        return [] 

    #need to implement possibility of killing wumpus to get potential loc
    def potential_loc(self):
        res = []
        for i in range(len(self.kb.safe)):
            for j in range(len(self.kb.safe[0])):
                if self.kb.safe[i][j] and not self.kb.visited[i][j]:
                    res.append([i,j])
        return res

    
class KB:
    def __init__(self, x, y, board_size):
        # -1 for unknow; 0 for False; 0-1 for probability; 1 for True
        self.wumpus = [[-1.0 for x in range(board_size)] for y in range(board_size)]
        self.pit = [[-1.0 for x in range(board_size)] for y in range(board_size)]
        self.breeze = [[False for x in range(board_size)] for y in range(board_size)]
        self.stench = [[False for x in range(board_size)] for y in range(board_size)]
        self.gold = [[False for x in range(board_size)] for y in range(board_size)]
        self.safe = [[False for x in range(board_size)] for y in range(board_size)]
        self.visited = [[False for x in range(board_size)] for y in range(board_size)]
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
        self.checksafe(len(self.pit),len(self.pit[0]))
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

                self.safe[loc[0]][loc[1]] = True 
        #Case 2: Stench and Breeze
        elif self.stench[x][y] and self.breeze[x][y]:
            #Probably have to check pit prob and wumpus prob of current loc
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
                if 0.0 < self.wumpus[nx][ny] < 1.0:
                    self.wumpus[nx][ny] = 0.0
                    for s in self.stench_neighbor(nx,ny):
                        self.cal_wumpus(s[0],s[1])
            for i in range(len(candidate)):
                self.pit[candidate[i][0],candidate[i][1]] = 1/len(candidate)
        #Case 4: Stench
        elif self.stench[x][y]:
            #Probably have to check pit prob and wumpus prob of current loc
            candidate = []
            for loc in self.neighbor(x,y):
                nx, ny = loc[0], loc[1]
                if self.wumpus[nx][ny] == -1.0 or 0.0 < self.wumpus[nx][ny] < 1.0:
                    candidate.append([nx,ny])
                #clear pit probability
                if 0.0 < self.pit[nx][ny] < 1.0:
                    self.pit[nx][ny] = 0.0
                    for s in self.breeze_neighbor(nx,ny):
                        self.cal_pit(s[0],s[1])
            for i in range(len(candidate)):
                self.wumpus[candidate[i][0],candidate[i][1]] = 1/len(candidate)
        
    def shoot(self):
        if self.arrow == False:
            return
        if self.dir == Directions.North:
            self.wumpus[self.x-1][y] = 0.0
        elif self.dir == Directions.South:
            self.wumpus[self.x+1][y] = 0.0
        elif self.dir == Directions.East:
            self.wumpus[self.x][y+1] = 0.0
        else:
            self.wumpus[self.x][y-1] = 0.0
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
            if 0 <= nx <= len(self.loc)-1 and 0 <= ny <= len(self.loc)-1:
                res.append([nx, ny])
        return res
    
    #Can be modified
    def checksafe(self,x,y):
        for i in range(x):
            for j in range(y):
                if self.pit[i][j] == 0.0 and self.wumpus[i][j] == 0.0:
                    self.safe[i][j] = True