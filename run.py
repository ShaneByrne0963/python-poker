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
    found_rank = None
    is_duplicate = False
    try:
        # Checking if the rank of the card is a number (2-10)
        for number in range(2, 11):
            number_str = str(number)
            if number_str in card:
                if found_rank is not None:
                    is_duplicate = True
                    break
                found_rank = number
        if found_rank is None:
            raise ValueError(
                f'No ranks found in "{card}"'
            )
        if is_duplicate:
            raise ValueError(
                f'Multiple ranks found in "{card}"'
            )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return None
    else:
        return found_rank


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
