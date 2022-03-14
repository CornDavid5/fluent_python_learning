from random import choice
from collections import namedtuple

Card = namedtuple("Card", "rank suit")
suit_value = {'diamond': 1, 'club': 2, 'heart': 3, 'spade': 4}

class FrenchDeck:
    suits = "diamond club heart spade".split()
    ranks = [i for i in range(2,11)] + list('JQKA')

    def __init__(self):
        self._card = [Card(rank, suit) for rank in FrenchDeck.ranks for suit in FrenchDeck.suits]

    def __len__(self):
        return len(self._card)
    
    def __getitem__(self, idx):
        return self._card[idx]

def card_value(card: Card):
    return FrenchDeck.ranks.index(card.rank) * len(suit_value) + suit_value[card.suit]


deck = FrenchDeck()
print(f"{choice(deck)}, {choice(deck)}")
print(f"contains 17 diamond: {Card(17, 'diamond') in deck}, contains 2 club: {Card(2, 'club') in deck}")
# cannot use random.shuffle(), because that method requires a MutableSequence, which requires class to implement __setitem__

for rank, suit in reversed(deck):
    print(f"{rank}, {suit}")