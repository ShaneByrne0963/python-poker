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
            for rank in range(2, 15):
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
            f'No {card.description(False)} in deck'
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
            print(card.description(True))

    def sort(self):
        """
        Sorts the cards in descending order, removing
        any wildcards and storing them in an integer
        """
        # Resetting the sorted hand if previously sorted
        self.cards_sorted = {
            'cards': [],
            'wildcards': 0
        }
        cards_template = self.cards.copy()
        while len(cards_template) > 0:
            # Finding the highest card in the list
            highest_card = None
            highest_value = 0
            for card in cards_template:
                card_val = card.rank
                if card_val > highest_value:
                    highest_card = card
                    highest_value = card_val
            if highest_card.is_wild():
                self.cards_sorted['wildcards'] += 1
            else:
                # Moving the highest card to the sorted cards dict
                self.cards_sorted['cards'].append(highest_card)
            cards_template.remove(highest_card)

    def get_value(self):
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
            if straight_high == 'Ace':
                return 'Royal Flush'
            return 'Straight Flush'
        # If the hand has 4 cards of the same rank
        if self.is_of_kind(4, pairs):
            return '4 of a Kind'
        # If the hand has 3 cards of the same rank and
        # a pair of a different rank
        if self.is_full_house(pairs):
            return 'Full House'
        # If the hand has 5 cards of the same suit
        suits = self.get_repeating_values('suit')
        if suits[-1] + self.cards_sorted['wildcards'] >= 5:
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
        wildcards = self.cards_sorted['wildcards']
        return pairs[-1] + wildcards >= number

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
        for card in self.cards_sorted['cards']:
            # Getting what property of the card will be checked
            # for repeats
            card_value = card.rank
            if value_type == 'suit':
                card_value = card.suit

            if card_value in values:
                index = values.index(card_value)
                value_amount[index] += 1
            else:
                # Add the value to the list if it does not exist
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
        # Duplicating the wild cards as it will be altered
        # for this evaluation
        wildcards = self.cards_sorted['wildcards']
        # Start at the lowest ranked card and work its way up
        previous_rank = 0
        straight_streak = 0
        high_rank = None
        i = 0
        while i < len(hand_checking):
            card = hand_checking[i]
            i += 1
            rank = card.rank
            # Restarting the straight evaluation
            if (straight_streak == 0 or
                    (rank < previous_rank - 1 and wildcards <= 0)):
                straight_streak = 1
                previous_rank = rank
                high_rank = rank
                wildcards = self.cards_sorted['wildcards']
                continue
            # If the rank is the same as the previous rank then
            # the loop will ignore it
            if rank < previous_rank:
                if rank < previous_rank - 1:
                    wildcards -= 1
                    # Starting the next iteration of the loop at the
                    # same card if a wild card is used in its place
                    i -= 1
                straight_streak += 1
                previous_rank -= 1
                if straight_streak >= 5 - wildcards:
                    # Adding any spare wild cards to the high end
                    # of the straight
                    high_rank += wildcards
                    # Capping the rank value at 14 (Ace)
                    if high_rank > 14:
                        high_rank = 14
                    return get_rank_name(high_rank)
        return None

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

    def is_full_house(self, pairs):
        """
        Returns True if the hand has 3 ranks of the same
        kind, and a pair of a different rank
        """
        wildcards = self.cards_sorted['wildcards']
        # Checking for the 3 of a Kind part of the Full House
        if not self.is_of_kind(3, pairs):
            return False
        # Removing any wildcards that were used for the first part
        # so they cannot be used again
        if pairs[-1] < 3:
            wildcards -= 3 - pairs[-1]
        # Checking for the pair
        return pairs[-2] + wildcards >= 2

    def take_from_deck(self, number):
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

    def description(self, extra_details):
        """
        Returns the cards rank and suit as a readable string,
        and if it is a wild card if specified
        """
        rank_name = get_rank_name(self.rank)
        desc_text = f'{rank_name} of {self.suit}'
        if extra_details and self.is_wild():
            desc_text += ' (Wild)'
        return desc_text

    def is_duplicate(self, cards_list):
        """
        Returns if this card already exists in a list of cards
        """
        for card in cards_list:
            if (self.rank == card.rank and
                    self.suit == card.suit):
                return True
        return False

    def is_wild(self):
        """
        Returns if this card is a wild card
        """
        return self.rank in deck.wildcards


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

    def get(self):
        """
        Reads the card input and returns a list of ranks and
        suits that best match the input
        """
        # Stores the found cards that consist of
        # the most letters of the input
        best_matches = []
        match_score = 0

        # Divides the input into words if there are spaces in it
        input_words = self.text.split(' ')

        # Iterating through all the ranks a card can have
        for rank in range(2, 15):
            # Creating a copy of the input words to delete elements from
            temp_words = input_words.copy()
            rank_word = get_rank_name(rank)

            found_rank = self.find_value(temp_words, rank_word)
            if found_rank is not None:
                # Removing the found rank so it can't also be used by the suit
                temp_words = self.remove_value(temp_words, found_rank)

                for suit in CardType.type_format['suit']:
                    found_suit = self.find_value(temp_words, suit)
                    if found_suit is not None:
                        # The amount of letters of both the found rank and suit
                        content_length = len(found_rank) + len(found_suit)
                        # What percent of the input consists of those letters
                        content_percent = get_percent(
                            content_length, len(self.text)
                        )
                        if content_percent >= match_score:
                            if content_percent > match_score:
                                match_score = content_percent
                                best_matches.clear()
                            found_card = {
                                'rank': rank,
                                'suit': suit,
                            }
                            best_matches.append(found_card)
        return best_matches

    def find_value(self, words, value):
        """
        Finds a given value in a list of words. Returns None if
        no value is found
        """
        if len(words) > 1:
            # If there are multiple words in the input,
            # iterate through all of them
            for word in words:
                if contains_word(word, value):
                    return word
            return None
        else:
            # If the input is simply one string, only the
            # part of the string that contains the word will be
            # returned
            return extract_word(words[0], value)

    def remove_value(self, words, value):
        """
        Removes a given value from a list of words, and returns
        a list of remaining words
        """
        if len(words) > 1:
            words.remove(value)
            return words
        else:
            reduced_word = words[0].replace(value, '')
            return [reduced_word]

    def has_input(self, input_words):
        """
        Returns if an input contains any text to be evaluated
        """
        for word in input_words:
            if len(word) > 0:
                return True
        return False

    def convert(self):
        """
        Converts a string into an instance of Card and returns it, if valid
        """
        card_objects = self.get()
        if len(card_objects) > 1:
            print_error(f'Multiple cards detected in "{self.text}"')
        if len(card_objects) == 1:
            rank = card_objects[0]['rank']
            suit = card_objects[0]['suit']
            # Converting the rank number into text that is readable by the user
            rank_num = get_rank_value(rank)
            card_obj = deck.get_card(rank_num, suit)
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


