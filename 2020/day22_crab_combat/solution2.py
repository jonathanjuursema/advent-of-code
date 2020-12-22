f = open("input.txt", "r")
initial_player_decks = f.read().split("\n\n")


class Game:
    def __init__(self, players, game_id=1, debug=False):
        self._players = players
        self._game_id = game_id
        self._debug = debug

    def play_game(self):
        debug = self._debug
        if debug:
            print("=== Game {} ===\n".format(self._game_id))
        # Start the game.
        round_no = 1
        game_over = False
        while game_over is False:
            if debug:
                print("--- Round {} (Game {}) ---".format(round_no, self._game_id))
                for player in self._players:
                    print("{}'s deck: {}".format(player.name, player.deck_string))

            recurring = [player.is_recurring for player in self._players]
            if False not in recurring:  # This situation has occurred before!
                if debug:
                    print("Recurring game detected!")
                winning_player = 0  # Player 1 is index 0.
                game_over = True
                continue

            drawn_cards = []
            for player in self._players:
                card = player.draw_card()
                if debug:
                    print("{} plays: {}".format(player.name, str(card)))
                drawn_cards.append(card)

            # For each player, check if they can play a sub-game (no. of cards in deck > card just drawn).
            can_play_subgame = [len(player.deck) >= drawn_cards[i] for i, player in enumerate(self._players)]

            # We can play a sub-game!
            if False not in can_play_subgame:
                if debug:
                    print("Playing a sub-game to determine the winner...\n")
                sub_players = [Player('Player {}'.format(i + 1), current_player.deck[:drawn_cards[i]])
                               for i, current_player in enumerate(self._players)]
                sub_game = Game(players=sub_players, game_id=self._game_id + 1, debug=debug)
                winning_player = sub_game.play_game()
                # If Player 2 wins, we need to reverse the drawn cards because their card is on the bottom of the list.
                if winning_player == 1:
                    drawn_cards = reversed(drawn_cards)

            else:
                winning_player = drawn_cards.index(max(drawn_cards))
                drawn_cards = sorted(drawn_cards, reverse=True)

            if debug:
                print("{} wins round {} of game {}!\n".format(self._players[winning_player].name, round_no,
                                                              self._game_id))

            for card in drawn_cards:
                self._players[winning_player].stow_card(card)

            for player in self._players:
                if len(player.deck) == 0:
                    game_over = True

            round_no += 1

        # Game is over!
        winning_player = 0 if len(self._players[0].deck) > 0 else 1
        if self._game_id > 1:
            if debug:
                print("The winner of game {} is player {}!".format(self._game_id, self._players[winning_player].name))
                print("\n...anyway, back to game {}.".format(self._game_id - 1))
        else:
            print("Game over!")
            for player in self._players:
                print(
                    "{}'s score: {} (Deck: {})".format(player.name, player.score, player.deck_string))
        return winning_player


class Player:
    def __init__(self, name, cards):
        self.name = name
        self._deck = cards.copy()
        self._history = []

    @property
    def deck(self):
        return self._deck.copy()

    @property
    def deck_string(self):
        return ", ".join([str(i) for i in self.deck])

    @property
    def is_recurring(self):
        return self.deck_string in self._history

    def draw_card(self):
        self._history.append(self.deck_string)
        return self._deck.pop(0)

    def stow_card(self, card):
        self._deck.append(card)

    @property
    def score(self):
        return sum([card * (len(self._deck) - i) for i, card in enumerate(self.deck)])


global_players = []
for i, initial_player_deck in enumerate(initial_player_decks):
    global_players.append(Player('Player {}'.format(i + 1), [int(c) for c in initial_player_deck.splitlines()[1:]]))

first_game = Game(players=global_players)
first_game.play_game()
