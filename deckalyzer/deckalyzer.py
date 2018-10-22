import sys
import db_utils, deck_utils

def run(deck_creator, deck_name, deck_descr, deck_data):
    # connect to existing database or create new and then connect
    con = db_utils.db_connect()

    # import deck list
    if deck_data is None:
        deck_data = deck_utils.get_deck_data()

    # parse deck deck list
    deck_list = deck_utils.parse_deck_data(deck_data)

    # create a new deck object with user info
    deck = deck_utils.create_deck(con, deck_creator, deck_name, deck_descr)

    # retrieve card data from database or scryfall api
    deck_utils.build_deck(con, deck_list, deck)
    db_utils.update_deck(con, deck)

    # insert cards into deck_cards table
    db_utils.insert_deck_cards(con, deck)


    #deck_record = db_utils.find_deck(con, deck.id)
    #db_utils.find_deck_cards(con, deck_record)

    con.close()

    return deck
