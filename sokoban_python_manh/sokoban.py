IsWall = -1
IsFloor = 0
IsGoal = 1
IsBox = 2
IsBoxOnGoal = 3
IsPlayer = 4
IsPlayerOnGoal = 5

int_to_char = {IsWall: '#', IsFloor: '.', IsGoal: '$', IsBox: '&', IsBoxOnGoal: 'G', IsPlayer: '*', IsPlayerOnGoal: '+'}

NoDirection = 0
Up = 1
Left = 2
Right = 3
Down = 4
AllDirections = [Up, Left, Right, Down]
DirectionName = {NoDirection: 'N/A', Up: 'Up', Left: 'Left', Right: 'Right', Down: 'Down'}

class Game:

    def __init__(self, StateBits, maze):
        # print("in init")
        # print(maze)
        self.StateBits = StateBits
        self.Maze = []
        self.maze = maze
        self.Finished = 0 
        self.Succeded = False
        self.Failed = False
        self.GoalPos = set()
        self.BoxPos0 = set()
        self.BoxPos = set()
        # self.FloorIndex = []
        self.TimeElapsed = 0
        self.PlayerPos = (-1, -1)
        self.StateHistory = set()
        self.path = []
        self.State = bin(0)
        self.Directions = []
        while(len(maze) > 0 and maze[0] == '\n'):
            maze.pop(0)
        
        while(len(maze) > 0 and maze[-1] == '\n'):
            maze.pop(-1)
        floor = []
        self.PlayerPos0 = (-1, -1)
        line = 0
        col = -1
        self.Height = 1
        self.Width = 0
    
        for m in maze:
            if m == '\r':
                pass    
            elif m == '\n':
                line += 1
                col = -1
                if line >= 125:
                    # print('Maze too large')
                    return 
                if line >= self.Height:
                    self.Height = line + 1
            else:
                col += 1 
                if col >= 125:
                    print('Maze too large')
                    return 
                if col >= self.Width:
                    self.Width = col + 1
                if m == '.':
                    floor.append((line, col))
                elif m == '*':
                    floor.append((line, col))
                    if self.PlayerPos0[0] + self.PlayerPos0[1] >= 0:
                        print("Too many players")   
                        return 
                    self.PlayerPos0 = (line, col)
                elif m == '$':
                    floor.append((line, col))
                    self.GoalPos.add((line, col))   
                elif m == '&':
                    floor.append((line, col))
                    self.BoxPos0.add((line, col))
                elif m == '+':
                    floor.append((line, col))
                    if self.PlayerPos0[0] + self.PlayerPos0[1] >= 0:
                        print("Too many players")
                        return
                    self.PlayerPos0 = (line, col)
                    self.GoalPos.add((line, col))
                elif m == 'G':
                    floor.append((line, col))
                    self.BoxPos0.add((line, col))
                    self.GoalPos.add((line, col))
        
        if self.PlayerPos0[0] + self.PlayerPos0[1] == -2:
            print("No player")
            return
        if len(self.BoxPos0) == 0:
            print("No box")
            return
        if len(self.BoxPos0) > len(self.GoalPos):
            print("Too few goals")
        
        self.FloorBits = 0 
        floor_remain = len(floor) - 1
        while floor_remain > 0:
            self.FloorBits += 1
            floor_remain >>= 1
        
        if self.FloorBits * (len(self.BoxPos0) + 1) > self.StateBits:
            print("Maze too large")
            return
        
        self.FloorIndex = [[IsWall for j in range(self.Width)] for i in range(self.Height)]
        index = -1
        while len(floor) > 0:
            p = floor[0]
            index += 1 
            self.FloorIndex[p[0]][p[1]] = index
            floor.pop(0)

        # for r in self.FloorIndex:
        #     print(r)        
        self.DoRestart() 

          
    def DoRestart(self):
        self.TimeElapsed = 0
        self.StateHistory.clear()
        self.PlayerPos = self.PlayerPos0[0], self.PlayerPos0[1]
        self.BoxPos = self.BoxPos0.copy()
        self.path.clear()
        self.UpdateData()

    def UpdateData(self):
        self.Maze.clear()
        # print("after clear Maze")
        # print(self.GetMazeString())
        self.Maze = [[IsWall for j in range(self.Width)] for i in range(self.Height)]
        # print("initlize Maze")
        # print(self.GetMazeString())
        self.Finished = 0
        for i in range(self.Height):
            for j in range(self.Width):
                if self.FloorIndex[i][j] >= 0: 
                    self.Maze[i][j] = IsFloor
        # print("fill floors")
        # print(self.GetMazeString())
        for i in self.GoalPos:
            if self.Maze[i[0]][i[1]] is not IsWall:
                self.Maze[i[0]][i[1]] = IsGoal
        
        self.State = self.FloorIndex[self.PlayerPos[0]][self.PlayerPos[1]]
        offset = 0
        for i in self.BoxPos:
            if self.Maze[i[0]][i[1]] is not IsWall:
                self.Maze[i[0]][i[1]] += IsBox
                if self.Maze[i[0]][i[1]] == IsBoxOnGoal:
                    self.Finished += 1
            
            offset += 1
            self.State |= (self.FloorIndex[i[0]][i[1]]) << self.FloorBits * offset
        
        self.Maze[self.PlayerPos[0]][self.PlayerPos[1]] += IsPlayer
        # print("after fill Maze")
        # print(self.GetMazeString())
        self.Directions.clear()
        for d in AllDirections:
            if self.CheckDirection(d, self.PlayerPos[0], self.PlayerPos[1], True):
                self.Directions.append(d)
        self.Succeded = (self.Finished == len(self.BoxPos0))
        self.Failed = self.CheckFailed()

    def CheckDirection(self, direction, line, col, can_push_box):
        movement = self.Movement(direction)
        if not self.CheckFloor(line + movement[0], col + movement[1]):
            return False
        if self.Maze[line +movement[0]][col + movement[1]] == IsBox or self.Maze[line +movement[0]][col + movement[1]] == IsBoxOnGoal:
            if can_push_box:
                if not self.CheckDirection(direction, line + movement[0], col + movement[1], False):
                    return False
            else:
                return False
        return True

    def CheckFloor(self, line, col):
        if (line >= 0 and line < self.Height and col >= 0 and col < self.Width):
            return self.FloorIndex[line][col] >= 0 
        return False  

    def Movement(self, direction):
        if direction == Up:
            return (-1, 0)
        elif direction == Left:
            return (0, -1)
        elif direction == Right:
            return (0, 1)
        elif direction == Down:
            return (1, 0)
        else:
            return (0, 0)

    def CheckFailed(self):       
        if self.Finished == len(self.BoxPos0): return False
        if len(self.Directions) == 0: return True
        for b in self.BoxPos:
            vis = set()
            vis.clear()
            stuck_vertical = self.BoxStuck(b[0], b[1], False, vis)
            vis.clear()
            stuck_horizontal= self.BoxStuck(b[0], b[1], True, vis)
            if self.Maze[b[0]][b[1]] != IsBoxOnGoal:
                if stuck_vertical and stuck_horizontal: 
                    return True
                if stuck_vertical:
                    stuck = False
                    if not self.CheckFloor(b[0]-1, b[1]):
                        stuck = stuck or self.WallStuck(b[0], b[1], Down)
                    if not self.CheckFloor(b[0]+1, b[1]):
                        stuck = stuck or self.WallStuck(b[0], b[1], Up)
                    if stuck:
                        return True
                if stuck_horizontal:
                    stuck = False
                    if not self.CheckFloor(b[0], b[1]-1):
                        stuck = stuck or self.WallStuck(b[0], b[1], Right)
                    if not self.CheckFloor(b[0], b[1]+1):
                        stuck = stuck or self.WallStuck(b[0], b[1], Left)
                    if stuck:
                        return True

        vis = set()
        if not self.CanPushAny(self.PlayerPos[0], self.PlayerPos[1], vis):
            return True
        return False

    def BoxStuck(self, line, col, is_horizontal, vis):
        current = ((line, col), is_horizontal)
        if current in vis:
            vis.remove(current)
            return True
        vis.add(current)
        ret = False
        if is_horizontal:
            ret = (not self.CheckFloor(line, col - 1)) or (not self.CheckFloor(line, col + 1)) or ((self.Maze[line][col-1] == IsBox or self.Maze[line][col-1] == IsBoxOnGoal) and (self.BoxStuck(line, col - 1, not is_horizontal, vis))) or ((self.Maze[line][col+1] == IsBox or self.Maze[line][col+1] == IsBoxOnGoal) and (self.BoxStuck(line, col + 1, not is_horizontal, vis))) 
        else:
            ret = (not self.CheckFloor(line - 1, col)) or (not self.CheckFloor(line + 1, col)) or ((self.Maze[line-1][col] == IsBox or self.Maze[line-1][col] == IsBoxOnGoal) and (self.BoxStuck(line - 1, col, not is_horizontal, vis))) or ((self.Maze[line+1][col] == IsBox or self.Maze[line+1][col] == IsBoxOnGoal) and (self.BoxStuck(line + 1, col, not is_horizontal, vis))) 

        if current in vis:
            vis.remove(current)
        return ret


    def WallStuck(self, line, col, side):
        box_count = 1 if (self.Maze[line][col] == IsBox or self.Maze[line][col] == IsBoxOnGoal) else 0
        goal_count = 1 if (self.Maze[line][col] == IsGoal or self.Maze[line][col] == IsBoxOnGoal) else 0
        movement = self.Movement(side)
        if side == Up or side == Down:
            p = col-1
            while self.CheckFloor(line, p):
                if(self.CheckFloor(line-movement[0], p)):
                    return False
                if(self.Maze[line][p] == IsBox or self.Maze[line][p] == IsBoxOnGoal):
                    box_count += 1
                if(self.Maze[line][p] == IsGoal or self.Maze[line][p] == IsBoxOnGoal):
                    goal_count += 1
                p -= 1
            p = col+1
            while self.CheckFloor(line, p):
                if(self.CheckFloor(line-movement[0], p)):
                    return False
                if(self.Maze[line][p] == IsBox or self.Maze[line][p] == IsBoxOnGoal):
                    box_count += 1
                if(self.Maze[line][p] == IsGoal or self.Maze[line][p] == IsBoxOnGoal):
                    goal_count += 1
                p += 1
        else:
            p = line-1
            while self.CheckFloor(p, col):
                if(self.CheckFloor(p, col-movement[1])):
                    return False
                if(self.Maze[p][col] == IsBox or self.Maze[p][col] == IsBoxOnGoal):
                    box_count += 1
                if(self.Maze[p][col] == IsGoal or self.Maze[p][col] == IsBoxOnGoal):
                    goal_count += 1
                p -= 1
            p = line+1
            while self.CheckFloor(p, col):
                if(self.CheckFloor(p, col-movement[1])):
                    return False
                if(self.Maze[p][col] == IsBox or self.Maze[p][col] == IsBoxOnGoal):
                    box_count += 1
                if(self.Maze[p][col] == IsGoal or self.Maze[p][col] == IsBoxOnGoal):
                    goal_count += 1
                p += 1
        return box_count > goal_count    

    def CanPushAny(self, line, col, vis):    
        p = (line, col)
        if p in vis:
            return False
        vis.add(p)
        ret = False
        for d in AllDirections:
            movement = self.Movement(d)
            tmp = self.CanPushAny(line+movement[0], col+movement[1], vis) if self.CheckDirection(d, line, col, False) else self.CheckDirection(d, line, col, True)
            ret = ret or tmp
        return ret

    def DoMove(self, direction):
        if len(self.Directions) == 0 or direction not in self.Directions:
            return False
        movement = self.Movement(direction)
        if movement[0] == movement[1]:
            return False
        self.TimeElapsed += 1
        self.StateHistory.add(self.State)

        self.PlayerPos = (self.PlayerPos[0] + movement[0], self.PlayerPos[1] + movement[1])
        pushed = False
        if self.PlayerPos in self.BoxPos:
            self.BoxPos.remove(self.PlayerPos)
            self.BoxPos.add((self.PlayerPos[0] + movement[0], self.PlayerPos[1] + movement[1]))
            pushed = True
        self.path.append(DirectionName[direction])
        self.UpdateData()
        return pushed

    def GetManhattanDistance(self, direction):
        if len(self.Directions) == 0 or direction not in self.Directions:
            return float('inf')
        movement = self.Movement(direction)
        if movement[0] == movement[1]:
            return float('inf')
        
        PlayerPos_new = self.PlayerPos[0] + movement[0], self.PlayerPos[1] + movement[1]
        boxPos_new = self.BoxPos.copy()
        if PlayerPos_new in boxPos_new:
            boxPos_new.remove(PlayerPos_new)
            boxPos_new.add((PlayerPos_new[0] + movement[0], PlayerPos_new[1] + movement[1]))

        sum_ = 0
        for box in boxPos_new:
            min_ = float('inf')
            for goal in self.GoalPos:
                manhDist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                min_ = min(min_, manhDist)
            sum_ += min_
        
        return sum_
    
    def MazeString(self):
        ret = ""
        for row in self.Maze:
            for c in row:
                ret += int_to_char[c]
            ret += "\n"
        return ret[:-1]

    def GetSucceeded(self):
        return self.Succeded
    
    def GetFailed(self):
        return self.Failed

    def GetDirections(self):
        return self.Directions
    
    def GetHeight(self):
        return self.Height

    def GetWidth(self):
        return self.Width

    def GetFloorBits(self):
        return self.FloorBits
    
    def GetFinished(self):
        return self.Finished

    def GetState(self):
        return self.State

    def GetTimeElapsed(self):
        return self.TimeElapsed

    def GetPlayerPos0(self):
        return self.PlayerPos0

    def GetPlayerPos(self):
        return self.PlayerPos

    def GetBoxPos0(self):
        return self.BoxPos0

    def GetBoxPos(self):
        return self.BoxPos

    def GetGoalPos(self):
        return self.GoalPos

    def GetMaze(self):
        return self.Maze

    def GetFloorIndex(self):
        return self.FloorIndex

    def GetStateHistory(self):
        return self.StateHistory

    def GetMazeString(self):
        return self.MazeString()

    def Restart(self):
        self.DoRestart()
    
    def Move(self, direction):
        return self.DoMove(direction)

    def ManhDist(self, direction):
        return self.GetManhattanDistance(direction)

    def getPathToGoal(self):
        return self.path


    
    
    
    
    

