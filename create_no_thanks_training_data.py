from no_thanks import NoThanksGame, NoThanksState
from minimax import Minimaxer
import random
import numpy as np

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

  tensor_dict = {}
  tensors = []
  for key, value in minimaxer.state_dict.items():
    state = value
    cards_tensor, chips_tensor = state.to_vectors()

    action = minimaxer.action_dict[key]
    # this_value = actions[state.turn_player]
    
    tensor_state = np.concatenate((cards_tensor.flatten(), chips_tensor))
    tensor_combined = np.concatenate((cards_tensor.flatten(), chips_tensor, [action]))

    # make sure we don't have duplicates
    if tensor_state.tostring() not in tensor_dict and action != None:
      tensor_dict[tensor_state.tostring()] = 1
      tensors.append(tensor_combined)
    

  tensors = np.array(tensors)

  # np.savetxt('2024-02-20_no_thanks_training_data_05.csv', tensors, delimiter=',', fmt = '%.3f')


