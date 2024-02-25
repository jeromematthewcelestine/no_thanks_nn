from no_thanks import NoThanksGame, NoThanksState
from minimax import Minimaxer
import random

WIN_VALUE = 100.0

def no_thanks_score_value_fn(state, player):
    if state.is_terminal():
        returns = state.returns()

        return returns[player]
    
    else:
        scores = [x / WIN_VALUE for x in state.get_scores()]
        return scores[player]
    

if __name__ == "__main__":
    start_chips = 2
    game = NoThanksGame(n_players = 3, min_card = 1, max_card = 5, start_chips = start_chips, n_omit_cards = 1)
    state = game.get_initial_state()

    minimaxer = Minimaxer()
    # values = minimaxer.get_values(state, 10, no_thanks_score_value_fn, state.current_player)
    values, action = minimaxer.solve_tree(state, 30)
    
    print('initial values:', values)

    keys_to_print = []

    for key in minimaxer.values_dict:
        turn_player, current_player, card_in_play, chips_in_play, n_cards_left, player_chips, player_cards = key

        if (current_player == 0 and 
            len(player_cards[0]) == 0 and
            len(player_cards[1]) == 0 and
            len(player_cards[2]) == 0 and 
            player_chips[0] == start_chips):
            keys_to_print.append(key)

        if (current_player == 1 and 
            player_cards[0] == (1,) and
            player_cards[1] == () and
            player_cards[2] == () and
            player_chips[1] == start_chips):
            
            keys_to_print.append(key)

    for key in keys_to_print:
        # pass
        # print(key)
        turn_player, current_player, card_in_play, chips_in_play, n_cards_left, player_chips, player_cards = key
        print('TP:', turn_player, 'CP:', current_player, 'CRD:', card_in_play, 'CHP:', chips_in_play, 'N:', n_cards_left, ' ', player_chips, ' ', player_cards,  minimaxer.values_dict[key], minimaxer.action_dict[key])


    human_player = 0
    while not state.is_terminal():
        
        if state.current_player == human_player:
            print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
            action = int(input('Enter action: '))
        elif state.is_chance_node():
            action = random.choice(state.legal_actions())
        else:
            print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
            action = minimaxer.action_dict[state.to_tuple()]
        state.apply_action(action)
    print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
    print('returns:', state.returns())
        