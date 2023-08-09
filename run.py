# Write your code to expect a terminal of 80 characters wide and 24 rows high


class Hand:
    """
    Holds a list of cards, and can calculate the hand value
    based on these cards
    """
    def __init__(self, cards):
        """
        Creates an instance of Hand
        """
        self.cards = cards
        self.cards_sorted = {
            'cards': [],
            'wildcards': 0
        }

    def print_hand(self):
        """
        Prints each card in this hand to the terminal
        """
        for card in self.cards:
            print(card.description())

    def sort(self):
        """
        Sorts the cards in ascending order, removing
        any wildcards and storing them in an integer
        """
        # Resetting the sorted hand if previously sorted
        self.cards_sorted = {
            'cards': [],
            'wildcards': 0
        }
        cards_template = self.cards.copy()
        # while len(cards_template) > 0:
        #     lowest_card = None
        #     for card in cards_template:

    def get_value(self, *wildcards):
        """
        Checks if the hand has a certain card combination,
        starting with the highest value and working its way
        down until a match is found
        """
        if (self.is_5_kind()):
            return '5 of a Kind'
        if (self.is_straight(True)):
            return 'Straight Flush'
        if (self.is_4_kind()):
            return '4 of a Kind'
        if (self.is_full_house()):
            return 'Full House'
        if (self.is_flush()):
            return 'Flush'
        if (self.is_straight(False)):
            return 'Straight'
        if (self.is_3_kind()):
            return '3 of a Kind'
        if (self.is_2_pair()):
            return 'Two Pair'
        if (self.is_pair()):
            return 'Pair'
        return 'High Card'

    def is_5_kind(self):
        """
        Returns true if 5 cards in the hand are of
        the same rank
        """
        return False

    def is_straight(self, flush):
        """
        Returns true if 5 cards are ranked in
        consecutive order, and have the same suit if
        specified
        """
        return False

    def is_4_kind(self):
        """
        Returns true if 4 cards in the hand are of
        the same rank
        """
        return False

    def is_full_house(self):
        """
        Returns true if the hand has 3 of a kind and
        a pair of a different rank
        """
        return False

    def is_flush(self):
        """
        Returns true if 5 cards in the hand are of
        the same suit
        """
        return False

    def is_3_kind(self):
        """
        Returns true if 3 cards in the hand are of
        the same rank
        """
        return False

    def is_2_pair(self):
        """
        Returns true if there are 2 pairs of cards
        in the hand that are of the same rank
        """
        return False

    def is_pair(self):
        """
        Returns true if 2 cards in the hand are of
        the same rank
        """
        return False


class Card:
    """
    A single card consisting of a rank and a suit
    """
    def __init__(self, rank, suit):
        """
        Creates an instance of Card
        """
        self.rank = rank
        self.suit = suit

    def description(self):
        """
        Returns the cards rank and suit as a readable string
        """
        return f'{self.rank} of {self.suit}'

    def is_duplicate(self, cards_list):
        """
        Returns if this card already exists in a list of cards
        """
        try:
            for card in cards_list:
                if (self.rank == card.rank and
                        self.suit == card.suit):
                    raise ValueError(
                        f'Multiple {self.description()}'
                    )
        except ValueError as e:
            print(f'Invalid input: {e}. Please try again.\n')
            return True
        else:
            return False

    def get_rank(self):
        """
        Returns the rank of the card as an integer
        """
        if self.rank == 'Jack':
            return 11
        if self.rank == 'Queen':
            return 12
        if self.rank == 'King':
            return 13
        if self.rank == 'Ace':
            return 14
        return int(self.rank)


