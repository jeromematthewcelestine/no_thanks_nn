from no_thanks import NoThanksGame, NoThanksState
from no_thanks_nn import NoThanksNN
import random
import torch
import numpy as np

if __name__ == '__main__':
  model = NoThanksNN(100)
  model.load_state_dict(torch.load('2024-02-19_no_thanks_nn_03.pth'))
  model.eval()
  print(model)

  game = NoThanksGame(n_players = 3, min_card = 1, max_card = 5, start_chips = 1, n_omit_cards = 1)
  state = game.get_initial_state()

  while not state.is_terminal():
    print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])

    if state.is_chance_node():
      legal_actions = state.legal_actions()
      action = random.choice(legal_actions)
      state.apply_action(action)

    elif state.current_player == 0:
      action = int(input('Enter action: '))
      state.apply_action(action)

    else:

      cards_tensor, chips_tensor = state.to_vectors()
    
      tensor_combined = np.concatenate((cards_tensor.flatten(), chips_tensor))
      input_t = torch.tensor([tensor_combined], dtype=torch.float32)
      # print(f"Input shape: {input.size()}")
      # print(f"Input: {input}")

      output = model(input_t)
      print(f"Predicted output: {output}")
      # print(f"Predicted output shape: {output.size()}")

      if output > 0.5:
        action = 1
      else:
        action = 0
      print(f"Predicted action: {action}")

      state.apply_action(action)
  
  print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
