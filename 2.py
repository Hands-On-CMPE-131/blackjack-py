import random

playerTurn = True
dealerTurn = True



#deck of cards / player dealer hands
singleDeck = [2, 3, 4, 5, 6, 7, 8, 9, 10,2, 3, 4, 5, 6, 7, 8, 9, 10,2, 3, 4, 5, 6, 7, 8, 9, 10,2, 3, 4, 5, 6, 7, 8, 9, 10,
              'J', 'Q', 'K', 'A','J', 'Q', 'K', 'A','J', 'Q', 'K', 'A','J', 'Q', 'K', 'A']
#eightDeck = []
playerHand = []
dealerHand = []

#deal cards func
def dealCard(hand):
    card = random.choice(singleDeck) #pulls rand from singleDeck
    hand.append(card) #deal the card (add card to player/dealer)
    singleDeck.remove(card) #removed from deck (cannot be pulled again)
    return card

#calc total of hands
def total(hand):
    total = 0
    faceCard = ['J', 'Q', 'K'] #all face cards from deck excluding 'A'
    for card in hand: #each card pulled
        if isinstance(card, int):  #if the card is a number
            total += card
        elif card in faceCard:
            total += 10
        else: #for 'A' rules
            if total > 11: #if total is bigger than 11 ace becomes 1
                total += 1
            else: #if total is less than 11 ace becomes 11
                total += 11
    return total #return total



#cehck winner
def checkDealerHand(): #shows dealers first turn
    if len(dealerHand) == 2: #turn 1 only show 1st card
        return dealerHand[0]
    elif len(dealerHand) > 2: #once the done dealing (dealer will show hand)
        return dealerHand[0] , dealerHand[1]


#first deal
for _ in range(2):
    dealCard(dealerHand)
    dealCard(playerHand)


#format hand names
# Format hand to show Ace as both possible values
def format_hand(hand):
    total_without_ace = sum(card if isinstance(card, int) else 10 for card in hand if card != 'A')
    ace_count = hand.count('A')
    if ace_count == 0:
        return ', '.join(str(card) for card in hand)
    else:
        # Add the Ace possibilities
        low_total = total_without_ace + ace_count  # Aces as 1
        high_total = total_without_ace + ace_count * 11 if total_without_ace + ace_count * 11 <= 21 else low_total
        hand_display = ', '.join(str(card) if card != 'A' else 'Ace' for card in hand)
        if low_total == high_total:  # Only one value is valid
            return f"{hand_display} = {low_total}"
        else:
            return f"{hand_display} = {low_total}/{high_total}"


# Format hand to display card names and totals correctly
def format_hand(hand):
    total_value = 0
    face_card_values = {'J': 10, 'Q': 10, 'K': 10}
    hand_display = []

    for card in hand:
        if isinstance(card, int):  # If the card is a number
            total_value += card
            hand_display.append(str(card))
        elif card in face_card_values:  # If it's a face card
            total_value += face_card_values[card]
            hand_display.append(f"{card} = {face_card_values[card]}")
        elif card == 'A':  # Handle Ace
            if total_value + 11 > 21:
                total_value += 1
                hand_display.append("Ace = 1")
            else:
                total_value += 11
                hand_display.append("Ace = 11")
    return f"{', '.join(hand_display)} = {total_value}"

# Dealer hand reveal logic
def checkDealerHand():
    if len(dealerHand) == 2:  # Turn 1, show only 1st card
        first_card = dealerHand[0]
        if isinstance(first_card, int):
            return str(first_card)
        elif first_card in ['J', 'Q', 'K']:
            return f"{first_card} = 10"
        elif first_card == 'A':
            return "Ace = 1/11"
    else:  # Show the full hand
        return format_hand(dealerHand)

# Game loop
while playerTurn or dealerTurn:
    print(f"Player : {format_hand(playerHand)}")
    print(f"Dealer : {checkDealerHand()}")

    if playerTurn:
        hitOrStand = input(f"1: Hit \n2: Stay\n")  # Player choice hit or stay
    if total(dealerHand) > 16:  # Once the dealer's cards are >= 17, stop
        dealerTurn = False
    else:  # If not, deal card
        dealCard(dealerHand)
    if hitOrStand == '1':  # Player chose to deal
        dealCard(playerHand)
    else:
        playerTurn = False
    if total(playerHand) >= 21:  # Player cannot hit after 21
        break  # Stops after 21
    elif total(dealerHand) >= 21:  # Dealer cannot hit after 21
        break  # Stops after 21

#wincon

#if total(playerHand) == 21 & len(playerHand) == 2:
#    playerBlackjack = True
#if total(dealerHand) == 21 & len(dealerHand) == 2:
#    dealerBlackjack = True
#if playerBlackjack == True & dealerBlackjack == True

if total(playerHand) == 21:
    print(f"\nPlayer : {playerHand} \nPlayer Total: {total(playerHand)}"
          f"\nDealer : {dealerHand} \nDealer Total: {total(dealerHand)}")
    print(f"Blackjack for player")
elif total(dealerHand) == 21:
    print(f"\nPlayer : {playerHand} \nPlayer Total: {total(playerHand)}"
          f"\nDealer : {dealerHand} \nDealer Total: {total(dealerHand)}")
    print(f"Blackjack for dealer")
elif total(playerHand) > 21:
    print(f"\nPlayer : {playerHand} \nPlayer Total: {total(playerHand)}"
          f"\nDealer : {dealerHand} \nDealer Total: {total(dealerHand)}")
    print(f"Player Busts")
elif total(dealerHand) > 21:
    print(f"\nPlayer : {playerHand} \nPlayer Total: {total(playerHand)}"
          f"\nDealer : {dealerHand} \nDealer Total: {total(dealerHand)}")
    print(f"Dealer Busts")

