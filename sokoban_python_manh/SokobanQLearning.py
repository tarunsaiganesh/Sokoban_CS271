import sokoban as sokoban

class TrainResult:
    def __init__(self, last_state, old_row, action=sokoban.NoDirection, reward=0, pushed=False, new_row=None):
        if new_row is None:
            new_row = old_row

        self.Action = action
        self.LastState = last_state
        self.Reward = reward
        self.OldRow = old_row
        self.NewRow = new_row
        self.Pushed = pushed
        

    def FindAction(self,  _random, epsilon, game, Q, CostTable):
        actions  = game.GetDirections()
        if len(actions) == 0: return sokoban.NoDirection
        state = game.GetState()
        all_same = True
        action_count = 1
        action_remain = len(actions) - 1
        last_action = actions[0]
        current_action =  actions[-1]

        last_Q = Q.Get(state, last_action)
        current_Q = Q.Get(state, current_action)
        max_Q = last_Q
        choice  = actions[0]

        if action_remain == 0:
            print("singel action: ", sokoban.DirectionName[actions[0]])
            return actions[0]

        while action_remain > 0:
            action_count += 1
            all_same = all_same and last_Q and current_Q

            manhattan_cur = game.ManhDist(current_action)
            manhattan_last = game.ManhDist(last_action)
            CostTable.Set(state, last_action, game.GetTimeElapsed()+1)
            CostTable.Set(state, current_action, game.GetTimeElapsed()+1)
            cost_last = CostTable.Get(state, last_action)
            cost_cur = CostTable.Get(state, current_action)
            if current_Q - 5*manhattan_cur - 5*cost_cur > max_Q - 5*manhattan_last - 5*cost_last:
                max_Q = current_Q
                choice = current_action
            action_remain -= 1
            last_action = current_action
            last_Q = current_Q
            current_action = actions[action_remain]
            current_Q = Q.Get(state, current_action)

        random_temp = _random.uniform(0, 1)
        if all_same or random_temp < epsilon:
            random_choice = _random.randint(0, action_count-1)
            choice = actions[random_choice]
            return choice
        else:
            return choice
        # random_choice = _random.randint(0, action_count-1)
        # print("action: ", sokoban.DirectionName[actions[random_choice]] )
        # return actions[random_choice]


    def Train(self, _random, game, Q, CostTable, epsilon, alpha, gamma, retrace_penalty, push_reward,  
    goal_reward, failure_penalty, success_reward):
        last_state = game.GetState()
        old_row = Q.Get(last_state)
        if game.GetSucceeded() or game.GetFailed():
            game.Restart()
            # return TrainResult(last_state, old_row)
            return
        
        last_finished = game.GetFinished()
        last_action = self.FindAction(_random, epsilon, game, Q, CostTable)
        pushed = game.Move(last_action)
        state = game.GetState()
        reward = goal_reward * (game.GetFinished() - last_finished)
        if state in game.GetStateHistory():
            reward -= retrace_penalty
        if pushed: 
            reward += push_reward
        if game.GetSucceeded():
            reward += success_reward
        if game.GetFailed():
            reward -= failure_penalty
        actions = game.GetDirections()
        max_Q = -(retrace_penalty + failure_penalty + goal_reward* len(game.GetBoxPos0()))
        for d in actions:
            max_Q = max(max_Q, Q.Get(state, d))

        Q.Set(last_state, last_action, (1-alpha)*Q.Get(last_state, last_action) + alpha*(reward + gamma*max_Q))
        # return TrainResult(last_state, old_row, last_action, reward, pushed, Q.Get(last_state))
        return


    def Print(self):
        if self.Action == sokoban.NoDirection:
            return 
        for d in sokoban.AllDirections:
            print(sokoban.DirectionName[d], end=' ')
        print('\n')

        for value in self.OldRow:
            print(value, end=' ')
        print('\n')

        for value in self.NewRow:
            print(value, end=' ')
        print('\n')
        

