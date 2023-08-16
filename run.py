# Write your code to expect a terminal of 80 characters wide and 24 rows high
import random


class Deck:
    """
    Contains all the cards that have not been dealt
    """
    def __init__(self):
        """
        Creates an instance of Deck
        """
        self.cards = self.get_full()
        self.wildcards = []

    def get_full(self):
        """
        Returns a list every card in a deck
        """
        cards = []
        for suit in CardType.type_format['suit']:
            # Adding the number ranks
            for rank in range(2, 11):
                card = Card(rank, suit)
                cards.append(card)
            # Adding the worded ranks
            for rank in CardType.type_format['rank']:
                card = Card(rank, suit)
                cards.append(card)
        return cards

    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self.cards)

    def take_card(self, card=None):
        """
        Returns a card of a given rank and suit, removing
        the card from the deck. Takes the first card from the
        deck if no rank or suit is given
        """
        # Takes the first card from the deck
        # if no parameters are given
        if card is None:
            if len(self.cards) > 0:
                found_card = self.cards[0]
                self.cards.pop(0)
                return found_card
            # Notifies the user when there are no cards in the
            # deck, and returns None
            print('No more cards in the deck!')
            return None
        if self.cards.count(card) > 0:
            self.cards.remove(card)
            return card
        # Creates a card to print an error if the card
        # does not exist in the deck
        print_error(
            f'No {card.description()} in deck'
        )
        return None

    def get_card(self, rank, suit):
        """
        Gets a specific card from the deck. Returns
        None if no card exists
        """
        for card in self.cards:
            if rank == card.rank and suit == card.suit:
                return card


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
        while len(cards_template) > 0:
            # Finding the lowest card in the list
            lowest_card = None
            lowest_value = 0
            for card in cards_template:
                card_val = card.get_rank_value()
                if (lowest_card is None or
                        card_val < lowest_value):
                    lowest_card = card
                    lowest_value = card_val
            # Moving the lowest card to the sorted cards dict
            self.cards_sorted['cards'].append(lowest_card)
            cards_template.remove(lowest_card)

    def get_value(self, *wildcards):
        """
        Checks if the hand has a certain card combination,
        starting with the highest value and working its way
        down until a match is found
        """
        self.sort()
        pairs = self.get_repeating_values('rank')
        # If the hand has 5 cards of the same rank (with wildcards)
        if self.is_of_kind(5, pairs):
            return '5 of a Kind'
        # If the hand has 5 consecutive ranking cards of the same suit
        straight_high = self.is_straight_flush()
        if straight_high is not None:
            if straight_high.rank == 'Ace':
                return 'Royal Flush'
            return 'Straight Flush'
        # If the hand has 4 cards of the same rank
        if self.is_of_kind(4, pairs):
            return '4 of a Kind'
        # If the hand has 3 cards of the same rank and
        # 2 different cards of the same rank
        if pairs[-1] >= 3 and pairs[-2] >= 2:
            return 'Full House'
        # If the hand has 5 cards of the same suit
        suits = self.get_repeating_values('suit')
        if suits[-1] >= 5:
            return 'Flush'
        # If the hand has 5 consecutive ranking cards
        if self.is_straight(self.cards_sorted['cards']):
            return 'Straight'
        # If the hand has 3 cards of the same rank
        if self.is_of_kind(3, pairs):
            return '3 of a Kind'
        # If the hand has 2 pairs of cards of the same rank
        if pairs.count(2) >= 2:
            return 'Two Pair'
        # If the hand has 2 cards of the same rank
        if self.is_of_kind(2, pairs):
            return 'Pair'
        # For everything else
        return 'High Card'

    def is_of_kind(self, number, pairs):
        """
        Returns if the hand has has a certain number
        of matching card ranks
        """
        return pairs[-1] >= number

    def get_repeating_values(self, value_type):
        """
        Returns all the repeating ranks or suits in a hand,
        depending on value_type
        """
        # The ranks list stores each unique rank in the hand,
        # and ranks_amount stores how many times that rank
        # appears in the hand
        values = []
        value_amount = []
        for card in self.cards:
            # Checking if this rank already exists in ranks
            found_value = False
            # Getting what property of the card will be checked
            # for repeats
            card_value = card.rank
            if value_type == 'suit':
                card_value = card.suit

            for i in range(len(values)):
                if card_value == values[i]:
                    found_value = True
                    value_amount[i] += 1
                    break
            # Add the value to the list if it does not exist
            if not found_value:
                values.append(card_value)
                value_amount.append(1)
        # Sorts the pairs in ascending order, so the largest
        # is at the end
        value_amount.sort()
        return value_amount

    def is_straight(self, hand_checking):
        """
        Checks if 5 cards are ranked in consecutive order
        and, if true, returns the highest card in the
        straight. Returns None if false
        """
        # The list is copied because values will be removed
        cards = hand_checking.copy()
        spare_wildcards = self.cards_sorted['wildcards']
        # Start at the lowest ranked card and work its way up
        previous_rank = 0
        straight_streak = 0
        high_card = None
        for card in cards:
            rank = card.get_rank_value()
            # For resetting the straight check algorithm
            if straight_streak == 0:
                straight_streak = 1
                previous_rank = rank
                continue
            # Adding 1 to the streak if conditions are met.
            # If the rank is the same as the previous rank then
            # the loop will ignore it
            if rank == previous_rank + 1:
                straight_streak += 1
                previous_rank = rank
                if straight_streak >= 5:
                    high_card = card
                continue
            # If the hand breaks anyt of the rules
            # set for the straight
            if rank > previous_rank + 1 or rank == previous_rank + 1:
                if spare_wildcards <= 0:
                    # Triggering the reset
                    straight_streak = 0
                    spare_wildcards = self.cards_sorted['wildcards']
                    continue
                else:
                    spare_wildcards -= 1
        return high_card

    def is_straight_flush(self):
        """
        Checks if 5 cards are ranked in consecutive order
        and of the same suit, if true, returns the highest card
        in the straight. Returns None if false
        """
        # Sorts each card by its suit into a list of lists
        suits = []
        for suit_sorting in CardType.type_format['suit']:
            # Add an empty list for each suit
            suits.append([])
            for card in self.cards_sorted['cards']:
                if card.suit == suit_sorting:
                    # Adds the card to the newest list
                    suits[-1].append(card)
        # Checking each suit for a straight
        for hand_suit in suits:
            high_card = self.is_straight(hand_suit)
            if high_card is not None:
                return high_card
        return None

    def take_from_deck(self, deck, number):
        """
        Sets this hand to a given number of random cards
        """
        cards_list = []
        for i in range(0, number):
            card = deck.take_card()
            cards_list.append(card)
        self.cards = cards_list


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
        for card in cards_list:
            if (self.rank == card.rank and
                    self.suit == card.suit):
                return True
        return False

    def get_rank_value(self):
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

    def convert(self, deck):
        """
        Converts a string into an instance of Card and returns it, if valid
        """
        rank = self.get('rank')
        if rank is not None:
            suit = self.get('suit')
            if suit is not None:
                card_obj = deck.get_card(rank, suit)
                # If the card doesn't exist in the deck, then the card
                # exists somewhere else
                if card_obj is None:
                    print_error(f'Multiple {rank} of {suit}')
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


