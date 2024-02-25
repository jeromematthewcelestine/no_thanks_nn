import random
from dataclasses import dataclass

ACTION_TAKE = 0
ACTION_PASS = 1

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

class NoThanksState():
    def __init__(self, game):
        self.game = game
        
        # setup state
        self.n_cards = self.game.max_card - self.game.min_card + 1
        self.deck = [True for i in range(self.n_cards)]
        self.n_cards_left = self.n_cards - self.game.n_omit_cards

        self.current_player = 0

        self.chips = [self.game.start_coins for i in range(self.game.n_players)]
        self.player_cards = [[] for i in range(self.game.n_players)]

        # draw a card from the deck
        cards_in_deck = [i for i in range(self.game.min_card, self.game.max_card + 1) if self.deck[i - self.game.min_card]]
        self.card_in_play = random.choice(cards_in_deck)
        self.n_cards_left -= 1

        self.coins_in_play = 0

    def legal_actions(self):
        if self.coins[self.current_player] == 0:
            return [ACTION_PASS]
        else:
            return [ACTION_TAKE, ACTION_PASS]
    
    def apply_action(self, action):
        if action == ACTION_TAKE:
            self.cards[self.current_player].append(self.card_in_play)
            self.chips[self.current_player] += self.coins_in_play
            self.coins_in_play = 0

            if self.n_cards_left > 0:

                cards_in_deck = [i for i in range(self.game.min_card, self.game.max_card + 1) if self.deck[i - self.game.min_card]]
                self.card_in_play = random.choice(cards_in_deck)
                self.deck[self.card_in_play - self.game.min_card] = False
                self.n_cards_left -= 1

            else:
                self.card_in_play = None

        else: # action == ACTION_PASS
            self.chips[self.current_player] -= 1
            self.coins_in_play += 1

            self.current_player += 1
            if self.current_player == self.game.n_players:
                self.current_player = 0

    def is_terminal(self):
        if self.n_cards_left == 0 and self.card_in_play == None:
            return True
        else:
            return False

