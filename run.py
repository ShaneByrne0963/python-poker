# Write your code to expect a terminal of 80 characters wide and 24 rows high

class Card:
    """
    Stores information about cards to be used for validation
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


def convert_hand(cards_list):
    """
    Converts a list of strings into a list of objects
    containing the rank and the suit
    Example: "10 of Diamonds" => {'rank': 10, 'suit': 'Diamonds'}
    """
    new_cards = []
    for card in cards_list:
        rank = get_card_type(card, 'rank')
        suit = get_card_type(card, 'suit')
        if rank is not None and suit is not None:
            card_obj = {'rank': rank, 'suit': suit}
            if not card_is_duplicate(card_obj, new_cards):
                new_cards.append(card_obj)
            else:
                return None
        else:
            return None
    return new_cards


def get_card_type(card, value_type):
    """
    Gets the rank of a card from a given string,
    raising an error if the rank is not valid
    """
    # The first rank the algorithm finds.
    # If multiple ranks are found then a ValueError will be raised
    found_values = []
    simple_types = Card.simple_type[value_type]
    complex_types = Card.complex_type[value_type]
    # The value for these ranks will be stored in the card object like this
    type_format = Card.type_format[value_type]

    found_simple_types = get_card_values(card, simple_types, type_format)
    found_complex_types = get_card_values(card, complex_types, type_format)
    # Checking if the rank of the card is a number (2-10)
    if value_type == 'rank':
        found_values = get_card_values(card, range(2, 11), range(2, 11))

    # Adding any of the complex worded values if any were found
    found_values.extend(found_complex_types)

    # Only add the simple values if there are no
    # other values found in the string
    if len(found_values) == 0:
        found_values.extend(found_simple_types)

    if (type_is_valid(card, value_type, found_values)):
        return found_values[0]
    else:
        return None


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


def card_is_duplicate(card, other_cards):
    """
    Checks if a card is identical to any other existing card
    """
    try:
        for other_card in other_cards:
            if (card['rank'] == other_card['rank'] and
                    card['suit'] == other_card['suit']):
                raise ValueError(
                    'Multiple cards of the same type'
                )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return True
    else:
        return False


def get_card_values(card, values, value_formats):
    """
    Scans the card string to check if it contains any of
    the specified values, and returns a list of all values found
    as their formatted versions
    """
    new_values = []
    card_lower = card.lower()
    for value, string_format in zip(values, value_formats):
        value_str = str(value)
        if value_str in card_lower:
            new_values.append(string_format)
    return new_values


def validate_hand(cards_list):
    """
    Checks if a poker hand is valid
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
        new_hand = validate_hand(hand_list)
        if new_hand is not None:
            return new_hand


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!\n')
    hand_input = get_hand_input()
    print(hand_input)


main()