def convert_hand(cards_list):
    """
    Converts a list of strings into a list of objects
    containing the rank and the suit
    Example: "10 of Diamonds" => {'rank': 10, 'suit': 'Diamonds'}
    """
    new_cards = []
    for card in cards_list:
        card_obj = card.convert()
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
        print_error(e)
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
        print_error(e)
        return None
    else:
        formatted_hand = convert_hand(cards_list)
        return formatted_hand


def get_hand_input():
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
            new_hand.take_from_deck(5)
            return new_hand

        # Splits the inputs into separate elements in a list
        hand_list = hand_input.split(',')
        card_objects = []
        for card_text in hand_list:
            # Removing any white space from the edge of each card input
            text_stripped = card_text.strip()
            card_object = CardType(text_stripped)
            card_objects.append(card_object)

        cards = validate_hand(card_objects)
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


def get_rank_value(rank_name):
    """
    Returns the rank of the card as an integer
    """
    if rank_name in CardType.type_format['rank']:
        return CardType.type_format['rank'].index(rank_name) + 11
    return int(rank_name)


def print_error(message):
    """
    Prints a specific user input error to the terminal
    """
    print(f'Invalid input: {message}. Please try again.\n')


def contains_word(input_word, word):
    """
    Returns True if an input is similar to a given word
    """
    if len(input_word) == 0:
        return False
    input_list = string_to_list(input_word)
    word_list = string_to_list(word)

    # The first letters have to be the same for them to match
    if input_list[0] != word_list[0]:
        return False
    # We start with one matching word as at this
    # point the first letter matches the word
    matching_letters = 1
    total_letters = 1
    # Removing the first letter from the input and the word
    input_list = input_list[1:]
    word_list = word_list[1:]
    # If input_word has 2 or 3 characters, then the last
    # letter has to match the last letter of the word
    if ((len(input_list) == 1 or len(input_list) == 2) and
            len(word) > 1):
        if input_list[-1] != word_list[-1]:
            return False
        # Remove the last letter from each of the words
        input_list = input_list[:-1]
        word_list = word_list[:-1]
    # Going through each of the characters in the input to
    # check if it exists in the word
    for char in input_list:
        total_letters += 1
        if char in word_list:
            matching_letters += 1
            # Removing the character from the word to
            # avoid duplicates
            word_list.remove(char)
    match = get_percent(matching_letters, total_letters)
    # If the amount of characters that match the word is at
    # least 80%, then the word is considered a match
    return match >= 80


