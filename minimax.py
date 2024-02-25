import copy

class Minimaxer():
  def __init__(self):
    self.values_dict = {}
    self.action_dict = {}
    self.state_dict = {}

  def get_values(self, state, depth, value_fn, maximizing_player : int):
    if depth == 0 or state.is_terminal():
      
      values = []
      for player in range(state.game.n_players):
        values.append(value_fn(state, player))
      return values
      
    if state.is_chance_node():
      value_sums = [0 for _ in range(state.game.n_players)]
      for action in state.legal_actions():
        new_state = copy.deepcopy(state)
        new_state.apply_action(action)
        values = self.get_values(new_state, depth, value_fn, maximizing_player)
        
        for player in range(state.game.n_players):
        
          value_sums[player] += values[player]
        
      for player in range(state.game.n_players):
        value_sums[player] /= len(state.legal_actions())  

      return value_sums
    
    else:
      max_current_player_value = float('-inf')
      for action in state.legal_actions():
        new_state = copy.deepcopy(state)
        new_state.apply_action(action)
        new_values = self.get_values(new_state, depth - 1, value_fn, maximizing_player)
        current_player_value = new_values[state.current_player]
        if current_player_value > max_current_player_value:
          max_current_player_value = current_player_value
          best_action = action
          values = new_values
        
      return values
      
  def solve_tree(self, state, depth):
    
    assert depth >= 0

    state_tuple = state.to_tuple()
    
    # if state_tuple in self.values_dict and state_tuple in self.action_dict:
      # return self.values_dict[state_tuple], self.action_dict[state_tuple]

    # assert state_tuple not in self.state_dict

    if state.is_terminal():
      returns = state.returns()
      
      return returns, None

    if state.is_chance_node():
      value_sums = [0 for _ in range(state.game.n_players)]
      for action in state.legal_actions():
        new_state = copy.deepcopy(state)
        print(new_state.to_string())
        print(new_state.legal_actions())
        print(action)
        new_state.apply_action(action)
        values, _ = self.solve_tree(new_state, depth - 1)
        
        for player in range(state.game.n_players):
          value_sums[player] += values[player]
        
      for player in range(state.game.n_players):
        value_sums[player] /= len(state.legal_actions())

      self.values_dict[state_tuple] = value_sums
      self.action_dict[state_tuple] = None
      self.state_dict[state_tuple] = state

      return value_sums, None
    
    else:

      # print(state.to_string())
      new_values_dict = {}
      legal_actions = state.legal_actions()
      for action in legal_actions:
        new_state = copy.deepcopy(state)
        print(new_state.to_string())
        print(new_state.legal_actions())
        print(action)
        new_state.apply_action(action)
        new_values, _ = self.solve_tree(new_state, depth - 1)
        new_values_dict[action] = new_values
      
      max_current_player_value = float('-inf')
      best_actions = [] # not really necessary
      for action in legal_actions:
        current_player_value = new_values_dict[action][state.current_player]
        if current_player_value > max_current_player_value:
          max_current_player_value = current_player_value
          best_actions = [action]
        elif current_player_value == max_current_player_value:
          best_actions.append(action)
      
      values = new_values_dict[best_actions[0]]

      self.values_dict[state_tuple] = values
      self.action_dict[state_tuple] = best_actions
      self.state_dict[state_tuple] = state
        
      return values, best_actions
          

    

