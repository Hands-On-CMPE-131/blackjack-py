import random


class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()  #create/reset the deck of cards
        self.reset_hands()  #reset player and dealer hands
        self.player_turn = True  #set player's turn to true
        self.dealer_turn = True  #set dealer's turn to true
        self.money = 100  #starting money
        self.minimum_bet = 25  #minimum bet
        self.bet = 0  #current bet
        self.game_count = 0  #tracks the number of games played (when count is 5 cards reset)

    def create_deck(self):
        return [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4 #single deck

    def reset_hands(self):
        self.player_hand = []  #player hand
        self.dealer_hand = []  #dealer hand

    def deal_card(self, hand):
        card = random.choice(self.deck)  #choose a random card
        hand.append(card)  #add card to hands
        self.deck.remove(card)  #remove added card from deck
        return card

    def calculate_total(self, hand):
        total = 0
        face_cards = {'J': 10, 'Q': 10, 'K': 10}  #set facecards to 10
        ace_count = 0 #knows how many aces in hand (can calc whether it is going to be 1 or 11)

        for card in hand:
            if isinstance(card, int):  #if its a number card add card value to total
                total += card
            elif card in face_cards:  #if its a face card add 10 to total
                total += face_cards[card]
            elif card == 'A':  #add ace to hand not a value yet (ace can be 1 or 11)
                ace_count += 1

        #ace can be 1 or 11 based on total hand value
        for _ in range(ace_count):
            if total + 11 > 21: #if hand is less than 11 then ace = 21
                total += 1
            else:
                total += 11#if hand is more than 11 then ace = 21

        return total

    def format_hand(self, hand, hide_second_card=False):
        if hide_second_card and len(hand) > 1: #for dealers hand, format (shown card), ?(hidden card)
            return f"{hand[0]}, ?"
        return ', '.join(str(card) for card in hand)

    def first_deal(self):
        #deals the first set of cards 2 to player 2 to dealer
        for _ in range(2):
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)

    def place_bet(self):
        #start w $100, min bet $25
        while True:
            print(f"You have ${self.money}. Minimum bet is ${self.minimum_bet}.")
            try:
                self.bet = int(input("Place your bet: $"))
                if self.bet >= self.minimum_bet and self.bet <= self.money:
                    self.money -= self.bet  #subtract bet from the players money when bettiong
                    print(f"You bet ${self.bet}. You now have ${self.money} left.")
                    break
                else:
                    #bet input validation
                    print(f"Invalid bet! Bet must be at least ${self.minimum_bet} and no more than ${self.money}.")
            except ValueError:
                print("Please enter a valid amount.")

    def check_blackjack(self):
        #check if players first two cards are blackjack, as long as dealers shown card is not an ace or face card
        player_total = self.calculate_total(self.player_hand)
        dealer_first_card = self.dealer_hand[0]

        #check if player has blackjack
        if player_total == 21:
            print(f"\nPlayer: {self.format_hand(self.player_hand)} = {player_total}")
            print(f"Dealer: {self.format_hand(self.dealer_hand, hide_second_card=True)}")
            #dealer cannot match player's blackjack if not one of these cards below
            if dealer_first_card not in ['A', 'J', 'Q', 'K', 10]:
                print("Player has Blackjack! Player Wins!")
                self.money += self.bet * 2  #player wins off first turn (player = bj && dealer != bj = instant win)
                print(f"You win ${self.bet * 2}! You now have ${self.money}.")
                return True
        return False

    def player_turn_logic(self):
        #shows player his turn
        while self.player_turn:
            print(f"Player: {self.format_hand(self.player_hand)} = {self.calculate_total(self.player_hand)}")
            print(f"Dealer: {self.format_hand(self.dealer_hand, hide_second_card=True)}")
            choice = input("1: Hit\n2: Stay\n")
            if choice == '1':  #player chooses hit
                self.deal_card(self.player_hand)
                #stop if player hand >= 21
                if self.calculate_total(self.player_hand) >= 21:
                    self.player_turn = False
            elif choice == '2':  #player chooses stay
                self.player_turn = False
            else:
                print("Invalid input. Please enter 1 for Hit or 2 for Stay.") #input validation for turn

    def dealer_turn_logic(self):
        while self.calculate_total(self.dealer_hand) < 17:  #dealer must stop at all 17s
            self.deal_card(self.dealer_hand)

    def calculate_winner(self):
        #calculate winner and bet(money)
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        print(f"\nPlayer: {self.format_hand(self.player_hand)} = {player_total}")
        print(f"Dealer: {self.format_hand(self.dealer_hand)} = {dealer_total}")

        if player_total > 21:
            #if player total goes over, instant loss
            print("Player Busts! Dealer Wins.") #bet is gone and not returned
        elif dealer_total > 21:
            #if player total goes over, instant loss
            print("Dealer Busts! Player Wins.")
            self.money += self.bet * 2  #players bet * 2 goes back to player
            print(f"You win ${self.bet * 2}! You now have ${self.money}.")
        elif player_total == dealer_total:
            #if cards total == , then push(tie)
            print("It's a Push!")
            self.money += self.bet  #players bet goes back to player
            print(f"You get your bet back. You now have ${self.money}.")
        elif player_total > dealer_total:
            #if player total > dealertotal && no one goes over 21, player wins
            print("Player Wins!")
            self.money += self.bet * 2  #players bet * 2 goes back to player
            print(f"You win ${self.bet * 2}! You now have ${self.money}.")
        else:
            #if player total < dealertotal && no one goes over 21, dealer wins
            print("Dealer Wins.")

    def play_game(self):
        #main loop for game
        self.reset_hands()  #reset hands for new game
        self.player_turn = True  #reset players turn
        self.dealer_turn = True  #reset dealers turn

        self.place_bet()  #input for players bet
        self.first_deal()  #start of game
        if self.check_blackjack():  #check for automatic win
            return True
        self.player_turn_logic()  #players turn
        if self.calculate_total(self.player_hand) <= 21:  #continue if player total <= 21
            self.dealer_turn_logic()  #dealers turn
        self.calculate_winner()  #calc winner

        #check for player money is still enough to play min bet = 25, if player money < 25 game restart
        if self.money < self.minimum_bet:
            print("You don't have enough money to play. Game Over!")
            return False
        return True


def main():
    print("Welcome to Blackjack!")

    while True:
        game = Blackjack()

        while True:
            if not game.play_game():  #play one game, stop if game over
                break

            #reset deck every 5 games
            game.game_count += 1
            if game.game_count % 5 == 0:
                print("Resetting deck...")
                game.deck = game.create_deck()

            #show remaining cards, single deck start 52 cards
            print(f"{len(game.deck)} cards left in the deck.")

        while True:  #restart or exit logic
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            if play_again == 'y':
                break  #restart
            elif play_again == 'n':
                print("Thanks for playing!")
                return
            else:
                print("Invalid input. Please enter 'y' for Yes or 'n' for No.") #input validation for turn


if __name__ == "__main__":
    main()