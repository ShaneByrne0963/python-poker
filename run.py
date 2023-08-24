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
        for suit in CardType.suits:
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
        card_desc = get_card_description(card.rank, card.suit)
        print_error(f'No {card_desc} in deck')
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
    def __init__(self, name, cards):
        """
        Creates an instance of Hand
        """
        self.name = name
        self.cards = cards
        self.cards_sorted = {
            'cards': [],
            'wildcards': 0
        }
        self.value = {
            'name': '',
            'score': 0,
            'subscore': 0,
            'high_card': 0
        }

    def print_hand(self):
        """
        Prints each card in this hand to the terminal
        """
        print_text = f'{self.name}:'
        if len(print_text) >= 8:
            print_text += '\t'
        else:
            print_text += '\t\t'
        for card in self.cards:
            print_text += f'{card.description()}\t'
        print_text += self.value['name']
        print(print_text)

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

    def set_value(self):
        """
        Stores the value of the hand in its instance
        """
        self.value = self.get_value()

    def get_value(self):
        """
        Checks if the hand has a certain card combination,
        starting with the highest value and working its way
        down until a match is found
        """
        found_value = {
            'name': '',
            'score': 0,
            'subscore': 0,
            'high_card': 0
        }
        self.sort()
        found_value['high_card'] = self.cards_sorted['cards'][0]

        pairs = self.get_repeating_values('rank')
        straight_flush = self.is_straight_flush()
        straight = self.is_straight(self.cards_sorted['cards'])
        suits = self.get_repeating_values('suit')
        # If the hand has 5 cards of the same rank (with wildcards)
        if self.is_of_kind(5, pairs):
            found_value['name'] = '5 of a Kind'
            found_value['score'] = 11
        # If the hand has 5 consecutive ranking cards of the same suit
        elif straight_flush is not None:
            if straight_high == 'Ace':
                found_value['name'] = 'Royal Flush'
                found_value['score'] = 10
            else:
                found_value['name'] = 'Straight Flush'
                found_value['score'] = 9
        # If the hand has 4 cards of the same rank
        elif self.is_of_kind(4, pairs):
            found_value['name'] = '4 of a Kind'
            found_value['score'] = 8
        # If the hand has 3 cards of the same rank and
        # a pair of a different rank
        elif self.is_full_house(pairs):
            found_value['name'] = 'Full House'
            found_value['score'] = 7
        # If the hand has 5 cards of the same suit
        elif suits[0]['amount'] + self.cards_sorted['wildcards'] >= 5:
            found_value['name'] = 'Flush'
            found_value['score'] = 6
        # If the hand has 5 consecutive ranking cards
        elif straight is not None:
            found_value['name'] = 'Straight'
            found_value['score'] = 5
        # If the hand has 3 cards of the same rank
        elif self.is_of_kind(3, pairs):
            found_value['name'] = '3 of a Kind'
            found_value['score'] = 4
        # If the hand has 2 pairs of cards of the same rank
        elif self.count_repeating_values(pairs, 2) >= 2:
            found_value['name'] = 'Two Pair'
            found_value['score'] = 3
        # If the hand has 2 cards of the same rank
        elif self.is_of_kind(2, pairs):
            found_value['name'] = 'Pair'
            found_value['score'] = 2
        # For everything else
        else:
            found_value['name'] = 'High Card'
            found_value['score'] = 1
        return found_value

    def is_of_kind(self, number, pairs):
        """
        Returns if the hand has has a certain number
        of matching card ranks
        """
        wildcards = self.cards_sorted['wildcards']
        return pairs[0]['amount'] + wildcards >= number

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
        # Sorts the pairs in descending order by amount of ranks
        final_values = []
        for index in range(len(values)):
            value_dict = {
                'value': values[index],
                'amount': value_amount[index]
            }
            final_values.append(value_dict)
        final_values = sort_dict_list(
            final_values, False, 'amount', 'value'
        )
        return final_values

    def count_repeating_values(self, values, number):
        """
        Returns how many groups of (rank * number) the
        hand has
        """
        value_count = 0
        for value in values:
            if value['amount'] == number:
                value_count += 1
        return value_count

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
        for suit_sorting in CardType.suits:
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
        if pairs[0]['amount'] < 3:
            wildcards -= 3 - pairs[-1]
        # Checking for the pair
        return pairs[1]['amount'] + wildcards >= 2

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

    def description(self):
        """
        Returns the cards rank and suit as a single word,
        only giving the first letter of worded ranks and suits
        and highlighting wild cards with **
        """
        wild = self.is_wild()
        desc_text = ''
        if wild:
            desc_text = '*'
        rank_name = get_rank_name(self.rank)
        simple_rank = self.rank
        if self.rank > 10:
            simple_rank = rank_name[0]
        desc_text += f'{simple_rank}{self.suit[0]}'
        if wild:
            desc_text += '*'
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
    ranks = ['Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

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
        has_suits = False
        # Divides the input into words if there are spaces in it
        input_words = self.text.split(' ')

        ranks = self.find_values(input_words, 'rank')
        if len(ranks) == 0:
            print_error(f'No ranks found in "{self.text}"')
            return None
        for rank in ranks:
            temp_words = input_words.copy()
            temp_words = self.remove_value(temp_words, rank['found'])
            # If any rank takes up the entire input,
            # then there are no suits in it
            if not self.has_input(temp_words):
                has_suits = False
                break
            suits = self.find_values(temp_words, 'suit')
            for suit in suits:
                has_suits = True
                # The amount of letters of both the found rank and suit
                content_length = len(rank['found']) + len(suit['found'])
                # What percent of the input consists of those letters
                content_percent = get_percent(
                    content_length, len(self.text)
                )
                if content_percent >= match_score:
                    if content_percent > match_score:
                        match_score = content_percent
                        best_matches.clear()
                    found_card = {
                        'rank': rank['value'],
                        'suit': suit['value'],
                    }
                    best_matches.append(found_card)
        if not has_suits:
            print_error(f'No suits found in "{self.text}"')
            return None
        return best_matches

    def find_values(self, words, value_type):
        """
        Gets all the ranks or suits found in an input
        """
        found_values = []
        # Finding out what to compare the words to
        checking_values = (
            range(2, 15) if value_type == 'rank' else CardType.suits
        )
        for value in checking_values:
            # Converting rank numbers to string format when necessary
            value_to_check = (
                get_rank_name(value) if value_type == 'rank' else value
            )
            found_value = self.find_single_value(words, value_to_check)

            if found_value is not None:
                # Returns both the word that was found and the word that
                # it could be referring to
                val_object = {
                    'value': value,
                    'found': found_value
                }
                found_values.append(val_object)
        return found_values

    def find_single_value(self, words, value):
        """
        Finds a given rank or suit in a list of words. Returns
        None if no value is found
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
        Converts a string into an instance of Card
        """
        # Returns an error if an input contains no text
        if self.text == '':
            print_error('Blank card detected')
            return None
        card_objects = self.get()
        if card_objects is not None:
            # If the evaluation finds more than one card in an input
            if len(card_objects) > 1:
                # Printing out each card found in the error
                found_cards = []
                for card in card_objects:
                    card_desc = get_card_description(
                        card['rank'], card['suit']
                    )
                    found_cards.append(card_desc)
                print_error(
                    f'Multiple cards detected in "{self.text}"', found_cards
                )
                return None
            if len(card_objects) == 1:
                rank = card_objects[0]['rank']
                suit = card_objects[0]['suit']
                card_obj = deck.get_card(rank, suit)
                # If the card doesn't exist in the deck, then the card
                # exists somewhere else
                if card_obj is None:
                    card_desc = get_card_description(rank, suit)
                    print_error(f'Multiple {card_desc}')
                return card_obj
        return None


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
        # Returning any cards taken from this hand
        # if one is invalid
        deck.cards.extend(new_cards)
        return None
    return new_cards


def validate_hand(cards_list):
    """
    Checks if a poker hand entered by the user can
    produce a valid set of cards
    """
    formatted_hand = []
    # Each hand must contain at least 5 cards
    if len(cards_list) < 5:
        print_error(
            f'Need at least 5 cards. You have given {len(cards_list)}'
        )
    else:
        formatted_hand = convert_hand(cards_list)
        return formatted_hand


def get_hand_input():
    """
    Requests a hand to be manually entered by the user, and returns
    an instance of Hand
    """
    player_name = get_required_input('Name', 'Please enter your name: ')
    print(f'Welcome {player_name}!\n')
    print('Please enter your poker hand, or "random" for a random hand.')
    # Keep requesting an input from the user until a valid hand is entered
    while True:
        print(
            '- Your hand must contain at least 5 cards, separated by a comma.'
        )
        print('- Each card must contain a rank and a suit.')
        print('- Example: "King of Hearts", "King Heart", "KH"\n')
        hand_input = get_required_input('Hand', 'Enter hand here: ')
        print('')

        # Creates a random hand if the user specifies it
        if contains_word(hand_input, 'random'):
            new_hand = Hand(player_name, [])
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
            new_hand = Hand(player_name, cards)
            return new_hand


def get_required_input(type, message):
    """
    Requests an input from the user continuously until
    an input is given
    """
    user_input = ''
    while user_input == '':
        user_input = input(message)
        if user_input == '':
            print_error(f'{type} is blank')
    return user_input


def get_card_description(rank, suit):
    """
    Returns the cards rank and suit as a readable string
    """
    rank_name = get_rank_name(rank)
    return f'{rank_name} of {suit}'


def get_wildcards():
    """
    Requests the user to enter a set of wild cards that
    can affect the hand
    """
    request_message = 'Do you wish to include wildcards in your game?\n'
    request_message += '- Wild cards are cards that can take form of any\n'
    request_message += '  rank or suit to make the best possible hand.'
    if user_allows(request_message):
        while True:
            print('Please enter any wild cards')
            print('- Only enter the rank of the card, i.e. 2 - Ace')
            wildcards = input('Wild Cards: ')
            # Adds a gap between the input and the next print
            print('')
            if wildcards == '':
                if user_allows('No wild cards entered. Continue?'):
                    return []
                else:
                    continue
            cards_list = wildcards.split(',')
            wildcard_ranks = []
            is_valid = True
            # Checking each input for a valid rank
            for card_text in cards_list:
                # Printing an error if an empty input is detected
                if card_text == '':
                    print_error('Blank card detected')
                    is_valid = False
                    # Exiting the for loop
                    break
                card = CardType(card_text)
                ranks = card.find_values(card_text.split(' '), 'rank')
                if len(ranks) == 0:
                    print_error(f'No ranks found in "{card_text}"')
                    is_valid = False
                    break
                for rank in ranks:
                    wildcard_ranks.append(rank['value'])
            # Only return the wild cards once all of them are valid.
            # Repeat the while loop if there are invalid wild cards
            if is_valid:
                return wildcard_ranks
    else:
        return []


def get_rank_name(rank_number):
    """
    Returns the rank of a given card as a string,
    consisting of the rank's full name
    """
    # For cards greater than 10
    if rank_number > 10:
        # The 11th rank will be "Jack", which is the first
        # element [0] in CardType.ranks
        return CardType.ranks[rank_number - 11]
    return str(rank_number)


def get_rank_value(rank_name):
    """
    Returns the rank of the card as an integer
    """
    if rank_name in CardType.ranks:
        return CardType.ranks.index(rank_name) + 11
    return int(rank_name)


def get_best_hand(hands):
    """
    Returns the hand with the best value out of a
    given list of hands
    """
    best_hand = None
    for hand in hands:
        if best_hand is None:
            best_hand = hand
            continue
        hand_score = hand.value['score']
        best_score = best_hand.value['score']
        if hand_score > best_score:
            best_hand = hand
    return best_hand


def print_error(message, bullet_points=None):
    """
    Prints a specific user input error to the terminal
    """
    error_message = f'Invalid input: {message}'
    # Support for bullet points
    if bullet_points is not None:
        error_message += ':\n'
        for point in bullet_points:
            error_message += f'- {point}\n'
    else:
        error_message += '. '
    error_message += 'Please try again.\n'
    print(error_message)


def contains_word(input_word, word):
    """
    Returns True if an input is similar to a given word
    """
    # region How this function works:
    """
     1. The function begins by checking if the first letter of
        the input is the same as the first of the word. This is
        required for the input to match the word
     2. Then the amount of characters that exist in both the
        input and the word will be counted
     3. If this count is at least 75% of the total letters in the
        input, then the words are considered a match and the
        function will return True
     4. The function will return False in every other case
    """
    # endregion

    if len(input_word) == 0:
        return False
    # Lists have more functions that are useful for this evaluation
    input_list = string_to_list(input_word)
    word_list = string_to_list(word)

    # The first letters have to be the same for them to match
    if input_list[0] != word_list[0]:
        return False
    matching_letters = 1
    total_letters = 1

    input_list = input_list[1:]
    word_list = word_list[1:]
    # Checking if each letter in the input is in the word
    for char in input_list:
        total_letters += 1
        if char in word_list:
            matching_letters += 1
            # Each letter in the word cannot be used twice
            word_list.remove(char)
    if word.isdigit() and len(word_list) > 0:
        return False
    match = get_percent(matching_letters, total_letters)
    # 75% of the input's characters must exist in the word
    return match >= 75


def extract_word(input_word, word):
    """
    Returns part of an input string that contains a given word
    """
    # region How this function works:
    """
     1. The function starts by iterating through each character of
        the input until the first character of the word is found.
        If this character isn't found the function will return None
     2. If the input is 2 characters or less, the function will
        return this first character on its own
     3. If not, the character will be added to a string,
        final_string, which will be returned at the end of the
        function.
     4. Then the function will iterate through the rest of the
        characters and check if they exist in the word. If the
        percentage of characters that match the word is at least
        75%, the character will be added to final_string
     5. Once the loop reaches the end of the input, or the total
        match falls below 75%, final_string will be returned
    """
    # endregion

    if len(input_word) == 0:
        return None
    # Lists have more functions that are useful for this evaluation
    input_list = string_to_list(input_word)
    word_list = string_to_list(word)

    # Searching the input for the first letter of the word
    index = 0
    while input_list[index] != word_list[0]:
        index += 1
        if index >= len(input_list):
            return None
    final_string = input_word[index]
    word_list.pop(0)
    # Returning the first letter for small inputs
    if len(input_word) <= 2:
        return final_string
    index += 1
    matching_letters = 1
    total_letters = 1
    # If there is a misspelling in the word, the mistake is
    # stored here, and will be added if the word continues
    unmatching_letters = ''

    while index < len(input_list):
        total_letters += 1
        char = input_list[index]
        if char in word_list:
            matching_letters += 1
            final_string += input_word[index]
            word_list.remove(char)
            # Adding the previous characters that didn't match
            final_string += unmatching_letters
            unmatching_letters = ''
        else:
            # Storing the unmatch in case it's a spelling error
            unmatching_letters += char
        if (get_percent(matching_letters, total_letters) < 75 or
                len(word_list) == 0):
            break
        index += 1
    # For numbers, the extraced word must contain the full number
    if word.isdigit() and len(word_list) > 0:
        return None
    return final_string


def user_allows(message):
    """
    Asks a user a yes/no question, and returns True or
    False depending on what the user entered
    """
    while True:
        print(message)
        answer = input('Your answer (Y/N): ')
        print('')
        if contains_word(answer, 'Yes'):
            return True
        elif contains_word(answer, 'No'):
            return False
        else:
            print('Please enter Yes (Y) or No (N)')


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


def sort_dict_list(dict_list, ascending, *keys):
    """
    Sorts a list of dictionaries in ascending/descending
    order in terms of it's given keys, with the first
    given key taking precedence
    """
    sorted_list = []
    while len(dict_list) > 0:
        best_value = dict_list[0]
        best_index = 0
        for index in range(1, len(dict_list)):
            is_best = True
            for key in keys:
                current_key = dict_list[index][key]
                # Skip this iteration if the value is a string
                if isinstance(current_key, str):
                    continue
                # Determining whether this index has the best
                # value depending on the order of the list
                if current_key < best_value[key]:
                    is_best = ascending
                    break
                if current_key > best_value[key]:
                    is_best = not ascending
                    break
                # The for loop only continues if the values at
                # this key are equal. Then the loop will move
                # to a lower priority key
            if is_best:
                best_value = dict_list[index]
                best_index = index
        sorted_list.append(best_value)
        dict_list.pop(best_index)
    return sorted_list


def get_percent(value, total):
    """
    Returns what percentage value is of total
    """
    return (value / total) * 100


def main():
    """
    Initializes the game.
    """
    # Creates the deck
    global deck
    deck = Deck()
    print('Welcome to Python Poker!\n')
    print('Python Poker will read one or more poker hands,')
    print('taking wild cards into consideration, and will')
    print('the values of each hand, as well as the winner.\n')
    wildcards = get_wildcards()
    deck.wildcards = wildcards

    # Adding different player hands
    player_hands = []
    while True:
        hand_input = get_hand_input()
        player_hands.append(hand_input)
        print('Name:\t\tCards:\t\t\t\t\tValue:')
        for hand in player_hands:
            hand.set_value()
            hand.print_hand()
        if len(player_hands) > 1:
            best_hand = get_best_hand(player_hands)
            print(f'Winning hand: {best_hand.name}')
        if not user_allows('\nDo you wish to add another hand?'):
            break
    print('Thank you for using Python Poker! Goodbye!')


main()