def convert_hand(cards_list, deck):
    """
    Converts a list of strings into a list of objects
    containing the rank and the suit
    Example: "10 of Diamonds" => {'rank': 10, 'suit': 'Diamonds'}
    """
    new_cards = []
    for card in cards_list:
        card_obj = card.convert(deck)
        if card_obj is not None:
            deck.take_card(card_obj)
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


def validate_hand(cards_list, deck):
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
        print_error(e)
        return None
    else:
        formatted_hand = convert_hand(cards_list, deck)
        return formatted_hand


def get_hand_input(deck):
    """
    Requests a hand to be manually entered by the user, and returns
    an instance of Hand
    """
    # Keep requesting an input from the user until a valid hand is entered
    while True:
        print('Please enter your poker hand, or "random" for a random hand')
        print(
            '- Your hand must contain at least 5 cards, separated by a comma.'
        )
        print('- Each card must clearly indicate its rank and its suit.')
        print('- Example: "King of Hearts", "King Heart", "KH"\n')
        hand_input = input('Enter hand here: ')

        # Creates a random hand if the user specifies it
        if contains_word(hand_input, 'random'):
            new_hand = Hand([])
            deck.shuffle()
            new_hand.take_from_deck(deck, 5)
            return new_hand

        # Splits the inputs into separate elements in a list
        hand_list = hand_input.split(',')
        card_objects = []
        for card_text in hand_list:
            card_object = CardType(card_text)
            card_objects.append(card_object)

        cards = validate_hand(card_objects, deck)
        if cards is not None:
            new_hand = Hand(cards)
            return new_hand


def get_wildcards():
    """
    Requests the user to enter a set of wild cards that
    can affect the hand
    """
    while True:
        print('\nPlease enter any wild cards,')
        print('or press Enter if there are none\n')
        print('- Only enter the rank of the card, i.e. 2 - Ace')
        print('- Wild cards are cards that can take form of any')
        print('  rank or suit to make the best possible hand.\n')
        wildcards = input('Wild Cards: ')
        if wildcards == '':
            return []
        cards_list = wildcards.split(',')
        wildcard_ranks = []
        is_valid = True
        # Checking each input for a valid rank
        for card_text in cards_list:
            card = CardType(card_text)
            rank = card.get('rank')
            if rank is not None:
                wildcard_ranks.append(rank)
            else:
                # Exits the for loop if one of the inputs
                # is not valid
                is_valid = False
                break
        # Only return the wild cards once all of them are valid.
        # Repeat the while loop if there are invalid wild cards
        if is_valid:
            return wildcard_ranks


def get_rank_name(rank_number):
    """
    Returns the rank of a given card as a string,
    consisting of the rank's full name
    """
    # For cards greater than 10
    if rank_number > 10:
        worded_ranks = CardType.type_format['rank']
        # The 11th rank will be "Jack", which is the first
        # element [0] in CardType.type_format
        return worded_ranks[rank_number - 11]
    return str(rank_number)


def print_error(message):
    """
    Prints a specific user input error to the terminal
    """
    print(f'Invalid input: {message}. Please try again.\n')


def contains_word(input, word):
    """
    Returns true if a player input contains a given word
    """
    input_lower = input.lower()
    return word in input_lower


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!\n')
    deck = Deck()
    hand_input = get_hand_input(deck)
    wildcards = get_wildcards()
    print('\nYour Hand:')
    hand_input.print_hand()
    print('\nValue:')
    print(hand_input.get_value())


main()
