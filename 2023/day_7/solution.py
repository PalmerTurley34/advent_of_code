from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
import operator

class HandType(Enum):
    FIVE_KIND = 4
    FOUR_KIND = 2
    FULL_HOUSE = 1
    THREE_KIND = 0
    TWO_PAIR = -1
    TWO_KIND = -2
    HIGH_CARD = -4

@dataclass
class Hand:
    cards: str
    bid: int
    part: int = 1
    hand_type: HandType = field(init=False)
    sort_key: str = field(init=False)

    def __post_init__(self):
        if self.part == 1:
            self.sort_key = self.cards.replace('A', 'Z').replace('K', 'Y').replace('Q', 'X').replace('J', 'W').replace('T', 'V')
            self.hand_type = self.get_hand_type()
        else:
            self.sort_key = self.cards.replace('A', 'Z').replace('K', 'Y').replace('Q', 'X').replace('J', '1').replace('T', 'V')
            self.hand_type = self.get_hand_type_with_wild()

    def get_hand_type(self) -> HandType:
        card_counts = defaultdict(int)
        for card in self.cards:
            card_counts[card] += 1
        hand_calculation = max(card_counts.values()) - len(card_counts)
        return HandType(hand_calculation)

    def get_hand_type_with_wild(self) -> HandType:
        if self.cards == 'JJJJJ':
            return HandType.FIVE_KIND
        card_counts = defaultdict(int)
        for card in self.cards:
            if card != 'J':
                card_counts[card] += 1
        if 'J' in self.cards:
            max_count = max(card_counts.values())
            jack_replacement = max(card for card, count in card_counts.items() if count == max_count)
            cards = self.cards.replace('J', jack_replacement)
            card_counts = defaultdict(int)
            for card in cards:
                if card != 'J':
                    card_counts[card] += 1
        hand_calculation = max(card_counts.values()) - len(card_counts)
        return HandType(hand_calculation)


def main(part=1):
    with open('inputs.txt') as file:
        lines = [line.strip() for line in file]
    hand_types: dict[HandType, list[Hand]] = defaultdict(list)
    for line in lines:
        cards, bid = line.split()
        bid = int(bid)
        hand = Hand(cards, bid, part)
        hand_types[hand.hand_type].append(hand)
    for hand_type in list(HandType):
        hand_types[hand_type] = sorted(hand_types[hand_type], key=lambda x: x.sort_key)
    all_hands = reduce(operator.add, [hand_types[hand_type] for hand_type in list(HandType)[::-1]])
    total_winnings = 0
    for rank, hand in enumerate(all_hands, start=1):
        total_winnings += rank * hand.bid
    print(f'Part {part}: {total_winnings}')

if __name__ == '__main__':
    main()
    main(2)