def extract_word(input_word, word):
    """
    Returns part of an input string that contains a given word
    """
    if len(input_word) == 0:
        return None
    input_list = string_to_list(input_word)
    word_list = string_to_list(word)

    # Searching the input for the first letter of the word
    index = 0
    while input_list[index] != word_list[0]:
        index += 1
        if index >= len(input_list):
            return None
    final_string = input_word[index]

    # Only returning the first character if the input
    # has 3 or less characters
    if len(input_word) <= 3:
        return final_string

    index += 1
    matching_letters = 1
    total_letters = 1
    # Keep iterating through the input until the end is
    # reached, or the word stops being similar
    while (index < len(input_list) and
            get_percent(matching_letters, total_letters) >= 80):
        total_letters += 1
        char = input_list[index]
        if char in word_list:
            matching_letters += 1
            final_string += input_word[index]
            word_list.remove(char)
        index += 1
    if len(final_string) == 2 or len(final_string) == 3:
        if final_string[-1] != word[-1]:
            return None
    return final_string


def string_to_list(text):
    """
    Converts a string into a list, with each character being an
    individual element.
    """
    text_lower = text.lower()
    text_lower = text_lower.strip()
    new_list = []
    for char in text_lower:
        new_list.append(char)
    return new_list


def get_percent(value, total):
    """
    Returns what percentage value is of total
    """
    return (value / total) * 100


def main():
    """
    Initializes the game.
    """
    print('Welcome to Python Poker!\n')
    # Creates the deck
    global deck
    deck = Deck()

    # deck.wildcards = [2]
    # deck.shuffle()
    # hand_input = Hand([])
    # hand_input.take_from_deck(5)
    # while hand_input.get_value() != 'Royal Flush':
    #     deck.cards = deck.get_full()
    #     deck.shuffle()
    #     hand_input.cards = []
    #     hand_input.take_from_deck(5)

    # Instructs the user to enter their hand
    hand_input = get_hand_input()

    wildcards = get_wildcards()
    deck.wildcards = wildcards

    print('\nYour Hand:')
    hand_input.print_hand()
    print('\nValue:')
    print(hand_input.get_value())


# main()

card_input = input('Enter a card: ')
new_card = CardType(card_input)
card_type = new_card.to_replace_get()
for element in card_type:
    card = Card(element['rank'], element['suit'])
    print(card.description(False))
