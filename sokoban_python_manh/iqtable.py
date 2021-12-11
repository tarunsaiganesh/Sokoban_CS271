import sokoban as sokoban

class IQTable:
    def Get(self, state, action): pass
    def Set(state, action, value): pass
    def Check(state): pass


class QTable(IQTable):
    def __init__(self):
        self.map = dict()

    def Get(self, state, action=None):
        if action is None:
            if state in self.map.keys():
                return self.map[state]
            else:
                return [0,0,0,0]
        else:
            if not (state in self.map.keys()):
                return 0
            if action is sokoban.Up: 
                return self.map[state][0]
            elif action is sokoban.Left:
                return self.map[state][1]
            elif action is sokoban.Right:
                return self.map[state][2]
            elif action is sokoban.Down:
                return self.map[state][3]
            return 0    
    
    def Set(self, state, action , value):
        if not (state in self.map.keys()):
            self.map[state] = [0,0,0,0]
        if action is sokoban.Up: 
            self.map[state][0] = value
            return
        elif action is sokoban.Left:
            self.map[state][1] = value
            return
        elif action is sokoban.Right:
            self.map[state][2] = value
            return
        elif action is sokoban.Down:
            self.map[state][3] = value
            return

    # def Set(self, state, row):
    #     self.map[state] = row

    def Check(self, state):
        return state in self.map.keys()

    def PrintStateRow(self, state):
        for value in self.Get(state):
            print(value, end=' ')
        print('\n')

    def PrintHeader(self):
        for d in sokoban.AllDirections:
            print(sokoban.DirectionName[d], end=' ')
        print('\n')
    
    def Print(self):
        self.PrintHeader()
        for p in self.map:
            self.PrintStateRow(p)
    
    

class CTable(IQTable):
    def __init__(self):
        self.map = dict()

    def Get(self, state, action=None):
        if action is None:
            if state in self.map.keys():
                return self.map[state]
            else:
                return [0,0,0,0]
        else:
            if not (state in self.map.keys()):
                return 0
            if action is sokoban.Up: 
                return self.map[state][0]
            elif action is sokoban.Left:
                return self.map[state][1]
            elif action is sokoban.Right:
                return self.map[state][2]
            elif action is sokoban.Down:
                return self.map[state][3]
            return 0
    
    def Set(self, state, action , value):
        if state not in self.map.keys():
            self.map[state] = [float('inf'), float('inf'), float('inf'), float('inf')]
        
        if action is sokoban.Up: 
            self.map[state][0] = min(self.map[state][0], value)
            return
        elif action is sokoban.Left:
            self.map[state][1] = min(self.map[state][1], value)
            return
        elif action is sokoban.Right:
            self.map[state][2] = min(self.map[state][2], value)
            return
        elif action is sokoban.Down:
            self.map[state][3] = min(self.map[state][3], value)
            return

    # def Set(self, state, row):
    #     self.map[state] = row

    def Check(self, state):
        return state in self.map.keys()
    
