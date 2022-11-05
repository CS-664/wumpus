class Actions(enum.Enum):
   left = 1
   right = 2
   forward = 3
   grab = 4
   release = 5
   shoot = 6

class KBAgent:
    def __init__(self,loc, board_size):
        self.kb = KB(board_size)# knowledge base
        self.t = 0 #time counter
        self.loc = loc 
        self.score = 0 #Gold +1000, Death -1000, Step -1, Shoot -10
        self.arrow = True

    def perceive(self):
        curloc = self.loc 
        if curloc.stench:
            self.tell(curloc.x, curloc.y, 's')
        if curloc.breeze:
            self.tell(curloc.x, curloc.y, 'b')
        if curloc.glitter:
            self.tell(curloc.x, curloc.y, 'g')

    def act(self):
        self.perceive()
        self.kb.update()
        action = self.ask()
        self.tell()
        return action
    
    def tell(self, x, y, z):
        if z == 's':
            self.kb.stench[x][y] = True
        elif z == 'b':
            self.kb.breeze[x][y] = True
        elif z == 'g':
            self.kb.breeze[x][y] = True 

    def ask(self):
        return 0
    
class KB:
    def __init__(self, board_size):
        self.wumpus = [[0 for x in range(board_size)] for y in range(board_size)]
        self.pit = [[0 for x in range(board_size)] for y in range(board_size)]
        self.breeze = [[0 for x in range(board_size)] for y in range(board_size)]
        self.stench = [[False for x in range(board_size)] for y in range(board_size)]
        self.gold = [[0 for x in range(board_size)] for y in range(board_size)]
    
    def update(self):
        