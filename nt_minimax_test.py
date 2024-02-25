from no_thanks import NoThanksGame, NoThanksState
from minimax import Minimaxer
import copy
import random

if __name__ == "__main__":
  game = NoThanksGame(n_players = 3, min_card = 3, max_card = 8, start_chips = 3, n_omit_cards = 2)
  state = game.get_initial_state()
  
  legal_actions = state.legal_actions()

  minimaxer = Minimaxer()

  # for action in legal_actions:
  #   new_state = copy.deepcopy(state)
  #   new_state.apply_action(action)
  
  #   values, actions = minimaxer.solve_tree(new_state, 30)

  #   print(f"Initial state: {action}, values: {values}, actions: {actions}")

  while not state.is_terminal():
    cip_str = '_' if state.card_in_play == None else state.card_in_play
    print('cp:', state.current_player, 'card:', cip_str, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
    
    if state.is_chance_node():
      action = random.choice(state.legal_actions())
    else:
      state_copy = copy.deepcopy(state)
      values, actions = minimaxer.solve_tree(state_copy, 30)
      
      print(f"actions: ", actions)
      if len(actions) > 1:
        action = random.choice(actions)
        print(f"random action: {action}")
    
    state.apply_action(action)

  print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
  print('scores: ', state.get_scores())
  print('returns: ', state.returns())