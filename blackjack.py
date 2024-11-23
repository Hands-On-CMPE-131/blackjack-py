import random

class Blackjack:
    def __init__(self):
        self.player_hand = []  #players hand
        self.dealer_hand = []  #dealers hand
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',   #single deck of cards
                     2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
                     2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A',
                     2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.player_turn = True #set turns to true
        self.dealer_turn = True

    def deal_card(self, hand):
        card = random.choice(self.deck) #chose random card
        hand.append(card) #add card to hand
        self.deck.remove(card) #remove addded card from deck
        print(f"{len(self.deck)} cards left")
        return card

    def calculate_total(self, hand):
        total = 0
        face_cards = {'J': 10, 'Q': 10, 'K': 10} #set facecards to 10
        ace_count = 0

        for card in hand:
            if isinstance(card, int): #if its a number card add card value to total
                total += card
            elif card in face_cards: #if its a face card add 10 to total
                total += face_cards[card]
            elif card == 'A': #add ace to hand not a value yet (ace can be 1 or 11)
                ace_count += 1

        #ace can be 1 or 11 based on total hand value
        for _ in range(ace_count):
            if total + 11 > 21:
                total += 1
            else:
                total += 11

        return total

    #formats the hand player and dealers hand to make look nicer
    def format_hand(self, hand):
        #hand total w/o ace
        total_without_ace = sum(
            card if isinstance(card, int) else 10 for card in hand if card != 'A'
        )
        #calc hand total with ace
        ace_count = hand.count('A')
        if ace_count == 0:
            return ', '.join(str(card) for card in hand)
        else:
            #shows total as ace = 1
            low_total = total_without_ace + ace_count
            #aces are worth 11 but only if the total isnt over 21.
            high_total = total_without_ace + ace_count * 11 \
                if total_without_ace + ace_count * 11 <= 21 \
                else low_total
            #displays hand with ,
            hand_display = ', '.join(str(card) if card != 'A' else 'Ace' for card in hand)
            #shows low if low is over 21, if not show bot hlow and high totals
            if low_total == high_total:
                return f"{hand_display} = {low_total}"
            else:
                return f"{hand_display} = {low_total}/{high_total}"

    def check_dealer_hand(self):
        #only shows dealers first card during first turn
        if len(self.dealer_hand) == 2:
            return self.format_hand([self.dealer_hand[0]])  #first card
        #after show all cards
        else:
            return self.format_hand(self.dealer_hand)  #whole hand

    def first_deal(self):
        #inital deal
        for _ in range(2):
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)

    def player_turn_logic(self):
        #prints cards
        print(f"Player: {self.format_hand(self.player_hand)}")
        print(f"Dealer: {self.check_dealer_hand()}")
        #players chose hit or stay
        choice = input("1: Hit\n2: Stay\n")
        if choice == '1':#hit
            self.deal_card(self.player_hand)
            print(f"{len(self.deck)} cards left")
            if self.calculate_total(self.player_hand) >= 21:#cannot draw past 21
                self.player_turn = False
        elif choice == '2':#stay
            self.player_turn = False

    def dealer_turn_logic(self):
        while self.calculate_total(self.dealer_hand) < 17:#dealer must stop at 17
            self.deal_card(self.dealer_hand)
        self.dealer_turn = False

    def calculate_winner(self):
        #calc winner
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        print(f"\nPlayer: {self.format_hand(self.player_hand)} (Total: {player_total})")
        print(f"Dealer: {self.format_hand(self.dealer_hand)} (Total: {dealer_total})")

        if player_total > 21:
            print("Player Busts! Dealer Wins.")
            print(f"{len(self.deck)} cards left")
        elif dealer_total > 21:
            print("Dealer Busts! Player Wins.")
            print(f"{len(self.deck)} cards left")
        elif player_total == dealer_total:
            print("It's a Tie!")
            print(f"{len(self.deck)} cards left")
        elif player_total > dealer_total:
            print("Player Wins!")
            print(f"{len(self.deck)} cards left")
        else:
            print("Dealer Wins!")
            print(f"{len(self.deck)} cards left")

    def play_game(self):
        #loop
        self.first_deal()#inital deal(start of game)
        while self.player_turn:#while still players turn
            self.player_turn_logic()#choose hit/stay
        if self.calculate_total(self.player_hand) <= 21: #calc player hand
            self.dealer_turn_logic() #dealer turn
        self.calculate_winner() #calc winner

def main():
    print("Blackjack rules: Beat dealers cards to win, Dealer must stop at 17")

    game = Blackjack()

    game.play_game()



if __name__ == "__main__":
    main()