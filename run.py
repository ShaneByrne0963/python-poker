# Write your code to expect a terminal of 80 characters wide and 24 rows high

def get_hand_input():
    """
    Requests a hand to be manually entered by the user
    """
    print('Please enter your poker hand.\n')
    print('- Your hand must contain at least 5 cards, separated by a comma.')
    print('- Each card must clearly indicate its rank and its suit.')
    print('- Example: "King of Hearts", "King Heart", "KH"\n')
    hand_input = input('Enter hand here: ')
    return hand_input


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!')
    hand_input = get_hand_input()


main()
