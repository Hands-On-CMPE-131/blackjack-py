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
def format_hand(hand):
    return ', '.join(str(card) if card != 'A' else 'Ace' for card in hand)

#loop
while playerTurn or dealerTurn:

    print(f"Player : {format_hand(playerHand)} = {total(playerHand)}")
    print(f"Dealer : {checkDealerHand()} = {total([dealerHand[0]])}")  # Only show one card
    if playerTurn:
        hitOrStand = input(f"1: Hit \n2: Stay\n") #player choice hit and stay
    if total(dealerHand) > 16: #once the dealers cards are => 17 stop
        dealerTurn = False
    else:   #if not deal card
        dealCard(dealerHand)
    if hitOrStand == '1': #chose to deal
        dealCard(playerHand)
    else:
        playerTurn = False
    if total(playerHand) >= 21: #player cannot hit after 21
        break #stops after 21
    elif total(dealerHand) >= 21: #dealer cannot hit after 21
        break #stops after 21

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