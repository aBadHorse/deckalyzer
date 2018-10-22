import os, sqlite3
from objects import Card, Deck

PATH = os.path.join(os.path.dirname(__file__), 'card_db.sqlite3')

def db_connect(db_path=PATH):
    if os.path.exists(db_path):
        con = sqlite3.connect(db_path)
    else:
        con = sqlite3.connect(db_path)
        create_tables(con)
        #describe_tables(con)
    return con

def find_card(con, name):
    sql = """
        SELECT * FROM all_cards WHERE name = ?
    """
    cur = con.cursor()
    cur.execute(sql, [name])
    return cur.fetchone()

def insert_card(con, card):
    sql = """
        INSERT INTO all_cards (name, cmc, mc, type)
        VALUES (?, ?, ?, ?)
    """
    try:
        cur = con.cursor()
        cur.execute(sql, (card.name, card.cmc, card.mc, card.type))
        con.commit()
    except:
        con.rollback()
        raise RuntimeError("Error trying to insert card into all_cards")

def find_deck(con, deck_id):
    sql = """
        SELECT * FROM all_decks WHERE id = ?
    """
    try:
        cur = con.cursor()
        cur.execute(sql, [deck_id])
        res = cur.fetchone()
        deck = Deck(res[0], res[1], res[2], res[3], res[4], res[5])
        return deck
    except:
        raise RuntimeWarning("Deck not found")


def find_deck_cards(con, deck):
    sql = """
        SELECT ac.name, ac.cmc, ac.mc, ac.type, dc.count FROM deck_cards dc
        JOIN all_cards ac ON dc.card_name = ac.name
        WHERE dc.deck_id = ?
    """
    cur = con.cursor()
    cur.execute(sql, [deck.id])
    res = cur.fetchall()
    for r in res:
        card_data = {
            'name': r[0],
            'cmc': r[1],
            'mana_cost': r[2],
            'type_line': r[3]
        }
        my_card = Card(card_data)
        for _ in range(r[4]):
            deck.add_card(my_card)

def insert_deck(con, deck):
    sql = """
        INSERT INTO all_decks (creator, name, descr, date_created, last_updated)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        cur = con.cursor()
        cur.execute(sql, (deck.creator, deck.name, deck.descr, deck.date_created, deck.last_updated))
        con.commit()
        return cur.lastrowid
    except:
        con.rollback()
        raise RuntimeError("Error trying to insert deck into all_decks")

def update_deck(con, deck):
    sql = """
        UPDATE all_decks
        SET creator = ?, name = ?, descr = ?, last_updated = ?
        WHERE id = ?
    """
    try:
        cur = con.cursor()
        cur.execute(sql, (deck.creator, deck.name, deck.descr, deck.last_updated, deck.id))
        con.commit()
    except:
        con.rollback()
        raise RuntimeError("Error trying to update deck in all_decks")

def insert_deck_cards(con, deck):
    sql = """
        INSERT INTO deck_cards (card_name, deck_id, count)
        VALUES (?, ?, ?)
    """
    cur = con.cursor()
    for card_tuple in deck.deck_cards():
        cur.execute(sql, (card_tuple[0], deck.id, card_tuple[1]))
    con.commit()

def create_tables(con):
    sql = """
        CREATE TABLE all_cards (
            name text PRIMARY KEY,
            cmc integer,
            mc text,
            type text
        )
    """
    sql2 = """
        CREATE TABLE all_decks (
            id integer PRIMARY KEY,
            creator text NOT NULL,
            name text NOT NULL,
            descr text,
            date_created datetime NOT NULL,
            last_updated datetime NOT NULL
        )
    """
    sql3 = """
        CREATE TABLE deck_cards (
            card_name text,
            deck_id integer,
            count integer,
            FOREIGN KEY (card_name) REFERENCES all_cards (name),
            FOREIGN KEY (deck_id) REFERENCES all_decks (id)
        )
    """
    cur = con.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    cur.execute(sql3)

def describe_tables(con):
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())
