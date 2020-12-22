f = open("input.txt", "r")
player_decks = f.read().split("\n\n")


class Player:
    def __init__(self, raw_input):
        raw_lines = raw_input.splitlines()
        player_name = raw_lines.pop(0)
        self.name = player_name.replace(":", "")
        self._deck = []
        for line in raw_lines:
            self._deck.append(int(line))

    @property
    def deck(self):
        return self._deck.copy()

    def draw_card(self):
        return self._deck.pop(0)

    def stow_card(self, card):
        self._deck.append(card)

    @property
    def score(self):
        return sum([card * (len(self._deck) - i) for i, card in enumerate(self.deck)])


players = []
for player_deck in player_decks:
    players.append(Player(player_deck))

# Start the game.
round_no = 1
game_over = False
while game_over is False:
    print("--- Round {} ---".format(round_no))
    for player in players:
        print("{}'s deck: {}".format(player.name, ", ".join([str(c) for c in player.deck])))

    drawn_cards = []
    for player in players:
        card = player.draw_card()
        print("{} plays: {}".format(player.name, str(card)))
        drawn_cards.append(card)

    winning_card = max(drawn_cards)
    winning_player = drawn_cards.index(winning_card)
    print("{} wins the round!\n".format(players[winning_player].name))

    drawn_cards = sorted(drawn_cards, reverse=True)
    for card in drawn_cards:
        players[winning_player].stow_card(card)

    for player in players:
        if len(player.deck) == 0:
            game_over = True

    round_no += 1

# Game is over!
print("Game over!")
for player in players:
    print("{}'s score: {} (Deck: {})".format(player.name, player.score, ", ".join([str(c) for c in player.deck])))
