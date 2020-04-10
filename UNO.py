# -----------------UNO--------------------
import random

deck = []
colors = ["red", "green", "blue", "yellow"]
special_cards = ["reverse", "skip", "draw 2"]
wild_cards = ["wild", "draw 4"]
playing_deck = [["red", "2"]]


class NormalCards:
    def __init__(self, color="", number=0):
        self.color = color
        self.number = number

    def card_gen(self):
        for color in colors:
            self.color = color
            deck.append([self.color, self.number])
            for times in range(2):
                for i in range(1, 10):
                    self.number = str(i)
                    deck.append([self.color, self.number])
            self.number = 0


n_cards = NormalCards()
n_cards.card_gen()


class SpecialCards:
    def __init__(self, color="", type_=""):
        self.color = color
        self.type = type_

    def card_gen(self):
        for card in special_cards:
            for color in colors:
                for i in range(2):
                    self.color = color
                    self.type = card
                    deck.append([self.color, self.type])


sp_cards = SpecialCards()
sp_cards.card_gen()


class WildCards:
    def __init__(self, type_="wild", type2=""):
        self.type = type_
        self.type2 = type2

    def card_gen(self):
        for w in wild_cards:
            for i in range(4):
                self.type2 = w
                deck.append([self.type, self.type2])


w_cards = WildCards()
w_cards.card_gen()

# print(f'''{deck}\n{len(deck)}''')
random.shuffle(deck)
# print(''deck'')
# print("len(deck)")


def playing_deck_top():
    if len(playing_deck) > 0:
        return playing_deck[-1]
    else:
        return [[]]


class Player:
    chosen_color = None
    draw_pending = 0
    no_start_cards = int(input("\nEnter the number of cards to start with: "))
    skip = False

    def __init__(self, name="Unnamed player", card_set=[],
                 valid_cards=[], drew=0):
        self.name = name
        self.card_set = card_set
        self.valid_cards = valid_cards
        self.drew = drew

    def distribute(self):
        self.card_set = deck[:Player.no_start_cards]
        del deck[:Player.no_start_cards]

    def draw(self):
        self.card_set.append(deck[0])
        del deck[0]

    def check_valid_cards(self):
        for card in self.card_set:
            if Player.chosen_color is None:
                if card[0] == "wild":
                    self.valid_cards.append(card)
                    print(card)
                elif card[0] in playing_deck_top() or card[1] in playing_deck_top():
                    self.valid_cards.append(card)
            else:
                if card[0] == Player.chosen_color:
                    self.valid_cards.append(card)
                Player.chosen_color = None

    def play(self):
        self.drew = 0
        while not Player.skip:
            print(f'''\n\n\n{self.name} playing...''')
            for i in range(Player.draw_pending):
                self.draw()
                print("Drew 1 card")
            Player.draw_pending = 0
            while True:
                self.check_valid_cards()
                print(f'''Card being played: {playing_deck_top()}''')
                # print(f'''Your cards:\n{list(enumerate(self.card_set))}''')
                print("\nYour cards: ")
                for card in list(enumerate(self.card_set)):
                    print(card)
                choice = input("Enter the index of card you want to play"
                               "or enter d to draw 1 card."
                               "\nif no options available enter p to pass: ").lower()
                if choice.isnumeric():
                    chosen_card = self.card_set[int(choice)]
                    if chosen_card == ["wild", "draw 4"]:
                        Player.chosen_color = colors[int(input("Enter the color you want(r:0, g:1, b:2, y:3): "))]
                        playing_deck.append(chosen_card)
                        self.card_set.remove(chosen_card)
                        Player.draw_pending = 4
                        break
                    elif chosen_card[0] == "wild":
                        Player.chosen_color = colors[int(input("Enter the color you want(r:0, g:1, b:2, y:3): "))]
                        playing_deck.append(chosen_card)
                        self.card_set.remove(chosen_card)
                        break
                    elif chosen_card in self.valid_cards:
                        if chosen_card[1] == "draw 2":
                            Player.draw_pending = 2
                        elif chosen_card[1] in ["reverse"]:
                            players.reverse()
                        elif chosen_card[1] == "skip":
                            Player.skip = True
                        else:
                            pass
                        playing_deck.append(chosen_card)
                        self.card_set.remove(chosen_card)
                        break
                    else:
                        print("Sorry, you can't play that card!")
                elif choice == "d":
                    self.draw()
                    self.drew += 1
                elif choice == "p" and self.drew > 0:
                    break
                elif choice == "p" and not self.drew > 0:
                    print("\nPlease draw a card first\n")
                else:
                    print("Invalid input")
            break
        else:
            Player.skip = False

    @classmethod
    def player_gen(cls):
        no_players = int(input("\nEnter the number of players: "))
        playing = []
        for i in range(no_players):
            playing.append(Player(input(f"Enter player {i+1}'s name: ")))
        return playing


players = Player.player_gen()


def game():
    end = False
    for player in players:
        player.distribute()
    while not end:
        for player in players:
            if len(player.card_set) == 0:
                end = True
                break
            player.play()
    else:
        for player in players:
            if len(player.card_set) == 0:
                winner = player.name
                print(f'''\nThe winner is {winner}!''')
                break


game()
