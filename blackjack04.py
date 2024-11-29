import random


class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()  #create/resets the deck of cards
        self.reset_hands()  #reset player and dealer hands
        self.player_turn = True  #set player's turn to true
        self.dealer_turn = True  #set dealer's turn to true
        self.game_count = 0  #tracks the number of games played (when count is 5 cards reset)

    def create_deck(self):
        return [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4  #single deck

    def reset_hands(self):
        """reset player and dealer hands"""
        self.player_hand = []  #player hand
        self.dealer_hand = []  #dealer hand

    def deal_card(self, hand):
        card = random.choice(self.deck)  #choose a random card
        hand.append(card)  #add card to hand
        self.deck.remove(card)  #remove added card from deck
        return card

    def calculate_total(self, hand):
        total = 0
        face_cards = {'J': 10, 'Q': 10, 'K': 10}  #set facecards to 10
        ace_count = 0  #knows how many aces in hand (can calc whether it is going to be 1 or 11)

        for card in hand:
            if isinstance(card, int):  #if it's a number card, add card value to total
                total += card
            elif card in face_cards:  #if it's a face card, add 10 to total
                total += face_cards[card]
            elif card == 'A':  #add ace to hand not a value yet (ace can be 1 or 11)
                ace_count += 1

        #ace can be 1 or 11 based on total hand value
        for _ in range(ace_count):
            if total + 11 > 21:  #if hand total is less than 11, ace = 11
                total += 1
            else:
                total += 11  #if hand total is more than 11, ace = 1

        return total

    def format_hand(self, hand, hide_second_card=False):
        """formats the hand, hiding the dealer's second card if needed"""
        if hide_second_card and len(hand) > 1:  #for dealer's hand, format (shown card), ?(hidden card)
            return f"{hand[0]}, ?"
        return ', '.join(str(card) for card in hand)

    def first_deal(self):
        """Deal two cards to both player and dealer."""
        for _ in range(2):  #deals the first set of cards 2 to player 2 to dealer
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)

    def check_blackjack(self):
        """Check for player's blackjack and end game early if dealer cannot beat it."""
        player_total = self.calculate_total(self.player_hand)
        dealer_first_card = self.dealer_hand[0]

        #check if player has blackjack
        if player_total == 21:
            print(f"\nPlayer: {self.format_hand(self.player_hand)} = {player_total}")
            print(f"Dealer: {self.format_hand(self.dealer_hand, hide_second_card=True)}")
            #dealer cannot match player's blackjack if not one of these cards below
            if dealer_first_card not in ['A', 'J', 'Q', 'K', 10]:
                print("Player has Blackjack! Player Wins!")
                return True
        return False

    def player_turn_logic(self):
        """Allow the player to take their turn."""
        while self.player_turn:  #shows player it's their turn
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
                print("Invalid input. Please enter 1 for Hit or 2 for Stay.")  #input validation for turn

    def dealer_turn_logic(self):
        """Handle the dealer's turn."""
        while self.calculate_total(self.dealer_hand) < 17:  #dealer must stop at all 17s
            self.deal_card(self.dealer_hand)

    def calculate_winner(self):
        """Determine the winner."""
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        print(f"\nPlayer: {self.format_hand(self.player_hand)} = {player_total}")
        print(f"Dealer: {self.format_hand(self.dealer_hand)} = {dealer_total}")

        if player_total > 21:
            #if player total goes over, instant loss
            print("Player Busts! Dealer Wins.")
        elif dealer_total > 21:
            #if dealer total goes over, instant win
            print("Dealer Busts! Player Wins.")
        elif player_total == dealer_total:
            #if card totals ==, then push (tie)
            print("It's a Tie!")
        elif player_total > dealer_total:
            #if player total > dealer total && no one goes over 21, player wins
            print("Player Wins!")
        else:
            #if player total < dealer total && no one goes over 21, dealer wins
            print("Dealer Wins!")

    def play_game(self):
        """Main gameplay loop for a single game."""
        self.reset_hands()  #reset hands for new game
        self.player_turn = True  #reset player's turn
        self.dealer_turn = True  #reset dealer's turn

        self.first_deal()  #start of game
        if self.check_blackjack():  #check for automatic win
            return
        self.player_turn_logic()  #player's turn
        if self.calculate_total(self.player_hand) <= 21:  #proceed if player hasn't busted
            self.dealer_turn_logic()  #dealer's turn
        self.calculate_winner()  #determine winner


def main():
    """Entry point for the game."""
    print("Welcome to Blackjack!")

    game = Blackjack()

    while True:
        game.play_game()  #play one game
        game.game_count += 1  #increment game count

        #reset deck every 5 games
        if game.game_count % 5 == 0:
            print("Resetting deck...")
            game.deck = game.create_deck()

        #show remaining cards, single deck starts at 52 cards
        print(f"{len(game.deck)} cards left in the deck.")

        #ask player if they want to play again
        while True:  #restart or exit logic
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            if play_again in ['y', 'n']:  #valid input
                break
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")  #input validation for turn
        if play_again != 'y':  #exit if no
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()