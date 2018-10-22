from datetime import datetime

class Card(object):
    def __init__(self, card_data):
        self.name = card_data['name']
        self.cmc = card_data['cmc']
        self.mc = card_data['mana_cost']
        self.type = card_data['type_line']

    def __str__(self):
        return self.name


class Deck(object):
    def __init__(self, id=None, creator=None, name=None, descr=None,
            date_created=datetime.now(), last_updated=datetime.now()):
        self.id = id
        self.cards = []
        self.creator = creator
        self.name = name
        self.descr = descr
        self.date_created = date_created
        self.last_updated = last_updated

    def add_card(self, card):
        self.cards.append(card)
        self.last_updated = datetime.now()

    def deck_cards(self):
        deck_cards = []
        unique_cards = {cards for cards in self.cards}
        for card in unique_cards:
            count = self.cards.count(card)
            deck_cards.append((card.name, count))
        return deck_cards


    def avg_cmc(self):
        return sum([card.cmc for card in self.cards])/len(self.cards)

    def __str__(self):
        return self.name + ', by ' + self.creator
