# Write your code to expect a terminal of 80 characters wide and 24 rows high

def validate_hand(cards_list):
    """
    Checks if a poker hand is valid
    """
    try:
        # Each hand must contain at least 5 cards
        if len(cards_list) < 5:
            raise ValueError(
                f'Need at least 5 cards. You have given {len(cards_list)}'
            )
    except ValueError as e:
        print(f'Invalid input: {e}. Please try again.\n')
        return False
    else:
        print(cards_list)
        return True


def get_hand_input():
    """
    Requests a hand to be manually entered by the user
    """
    while True:
        print('Please enter your poker hand.')
        print('- Your hand must contain at least 5 cards, separated by a comma.')
        print('- Each card must clearly indicate its rank and its suit.')
        print('- Example: "King of Hearts", "King Heart", "KH"\n')
        hand_input = input('Enter hand here: ')

        hand_list = hand_input.split(',')
        if (validate_hand(hand_list)):
            return hand_input


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!\n')
    hand_input = get_hand_input()


main()
