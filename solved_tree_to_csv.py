from no_thanks import NoThanksGame, NoThanksState
from minimax import Minimaxer
import random
import numpy as np
import pandas as pd

if __name__ == "__main__":
  start_chips = 1
  game = NoThanksGame(n_players = 3,
                      min_card = 1,
                      max_card = 5,
                      start_chips = start_chips, 
                      n_omit_cards = 1)
  state = game.get_initial_state()

  minimaxer = Minimaxer()
  _, _ = minimaxer.solve_tree(state, 30)

  turn_player_list = []
  current_player_list = []
  card_in_play_list = []
  chips_in_play_list = []
  n_cards_left_list = []
  p1_cards_list = []
  p2_cards_list = []
  p3_cards_list = []
  p1_chips_list = []
  p2_chips_list = []
  p3_chips_list = []
  action_list = []
  v1_list = []
  v2_list = []
  v3_list = []

  for state in minimaxer.action_dict:
    action = minimaxer.action_dict[state]
    value = minimaxer.values_dict[state]
    
    turn_player, current_player, card_in_play, chips_in_play, n_cards_left, player_chips, player_cards = state
    turn_player_list.append(turn_player)
    current_player_list.append(current_player)
    card_in_play_list.append(card_in_play)
    chips_in_play_list.append(chips_in_play)
    n_cards_left_list.append(n_cards_left)
    p1_chips_list.append(player_chips[0])
    p2_chips_list.append(player_chips[1])
    p3_chips_list.append(player_chips[2])
    p1_cards_list.append(player_cards[0])
    p2_cards_list.append(player_cards[1])
    p3_cards_list.append(player_cards[2])

    action_list.append(action)
    v1_list.append(value[0])
    v2_list.append(value[1])
    v3_list.append(value[2])

    print(f"state: {state}, action: {action}, value: {value}")

  df = pd.DataFrame({'turn_player': turn_player_list,
                      'current_player': current_player_list,
                      'card_in_play': card_in_play_list,
                      'chips_in_play': chips_in_play_list,
                      'n_cards_left': n_cards_left_list,
                      'p1_chips': p1_chips_list,
                      'p2_chips': p2_chips_list,
                      'p3_chips': p3_chips_list,
                      'p1_cards': p1_cards_list,
                      'p2_cards': p2_cards_list,
                      'p3_cards': p3_cards_list,
                      'action': action_list,
                      'v1': v1_list,
                      'v2': v2_list,
                      'v3': v3_list})
  df.to_csv('2024-02-20_no_thanks_tree_01.csv', index=False)

    