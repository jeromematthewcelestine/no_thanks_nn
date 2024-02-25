import random
import numpy as np



ACTION_PASS = 0
ACTION_TAKE = 1
FIRST_CARD_ACTION = 2

class NoThanksState():
    def __init__(self, game):
        self.game = game
        
        # setup state
        self.n_cards = self.game.max_card - self.game.min_card + 1
        self.deck = [True for i in range(self.n_cards)]
        self.n_cards_left = self.n_cards - self.game.n_omit_cards

        self.player_chips = [self.game.start_chips for i in range(self.game.n_players)]
        self.player_cards = [[] for i in range(self.game.n_players)]

        self.chips_in_play = 0
        self.card_in_play = None

        self.turn_player = 0
        self.current_player = -1

    def legal_actions(self):
        if self.current_player == -1:
            if self.n_cards_left == 0:
                return []
            
            legal_actions = []
            for card_idx in range(self.n_cards):
                if self.deck[card_idx]:
                    legal_actions.append(card_idx + FIRST_CARD_ACTION)
            return legal_actions
        
        elif self.player_chips[self.turn_player] == 0:
            return [ACTION_TAKE]
        else:
            return [ACTION_TAKE, ACTION_PASS]
    
    def apply_action(self, action):
        
        if action not in self.legal_actions():
            print("ILLEGAL action:", action)
            print('legal actions:', self.legal_actions())
            print('cp:', self.current_player, 'card:', self.card_in_play, 'chips:', self.chips_in_play, ' ', self.player_chips, ' ', [cards for cards in self.player_cards])
        assert action in self.legal_actions()

        if action == ACTION_TAKE:
            self.player_cards[self.current_player].append(self.card_in_play)
            self.player_chips[self.current_player] += self.chips_in_play
            self.chips_in_play = 0
            self.card_in_play = None

            self.current_player = -1
            
        elif action == ACTION_PASS: # action == ACTION_PASS
            self.player_chips[self.current_player] -= 1
            self.chips_in_play += 1

            self.turn_player += 1
            if self.turn_player == self.game.n_players:
                self.turn_player = 0

            self.current_player = self.turn_player
        
        else: # action is card

            card = action - FIRST_CARD_ACTION
            self.card_in_play = card + self.game.min_card 
            self.deck[card] = False
            self.n_cards_left -= 1

            self.current_player = self.turn_player

    def is_terminal(self):
        if self.n_cards_left == 0 and self.card_in_play == None:
            return True
        else:
            return False
        
    def is_chance_node(self):
        return self.current_player == -1
    
    def get_scores(self):
        scores = [0 for i in range(self.game.n_players)]
        card_totals = [0 for i in range(self.game.n_players)]
        for player in range(self.game.n_players):
            cards_sorted = sorted(self.player_cards[player])
            last_card = -1
            for card in cards_sorted:
                if not card == last_card + 1:
                    card_totals[player] += card

                last_card = card

        for player in range(self.game.n_players):
            scores[player] = self.player_chips[player] - card_totals[player]

        return scores
        
    def returns(self):
        if self.n_cards_left == 0 and self.card_in_play == None:
            scores = self.get_scores()

            max_score = max(scores)
            max_scorers = [player for player in range(self.game.n_players) if scores[player] == max_score]

            if len(max_scorers) == 1:
                winner = max_scorers[0]
            else:
                most_cards = max([len(self.player_cards[player]) for player in max_scorers])
                most_card_scorers = [player for player in max_scorers if len(self.player_cards[player]) == most_cards]

                if len(most_card_scorers) == 1:
                    winner = most_card_scorers[0]
                else:
                    highest_card = self.game.min_card - 1
                    highest_card_scorer = None
                    for player in most_card_scorers:
                        for card in self.player_cards[player]:
                            if card > highest_card:
                                highest_card = card
                                highest_card_scorer = player
                    if highest_card > self.game.min_card - 1:
                        winner = highest_card_scorer
                    else:
                        winner = most_card_scorers[-1]

            return [1.0 if player == winner else -1.0 for player in range(self.game.n_players)]
            
        else:
            return [0.0 for i in range(self.game.n_players)]
        
    def to_tuple(self):
        return (self.turn_player, 
                self.current_player, 
                self.card_in_play, 
                self.chips_in_play, 
                self.n_cards_left, 
                tuple(self.player_chips), 
                tuple([tuple(cards) for cards in self.player_cards]))
    
    def to_vectors(self, from_turn_player_pov = True):

        cards_tensor = np.zeros((self.game.n_players + 1, self.n_cards), dtype=np.float32)
        start_player = self.turn_player if from_turn_player_pov else 0
        players = list(range(start_player, self.game.n_players)) + list(range(0, start_player))
        for row, player in enumerate(players):
            for card in self.player_cards[player]:
                cards_tensor[row, card - self.game.min_card] = 1.0

        if self.card_in_play != None:
            cards_tensor[-1, self.card_in_play - self.game.min_card] = 1.0

        max_chips = self.game.start_chips * self.game.n_players
        chips_tensor = np.zeros((self.game.n_players + 1), dtype=np.float32)
        for row, player in enumerate(players):
            chips_tensor[row] = self.player_chips[player] / max_chips
        chips_tensor[-1] = self.chips_in_play / max_chips

        return cards_tensor, chips_tensor

    def to_string(self):
        return f"CP:{self.current_player} TP:{self.turn_player} CP:{self.card_in_play} CH:{self.chips_in_play}, {self.player_chips}, {[cards for cards in self.player_cards]}"
        

class NoThanksGame():
    def __init__(self, named = 'custom', n_players = 3, min_card = 3, max_card = 35, start_chips = 11, n_omit_cards = 9):
        self.n_players = n_players

        if named == 'tiny':
            self.min_card = 1
            self.max_card = 5
            self.start_chips = 1
            self.n_omit_cards = 1
        elif named == 'standard':
            self.min_card = 3
            self.max_card = 35
            self.start_chips = 11
            self.n_omit_cards = 9
        else:
            self.min_card = min_card
            self.max_card = max_card
            self.start_chips = start_chips
            self.n_omit_cards = n_omit_cards

    def get_initial_state(self):
        return NoThanksState(self)

if __name__ == "__main__":
    game = NoThanksGame(n_players = 3, min_card = 1, max_card = 6, start_chips = 1, n_omit_cards = 2)
    state = game.get_initial_state()
    
    while not state.is_terminal():
        print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
        action = random.choice(state.legal_actions())
        state.apply_action(action)
    print('cp:', state.current_player, 'card:', state.card_in_play, 'chips:', state.chips_in_play, ' ', state.player_chips, ' ', [cards for cards in state.player_cards])
