# Write your code to expect a terminal of 80 characters wide and 24 rows high

def convert_hand(cards_list):
    """
    Converts a list of strings into a list of objects
    containing the rank and the suit
    Example: "10 of Diamonds" => {'rank': 10, 'suit': 'Diamonds'}
    """
    new_cards = []
    for card in cards_list:
        rank = get_rank(card)
        if rank is not None:
            new_cards.append({'rank': rank, 'suit': ''})
        else:
            return None
    return new_cards


def get_rank(card):
    """
    Gets the rank of a card from a given string
    """
    # The first rank the algorithm finds.
    # If multiple ranks are found then a ValueError will be raised
    found_ranks = []
    simple_ranks = ['j', 'q', 'k', 'a']
    complex_ranks = ['jack', 'queen', 'king', 'ace']
    try:
        # Checking if the rank of the card is a number (2-10)
        found_ranks = get_card_values(card, range(2, 11))
        found_complex_ranks = get_card_values(card, complex_ranks)
        # Only check for simple ranks if there are no complex
        # ranks found in the string, to prevent duplication
        if len(found_complex_ranks) == 0:
            found_ranks.extend(get_card_values(card, simple_ranks))
        else:
            found_ranks.extend(found_complex_ranks)
        
        if found_ranks == []:
            raise ValueError(
                f'No ranks found in "{card}"'
            )
        if len(found_ranks) > 1:
            raise ValueError(
                f'Multiple ranks found in "{card}"'
            )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return None
    else:
        return found_ranks[0]


def get_card_values(card, values):
    """
    Scans the card string to check if it contains any of
    the specified values, and returns a list of all values found
    """
    new_values = []
    card_lower = card.lower()
    for value in values:
        value_str = str(value)
        if value_str in card_lower:
            new_values.append(value)
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
