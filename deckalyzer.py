import requests, os
from time import sleep
from objects import Card, Deck
import db_utils

path = os.path.join(os.path.dirname(__file__), 'exported_cards.txt')
cards_file = open(path, 'r')
deck_list = []

for card in cards_file:
    name = card[card.find(' ')+1:card.find(' (')]
    count = card[:card.find(' ')]
    deck_list.append((name, count))

deck = Deck(creator='Malachi', name='Handsome Deck')


con = db_utils.db_connect()

deck.id = db_utils.insert_deck(con, deck)
print('deck ', deck.name, ' id: ', deck.id)


for card in deck_list:
    card_record = db_utils.find_card(con, card[0])
    if card_record is not None:
        card_data = {
            'name': card_record[0],
            'cmc': card_record[1],
            'mana_cost': card_record[2],
            'type_line': card_record[3]
        }
        my_card = Card(card_data)
    else:
        card_data = requests.get('https://api.scryfall.com/cards/named?fuzzy='+card[0]).json()
        my_card = Card(card_data)
        db_utils.insert_card(con, Card(card_data))

    for _ in range(int(card[1])):
        deck.add_card(my_card)
    sleep(0.1)

db_utils.insert_deck_cards(con, deck)

deck_record = Deck(db_utils.find_deck(con, deck.id))
con.close()
avg_cmc = deck_record.avg_cmc()
print(deck_record, '{0:.2f}'.format(avg_cmc))
for card in deck_record.deck_cards():
    print(card[0], card[1])
#for card in [c for c in deck.cards if c.type.find('Land') == -1]:
#    print(card.name)
