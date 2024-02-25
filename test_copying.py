from no_thanks import NoThanksGame, NoThanksState
from minimax import Minimaxer
import copy

if __name__ == "__main__":
  game = NoThanksGame(n_players = 3, min_card = 3, max_card = 8, start_chips = 3, n_omit_cards = 2)
  state1 = game.get_initial_state()

  state2 = copy.deepcopy(state1)

  print(state1.to_string())
  print(state2.to_string())

  legal_actions = state1.legal_actions()
  state1.apply_action(legal_actions[0])
  print(f"action: {legal_actions[0]}")

  print(state1.to_string())
  print(state2.to_string())
