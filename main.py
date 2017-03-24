from card_dealer import *

dealer = read_cards('cards.txt')
for i in range(20):
    card = dealer.deal()
    print('{:<18}\n{:<13}\n{}'.format(card.name, card.cost_string(), card.action_string()))