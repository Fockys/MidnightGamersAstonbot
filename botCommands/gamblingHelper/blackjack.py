
import random

#this whole file is just for the blackjack game, handles one game

class card():
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value

class blackjackGame():
    def __init__(self,bet):
        self.createDeck()
        self.userHand = []
        self.botHand = []
        self.userTotal = 0
        self.botTotal = 0
        self.bet= bet
        self.setup()


    def createDeck(self):
        self.values = {
            "Ace":1,
            "2":2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "10":10,
            "Jack":10,
            "Queen":10,
            "King":10
        }
        suit = ["Hearts","Diamonds","Clubs","Spades"]

        self.deck = []
        for s in suit:
            for key in self.values:
                self.deck.append(card(s,key))

    def drawCard(self):
        index = random.randomint(0,len(self.deck))
        card = self.deck[index]
        del(self.deck[index])
        return card
    
    def setup(self):
        random.shuffle(self.deck)
        self.botHand = [self.deck.pop(),self.deck.pop()]
        self.userHand = [self.deck.pop(),self.deck.pop()]
        self.botTotal = self.calcTotal(self.botHand)
        self.userTotal = self.calcTotal(self.userHand)

    def calcTotal(self,hand):
        sum = 0
        aces =0
        for card in hand:
            sum += self.values[card.value]
            if card.value == "Ace":
                aces += 1

        while aces > 0 and sum + 10 <= 21:
            sum += 10
            aces -= 1
        
        return(sum)
    
    def isBustUser(self):
        if self.calcTotal(self.userHand) > 21:
            return 1
        else:
            return 0

    def returnDeck(self,deck):
        deckNumbers = []
        for cards in deck:
            deckNumbers.append([cards.value,cards.suit])
        return deckNumbers

    def returnDeckWithEmoji(self,deck):
        DeckValues = self.returnDeck(deck)
        suitsEmoji = {
            "Hearts":"♥️",
            "Diamonds":"♦️",
            "Clubs":"♣️",
            "Spades":"♠️"
        }
        result = []
        for card in DeckValues:
            card[1] = suitsEmoji[card[1]]
            result.append(''.join(card))

        return(' | '.join(result))
    
    def niceUserDeck(self):
        return(self.returnDeckWithEmoji(self.userHand))
    def niceBotDeck(self,end):
        
        #if end isnt true obfursates first card
        hand = self.returnDeckWithEmoji(self.botHand)
        if end == False:
            try:
                temp = hand.split('|')
                del(temp[0])
                hand = '|'.join(temp)
                hand = "? |"+hand
            except Exception as e:
                print(e)

        return(hand)
    
    def hitUser(self):
        self.userHand.append(self.deck.pop())
        self.userTotal = self.calcTotal(self.userHand)
        if self.userTotal>21:
            self.result()

    def hitBot(self):
        self.botHand.append(self.deck.pop())
        self.botTotal = self.calcTotal(self.botHand)

    def userStay(self):
        self.botTurn()
        return self.result()

    def botTurn(self):
        while True:
            cards = self.returnDeck(self.botHand)
            for i in range(len(cards)):
                cards[i] = ' '.join(cards[i])
            cards = ",".join(cards)

            
            

            if self.botTotal>16:
                break
            else:
                self.hitBot()


    #return 0 for tie, 1 for loss, 2 for win, 3 for win with bonus
    def result(self):

        if self.userTotal == 21:
            return 3
        
        if self.userTotal>21:
            return 1
        elif self.botTotal>21:
            return 2
        elif self.botTotal>self.userTotal:
            return 1
        elif self.userTotal>=self.botTotal:
            return 2
        else:
            return 0









    
    