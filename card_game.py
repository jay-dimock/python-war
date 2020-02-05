import random

class Card:
    def __init__(self, number, suit):
        self.number = number        
        self.suit = suit        
        self.num_string = str(self.number)
        if self.number == 11: self.num_string = "J"
        elif self.number ==12: self.num_string = "Q"
        elif self.number == 13: self.num_string = "K"
        elif self.number == 14: self.num_string = "A"

        if len(self.num_string) == 1: self.num_string = " " + self.num_string
        
        self.face = f"{self.num_string}{self.suit}"

class Player:
    def __init__(self, name):
        self.name = name
        self.unplayed_cards = []
        self.played_cards = []
        self.discards = []
        self.loser = False

    def deal(self):
        if len(self.unplayed_cards) == 0:
            if len(self.discards) == 0:
                self.loser = True
                return False
            random.shuffle(self.discards)
            self.unplayed_cards = self.discards
            self.discards = []

        self.played_cards.append(self.unplayed_cards[0])
        self.unplayed_cards.pop(0)
        return True

    def take_cards(self, opponent):  
        for i in range(len(opponent.played_cards)):
            self.discards.append(opponent.played_cards[i])
            self.discards.append(self.played_cards[i])
        opponent.played_cards = []
        self.played_cards = []  

    def last_played_card(self):
        return self.played_cards[len(self.played_cards)-1]

    # def display_played_card(self, warMode):
    #     if (warMode): print("\tface down card")
    #     else: 
    #         print(f"{self.name}: {self.last_played_card().face}")
    #         print('┌───────┐')
    #         print(f'| {self.last_played_card().num_string}    |')
    #         print('|       |')
    #         print(f'|   {self.last_played_card().suit}   |')
    #         print('|       |')
    #         print(f'|    {self.last_played_card().num_string} |')
    #         print('└───────┘') 

    def display_status(self):
        card_count = len(self.unplayed_cards) + len(self.discards)
        plural = "s"
        if card_count == 1: plural = ""
        print(f"{self.name} has {card_count} card{plural}")

class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.warMode = False

    def startGame(self):
        print("\nWelcome to WAR!")
        print("Press ENTER to start a new round (Q to Quit)...")        

        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        if input().lower() == "q": return

        cards = []
        suits = ["♥","♦","♣","♠"]
        for s in range(len(suits)):
            for n in range(2, 15):
                cards.append(Card(n, suits[s]))
        random.shuffle(cards)
        for i in range(len(cards)):
            if i % 2 == 0:
                self.player1.unplayed_cards.append(cards[i])
            else:
                self.player2.unplayed_cards.append(cards[i])

        if not self.play(): return
        self.startGame()

    def fightWar(self, player):
        for i in range (3):            
            if not player.deal(): return False
        return True  

    def play(self):
        while True:
            warDisplay = self.warMode
            if self.warMode:
                print()
                print("*"*50)
                print("   WAR!!!")
                print("*"*50)
                print()
                self.fightWar(self.player1)
                self.fightWar(self.player2)
                self.warMode = False
                if self.player1.loser or self.player2.loser:
                    self.printLostGame()
                    break                
            
            if not self.deal(warDisplay): break

            winner = None
            cardCount = len(self.player1.played_cards)

            if self.player1.last_played_card().number > self.player2.last_played_card().number:
                self.player1.take_cards(self.player2)
                winner = self.player1
            elif self.player2.last_played_card().number > self.player1.last_played_card().number:
                self.player2.take_cards(self.player1)
                winner = self.player2
            else: 
                self.warMode = True
                continue

            plural = "s"
            if cardCount == 1: plural = ""
            print()
            print(f"{winner.name} won {cardCount} card{plural}!  [ Q:Quit | S:Status ]")
            print("*"*50)
            userInput = input().lower()
            if userInput == "q": return False
            elif userInput == "s":
                if not self.printStatus(): return False

        print("*" * 50)
        print("           GAME OVER")
        print("*" * 50)
        return True
                    
    def deal(self, warDisplay):
        self.player1.deal()
        self.player2.deal()

        if self.player1.loser or self.player2.loser:
            self.printLostGame()    
            return False          

        if warDisplay:
            self.displayWar(self.player1)
            self.displayWar(self.player2)
        else: 
            self.displayCards()
        return True
 

    def displayCards(self):
        card1 = self.player1.last_played_card()
        card2 = self.player2.last_played_card()
        print(f'{self.player1.name}      {self.player2.name}')
        print('┌───────┐     ┌───────┐')
        print(f'| {card1.num_string}    |     | {card2.num_string}    |')
        print('|       |     |       |')
        print(f'|   {card1.suit}   |     |   {card2.suit}   |')
        print('|       |     |       |')
        print(f'|    {card1.num_string} |     |    {card2.num_string} |')
        print('└───────┘     └───────┘') 

    def displayWar(self, player):
        card = player.last_played_card()
        print(player.name)
        print('\t┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐')
        print(f'\t|       |  |       |  |       |  | {card.num_string}    |')
        print('\t|       |  |       |  |       |  |       |')
        print(f'\t|       |  |       |  |       |  |   {card.suit}   |')
        print('\t|       |  |       |  |       |  |       |')
        print(f'\t|       |  |       |  |       |  |    {card.num_string} |')
        print('\t└───────┘  └───────┘  └───────┘  └───────┘')

    def printLostGame(self):
        if self.player1.loser and self.player2.loser:
            print("\nBoth players are out of cards! It's a tie.")
        elif self.player1.loser:
            print(f"\n{self.player1.name} is out of cards. {self.player2.name} won!")
        else:
            print(f"\n{self.player2.name} is out of cards. {self.player1.name} won!") 

    def printStatus(self):
        print()
        print("*" * 50)
        print("STATUS:")
        self.player1.display_status()
        self.player2.display_status()
        print("*" * 50)
        print()
        print("[ Q:Quit ]")
        return input().lower() != "q"

if __name__ == '__main__':
    game = Game()
    game.startGame()