class CardType:
    """
    Stores a single card input by the user, and contains
    functions to convert that string into a card dictionary
    """
    simple_type = {
        'rank': ['j', 'q', 'k', 'a'],
        'suit': ['h', 'd', 'c', 's']
    }
    complex_type = {
        'rank': ['jack', 'queen', 'king', 'ace'],
        'suit': ['heart', 'diamond', 'club', 'spade']
    }
    type_format = {
        'rank': ['Jack', 'Queen', 'King', 'Ace'],
        'suit': ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    }

    def __init__(self, text):
        """
        Creates an instance of CardType
        """
        self.text = text

    def get(self, value_type):
        """
        Gets the rank or suit of the card,
        raising an error if the type is not valid
        """
        found_values = []
        simple_types = CardType.simple_type[value_type]
        complex_types = CardType.complex_type[value_type]
        # The value for these ranks will be stored in the card object like this
        type_format = CardType.type_format[value_type]

        found_simple_types = self.find_values(simple_types, type_format)
        found_complex_types = self.find_values(complex_types, type_format)
        # Checking if the rank of the card is a number (2-10)
        if value_type == 'rank':
            found_values = self.find_values(range(2, 11), range(2, 11))

        # Adding any of the complex worded values if any were found
        found_values.extend(found_complex_types)

        # Only add the simple values if there are no
        # other values found in the string
        if len(found_values) == 0:
            found_values.extend(found_simple_types)

        if (type_is_valid(self.text, value_type, found_values)):
            return found_values[0]
        else:
            return None

    def convert(self, other_cards):
        """
        Converts a string into an instance of Card and returns it, if valid
        """
        rank = self.get('rank')
        if rank is not None:
            suit = self.get('suit')
            if suit is not None:
                card_obj = Card(rank, suit)
                if not card_obj.is_duplicate(other_cards):
                    return card_obj
        return None

    def find_values(self, values, value_formats):
        """
        Scans the card string to check if it contains any of
        the specified values, and returns a list of all values found
        as their formatted versions
        """
        new_values = []
        card_lower = self.text.lower()
        for value, string_format in zip(values, value_formats):
            value_str = str(value)
            if value_str in card_lower:
                new_values.append(string_format)
        return new_values


def convert_hand(cards_list):
    """
    Converts a list of strings into a list of objects
    containing the rank and the suit
    Example: "10 of Diamonds" => {'rank': 10, 'suit': 'Diamonds'}
    """
    new_cards = []
    for card in cards_list:
        card_obj = card.convert(new_cards)
        if card_obj is not None:
            new_cards.append(card_obj)
            continue
        return None
    return new_cards


def type_is_valid(card, value_type, found_values):
    """
    Checks if any ranks or suits found in a card string is
    valid. Will raise an error if there is not exactly one
    value found
    """
    try:
        if found_values == []:
            raise ValueError(
                f'No {value_type}s found in "{card}"'
            )
        if len(found_values) > 1:
            raise ValueError(
                f'Multiple {value_type}s {found_values} found in "{card}"'
            )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return False
    else:
        return True


def validate_hand(cards_list):
    """
    Checks if a poker hand entered by the user can
    produce a valid set of cards
    """
    formatted_hand = []
    try:
        # Each hand must contain at least 5 cards
        if len(cards_list) < 5:
            raise ValueError(
                f'Need at least 5 cards. You have given {len(cards_list)}'
            )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return None
    else:
        formatted_hand = convert_hand(cards_list)
        return formatted_hand


def get_hand_input():
    """
    Requests a hand to be manually entered by the user
    """
    # Keep requesting an input from the user until a valid hand is entered
    while True:
        print('Please enter your poker hand.')
        print(
            '- Your hand must contain at least 5 cards, separated by a comma.'
        )
        print('- Each card must clearly indicate its rank and its suit.')
        print('- Example: "King of Hearts", "King Heart", "KH"\n')
        hand_input = input('Enter hand here: ')

        hand_list = hand_input.split(',')
        card_objects = []
        for card_text in hand_list:
            card_object = CardType(card_text)
            card_objects.append(card_object)

        new_hand = validate_hand(card_objects)
        if new_hand is not None:
            return new_hand


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!\n')
    card_values = get_hand_input()
    hand_input = Hand(card_values)
    hand_input.print_hand()


main()
