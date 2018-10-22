import requests, os
from time import sleep
from objects import Card, Deck
import db_utils

# opens file containing deck data
def get_deck_data():
    path = os.path.join(os.path.dirname(__file__), 'exported_cards.txt')
    deck_data = open(path, 'r')
    return deck_data

# parses imported deck data into a list of tuples
def parse_deck_data(deck_data):
    split_deck_data = deck_data.splitlines()
    parsed_deck = []
    for record in split_deck_data:
        card_name = record[record.find(' ')+1:record.find(' (')]
        card_count = record[:record.find(' ')]
        parsed_deck.append((card_name, card_count))
    return parsed_deck

# creates an instance of the Deck object and inserts it to the database
def create_deck(con, creator, name, descr):
    deck = Deck(creator=creator, name=name, descr=descr)
    deck.id = db_utils.insert_deck(con, deck)
    return deck

# adds each card from the deck list to the deck
def build_deck(con, deck_list, deck):
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
        sleep(0.1) # scryfall wants api requests limited to 10/sec