class NoThanksGame():
    def __init__(self, n_players = 3, min_card = 3, max_card = 35, start_coins = 11, n_omit_cards = 9):
        self.n_players = n_players

        self.min_card = min_card
        self.max_card = max_card
        self.start_coins = start_coins
        self.n_omit_cards = n_omit_cards

    def starting_state(self):
        coins = [self.config.start_coins for i in range(self.n_players)]
        cards = [[] for i in range(self.n_players)]

        card_in_play = random.choice(self.full_deck)
        
        coins_in_play = 0
        n_cards_in_deck = self.n_cards - 1 - self.n_omit_cards
        current_player = 0

        return coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player)

    def next_state(self, state, action):
        pass

    def is_legal(self, state, action):
        pass

    def legal_actions(self, state):
        pass

    def pack_state(self, state):
        coins, cards, details = state
        packed_state = tuple(coins), tuple(map(tuple, cards)), details
        return packed_state

    def unpack_state(self, packed_state):
        coins, cards, details = packed_state
        coins = list(coins)
        cards = list(map(list, cards))
        return coins, cards, details

    def is_ended(self, state):
        pass

    def compute_scores(self, state):
        pass

    def winner(self, state):
        pass

    def basic_display_state(self, state):
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        print("Coins:           {0}".format(coins))
        print("Cards:           {0}".format(cards))
        print("Card in play:    {0}".format(card_in_play))
        print("Coins:           {0}".format(coins_in_play))
        print("Player:          {0}".format(current_player))

    def display_scores(self, state):
        scores = self.compute_scores(state)
        print("")
        print("--- Scores ---")
        for i in range(self.n_players):
            print("Player {0}: {1}".format(i, scores[i]))
        print("")

    def display_state(self, state):
        state = self.unpack_state(state)
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if self.n_players == 3:
            print(""

@dataclass 
class NoThanksConfig:
    min_card: int = 3
    max_card: int = 35
    start_coins: int = 11
    n_omit_cards: int = 9

class NoThanksBoard():
    def __init__(self, n_players = 3, config = NoThanksConfig()):
        self.n_players = n_players
        
        self.start_coins = config.start_coins
        self.min_card = config.min_card
        self.max_card = config.max_card
        self.full_deck = list(range(self.min_card, self.max_card+1))
        self.n_omit_cards = config.n_omit_cards
        self.n_cards = self.max_card - self.min_card + 1

    # state: ((player coins),(player cards),(card in play, coins in play, n_cards_remaining, current player))
    def starting_state(self):
        coins = [self.start_coins for i in range(self.n_players)]
        cards = [[] for i in range(self.n_players)]

        card_in_play = random.choice(self.full_deck)
        
        coins_in_play = 0
        n_cards_in_deck = self.n_cards - 1 - self.n_omit_cards
        current_player = 0

        return coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player)

    def next_state(self, state, action):

        state = self.unpack_state(state)
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if action == ACTION_TAKE:
            cards[current_player].append(card_in_play)
            coins[current_player] += coins_in_play

            all_player_cards = [card for player_cards in cards for card in player_cards]
            cards_in_deck = diff(self.full_deck, all_player_cards)

            if cards_in_deck and n_cards_in_deck > 0:
                
                random.shuffle(list(cards_in_deck))
                card_in_play = random.choice(cards_in_deck)
                n_cards_in_deck -= 1

            else:
                card_in_play = None
            coins_in_play = 0

            

        else:
            coins[current_player] -= 1
            coins_in_play += 1
            
            current_player += 1
            if current_player == self.n_players:
                current_player = 0

        

        next_state = coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player)
        return self.pack_state(next_state)

    def is_legal(self, state, action):
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if coins[current_player] == 0 and action == ACTION_PASS:
            return False
        else:
            if card_in_play is None:
                return False
            else:
                return True

    def legal_actions(self, state):
        actions = []
        
        actions.append(ACTION_TAKE)

        if self.is_legal(state, ACTION_PASS):
            actions.append(ACTION_PASS)

        return actions

    def pack_state(self, state):
        coins, cards, details = state
        packed_state = tuple(coins), tuple(map(tuple, cards)), details
        return packed_state

    def unpack_state(self, packed_state):
        coins, cards, details = packed_state
        coins = list(coins)
        cards = list(map(list, cards))
        return coins, cards, details

    def is_ended(self, state):
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if n_cards_in_deck == 0 and card_in_play == None:
            return True
        else:
            return False

    def compute_scores(self, state):
        state = self.unpack_state(state)
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        scores = []

        for p_idx in range(self.n_players):
            cards[p_idx].sort()

            score = 0
            if cards[p_idx]:
                score += cards[p_idx][0]
                last_card = cards[p_idx][0]

                for card_idx in range(1, len(cards[p_idx])):
                    new_card = cards[p_idx][card_idx]

                    if not new_card == last_card + 1:
                        score += new_card
                    last_card = new_card

            score -= coins[p_idx]

            scores.append(score)

        return scores

    def winner(self, state):
        state = self.unpack_state(state)
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if not self.is_ended(state):
            return None
        
        scores = self.compute_scores(state)
        min_score = 1000
        lowest_scorers = []
        # get lowest scorers (could be more than one)
        for i, score in enumerate(scores):
            if score < min_score:
                lowest_scorers = [i]
                min_score = score
            if score <= min_score:
                lowest_scorers.append(i)
        
        # if players are tied on lowest score, get the one with the fewest cards
        if len(lowest_scorers) > 1:
            min_n_cards = 1000
            for i in lowest_scorers:
                n_cards = len(cards[i])
                if n_cards < min_n_cards:
                    lowest_card_players = [i]
                    min_n_cards = n_cards
                elif n_cards <= min_n_cards:
                    lowest_card_players.append(i)

            if len(lowest_card_players) > 1:
                winner = lowest_card_players[0]
            else: # if still tied, pick a random winner (not the official rules)
                winner = random.choice(lowest_card_players) 
        else:
            winners = lowest_scorers[0]

        return winner

    def basic_display_state(self, state):
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        print("Coins:           {0}".format(coins))
        print("Cards:           {0}".format(cards))
        print("Card in play:    {0}".format(card_in_play))
        print("Coins:           {0}".format(coins_in_play))
        print("Player:          {0}".format(current_player))

    def display_scores(self, state):
        scores = self.compute_scores(state)
        print("")
        print("--- Scores ---")
        for i in range(self.n_players):
            print("Player {0}: {1}".format(i, scores[i]))
        print("")

    def display_state(self, state):
        state = self.unpack_state(state)
        coins, cards, (card_in_play, coins_in_play, n_cards_in_deck, current_player) = state

        if self.n_players == 3:
            print("")
            print("-------------------------------------------------------")
            print("")
            print("--- Player 1 ---\t\t\t---Player 2 ---")
            print(" Cards: {0}".format(sorted(cards[1])))
            print("\t\t\t\t\t Cards: {0}".format(sorted(cards[2])))
            print(" Coins: {0}".format(coins[1]))
            print("\t\t\t\t\t Coins: {0}".format(coins[2]))
            print("")
            print("\t\t In play: [{0}]".format(card_in_play))
            print("\t\t   Coins: {0}".format(coins_in_play))
            print("")
            print("")
            print("--- Player 0 (You) ---")
            print(" Cards: {0}".format(sorted(cards[0])))
            print(" Coins: {0}".format(coins[0]))
            print("")
            
    def pack_action(self, notation):
        if notation == "y" or notation == "Y":
            return ACTION_TAKE
        else:
            return ACTION_PASS

    def current_player(self, state):
        return state[2][3]