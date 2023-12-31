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
        for suit in CardInput.suits:
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
        if card in self.cards:
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
        self.cards_sorted = []
        self.wildcards = 0
        # Used to store cards that wild cards are imitating
        self.fake_cards = []
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
        # Adding the spacing after the player name
        if len(print_text) >= 8:
            print_text += '\t'
        else:
            print_text += '\t\t'
        # Printing each card
        for card in self.cards:
            card_desc = card.description()
            print_text += card_desc
            if len(self.cards) <= 6:
                print_text += '\t'
            else:
                # Reducing the spacing for larger hands
                space_amount = 6 - len(card_desc)
                while space_amount > 0:
                    print_text += ' '
                    space_amount -= 1
        print_text += self.value['name']
        print(print_text)

    def format_hand(self):
        """
        Updates the cards_sorted value of this hand, sorting
        the cards in descending order
        Sorts the cards in descending order in a dictionary,
        removing any wildcards and storing them separately, and
        setting self.cards_sorted to this dictionary
        """
        self.wildcards = 0
        for card in self.cards:
            if card.is_wild():
                self.wildcards += 1

        self.cards_sorted = self.sort(self.cards, True)

    def sort(self, hand_list, remove_wild):
        """
        Sorts a given hand by its rank in descending order
        """
        cards_temp = hand_list.copy()
        cards_sorted = []
        while len(cards_temp) > 0:
            # Finding the highest ranking card in the list
            highest_card = None
            for card in cards_temp:
                if (highest_card is None or
                        card.rank > highest_card.rank):
                    highest_card = card
            # Only add wild cards if specified
            if not (remove_wild and highest_card.is_wild()):
                cards_sorted.append(highest_card)
            cards_temp.remove(highest_card)
        return cards_sorted

    def add_fake_card(self, rank, suit=''):
        """
        Adds a card that a wild card is imitating to the
        hand. This card is not part of the main deck
        """
        fake_card = Card(rank, suit)
        self.fake_cards.append(fake_card)

    def combine_all_cards(self):
        """
        Returns a sorted list of all real and fake cards
        within this hand
        """
        new_cards = self.cards_sorted.copy()
        new_cards.extend(self.fake_cards)
        # For Flushes, only cards of the same suit matter
        if self.value['name'] == 'Flush':
            new_cards = self.get_suit_only(
                new_cards, self.value['subscore']
            )
        new_cards = self.sort(new_cards, False)
        return new_cards

    def get_suit_only(self, cards, suit):
        """
        Returns a hand that only contains a given suit
        """
        new_cards = []
        for card in cards:
            if card.suit == suit:
                new_cards.append(card)
        return new_cards

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
        self.format_hand()

        pairs = self.get_repeating_values('rank')
        current_kind = None
        # If all the cards in the hand are wild, set them all to Ace
        if len(self.cards_sorted) == 0:
            current_kind = 14
            for i in range(self.wildcards):
                self.add_fake_card(current_kind)
        # If the hand has 5 cards of the same rank
        else:
            current_kind = self.is_of_kind(5, pairs)
        if current_kind is not None:
            return self.create_value_dict('5 of a Kind', current_kind)
        # If the hand has 5 consecutive ranking cards of the same suit
        straight_high = self.is_straight_flush()
        if straight_high is not None:
            name = 'Straight Flush'
            # Rank 14 = Ace
            if straight_high == 14:
                name = 'Royal Flush'
            return self.create_value_dict(name, straight_high)
        # If the hand has 4 cards of the same rank
        current_kind = self.is_of_kind(4, pairs)
        if current_kind is not None:
            return self.create_value_dict('4 of a Kind', current_kind)
        # If the hand has 3 cards of the same rank and
        # a pair of a different rank
        house_ranks = self.is_full_house(pairs)
        if house_ranks is not None:
            return self.create_value_dict('Full House', house_ranks)
        # If the hand has 5 cards of the same suit
        flush_suit = self.is_flush()
        if flush_suit is not None:
            return self.create_value_dict('Flush', flush_suit)
        # If the hand has 5 consecutive ranking cards
        straight_high = self.is_straight(self.cards_sorted)
        if straight_high is not None:
            return self.create_value_dict('Straight', straight_high)
        # If the hand has 3 cards of the same rank
        current_kind = self.is_of_kind(3, pairs)
        if current_kind is not None:
            return self.create_value_dict('3 of a Kind', current_kind)
        # If the hand has 2 pairs of cards of the same rank
        pair_groups = self.count_repeating_values(pairs, 2)
        if len(pair_groups) >= 2:
            return self.create_value_dict('Two Pair', pair_groups)
        # If the hand has 2 cards of the same rank
        current_kind = self.is_of_kind(2, pairs)
        if current_kind is not None:
            return self.create_value_dict('Pair', current_kind)
        # For everything else
        return self.create_value_dict('High Card', 0)

    def create_value_dict(self, name, subscore):
        """
        Creates a dictionary containing all the information
        about the value of the hand and returns it
        """
        value_info = {}
        value_info['name'] = name
        if name == 'High Card':
            value_info['score'] = 1
        elif name == 'Pair':
            value_info['score'] = 2
        elif name == 'Two Pair':
            value_info['score'] = 3
        elif name == '3 of a Kind':
            value_info['score'] = 4
        elif name == 'Straight':
            value_info['score'] = 5
        elif name == 'Flush':
            value_info['score'] = 6
        elif name == 'Full House':
            value_info['score'] = 7
        elif name == '4 of a Kind':
            value_info['score'] = 8
        elif name == 'Straight Flush':
            value_info['score'] = 9
        elif name == 'Royal Flush':
            value_info['score'] = 10
        elif name == '5 of a Kind':
            value_info['score'] = 11
        value_info['subscore'] = subscore
        return value_info

    def is_of_kind(self, number, pairs):
        """
        Returns if the hand has has a certain number
        of matching card ranks, and returns that rank
        """
        self.fake_cards.clear()
        highest_amount = pairs[0]['amount']
        if highest_amount + self.wildcards >= number:
            # Adding the wild cards to the sorted hand as the
            # rank of the highest group of cards
            of_kind_rank = pairs[0]['value']
            while highest_amount < number:
                self.add_fake_card(of_kind_rank)
                highest_amount += 1

            return of_kind_rank
        return None

    def is_flush(self):
        """
        Evaluates if the hand has 5 cards of the same suit,
        returns the suit if it does, and None if it doesn't
        """
        self.fake_cards.clear()
        suits = self.get_repeating_values('suit')
        best_suit = suits[0]['value']
        suit_amount = suits[0]['amount']
        if suit_amount + self.wildcards >= 5:
            while suit_amount < 5:
                # Always pick the best rank for wild cards
                self.add_fake_card(14, best_suit)
                suit_amount += 1
            return best_suit
        return None

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
        for card in self.cards_sorted:
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
        value_counts = []
        for value in values:
            if value['amount'] == number:
                value_counts.append(value['value'])
        return value_counts

    def is_straight(self, hand_checking):
        """
        Checks if 5 cards are ranked in consecutive order
        and, if true, returns the highest card in the
        straight. Returns None if false
        """
        self.fake_cards.clear()
        # Duplicating the wild cards as it will be altered
        # for this evaluation
        wildcards = self.wildcards
        wildcard_ranks = []
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
                wildcards = self.wildcards
                wildcard_ranks.clear()
                continue
            # If the rank is the same as the previous rank then
            # the loop will ignore it
            if rank == previous_rank:
                continue
            if rank < previous_rank - 1:
                wildcards -= 1
                wildcard_ranks.append(previous_rank - 1)
                # Starting the next iteration of the loop at the
                # same card if a wild card is used in its place
                i -= 1
            straight_streak += 1
            previous_rank -= 1
            if straight_streak >= 5 - wildcards:
                # Adding the simulated wild cards to the sorted deck
                for wild_rank in wildcard_ranks:
                    self.add_fake_card(wild_rank)
                # Finding the best ranks for the remaining fake cards
                while wildcards > 0:
                    if high_rank < 14:
                        # Moving up the ranks until it reaches an Ace
                        high_rank += 1
                        self.add_fake_card(high_rank)
                    else:
                        # Moving down the ranks
                        self.add_fake_card(previous_rank)
                        previous_rank -= 1
                    wildcards -= 1
                return high_rank
        return None

    def is_straight_flush(self):
        """
        Checks if 5 cards are ranked in consecutive order
        and of the same suit. If true, returns the highest card
        in the straight. Returns None if false
        """
        # Sorts each card by its suit into a list of lists
        suits = []
        for suit_sorting in CardInput.suits:
            # Add an empty list for each suit
            suits.append([])
            for card in self.cards_sorted:
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
        # Stores the ranks of the full house
        house_ranks = []
        # Checking for the 3 of a Kind part of the Full House
        three_pair = self.is_of_kind(3, pairs)
        if three_pair is None:
            return None
        house_ranks.append(three_pair)
        # Checking the second highest group of ranks
        two_pair = pairs[1]['amount']
        if two_pair < 2:
            return None
        house_ranks.append(two_pair)
        return house_ranks

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

    def is_wild(self):
        """
        Returns if this card is a wild card
        """
        return self.rank in deck.wildcards


class CardInput:
    """
    Stores a single card input by the user, and contains
    functions to convert that string into a card dictionary
    """
    ranks = ['Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, text):
        """
        Creates an instance of CardInput
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
        # At least 1 in 3 characters in the input must match the card
        match_score = 33
        has_ranks = False
        missing_rank_message = f'No ranks found in "{self.text}"'
        has_suits = False
        # Divides the input into words if there are spaces in it
        input_words = self.text.split(' ')

        ranks = self.find_values(input_words, 'rank')
        if len(ranks) == 0:
            print_error(missing_rank_message)
            return None
        for rank in ranks:
            temp_words = input_words.copy()
            temp_words = self.remove_value(temp_words, rank['found'])
            # If any rank takes up the entire input,
            # then there are no suits in it
            if not self.has_input(temp_words):
                has_ranks = True
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
                    has_ranks = True
                    if content_percent > match_score:
                        match_score = content_percent
                        best_matches.clear()
                    found_card = {
                        'rank': rank['value'],
                        'suit': suit['value'],
                    }
                    best_matches.append(found_card)
        if not has_ranks:
            print_error(missing_rank_message)
            return None
        if not has_suits:
            print_error(f'No suits found in "{self.text}"')
            return None
        return best_matches

    def find_values(self, words, value_type, remove_value=False):
        """
        Gets all the ranks or suits found in an input
        """
        # Removing values from words without affecting the original list
        words_copy = words.copy()
        found_values = []
        # Finding out what to compare the words to
        checking_values = (
            range(2, 15) if value_type == 'rank' else CardInput.suits
        )
        for value in checking_values:
            # Converting rank numbers to string format when necessary
            value_to_check = (
                get_rank_name(value) if value_type == 'rank' else value
            )
            found_value = self.find_single_value(
                words_copy, value_to_check
            )

            if found_value is not None:
                # Returns both the word that was found and the word that
                # it could be referring to
                val_object = {
                    'value': value,
                    'found': found_value
                }
                found_values.append(val_object)
                # If specified, characters can only be used once
                if remove_value:
                    words_copy = self.remove_value(
                        words_copy, found_value
                    )
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
            # Only 1 card should exist in each input
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
    for index in range(len(cards_list)):
        card = cards_list[index]
        # Stopping the loop if the user enters a comma at the end
        if card.text == '' and index == len(cards_list) - 1:
            break
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


def validate_hand(cards_list, card_number):
    """
    Checks if a poker hand entered by the user can
    produce a valid set of cards
    """
    formatted_hand = []
    # Each hand must contain at least 5 cards
    enough_cards = True
    card_len = len(cards_list)
    # All hands must have the same length once one is entered
    if card_number == 0:
        enough_cards = number_in_range('card', card_len, 5, 8)
    else:
        enough_cards = number_in_range(
            'card', card_len, card_number, card_number
        )
    if not enough_cards:
        return None
    formatted_hand = convert_hand(cards_list)
    return formatted_hand


def get_hand_input(card_number):
    """
    Requests a hand to be manually entered by the user, and returns
    an instance of Hand
    """
    player_name = get_required_input(
        'Name', 'Please enter your name: ', 12, names
    )
    names.append(player_name)
    print(f'Welcome {player_name}!\n')
    print('Please enter your poker hand, or "random" for a random hand.')
    # Keep requesting an input from the user until a valid hand is entered
    while True:
        # Telling the user the correct amount of cards they need to enter
        text = 'between 5 and 8'
        if card_number > 0:
            text = str(card_number)
        print(
            f'- Your hand must contain {text} cards, separated by a comma.'
        )
        print('- Each card must contain a rank and a suit.')
        print('- Example: "King of Hearts", "King Heart", "KH"\n')
        hand_input = get_required_input('Hand', 'Enter hand here: ')
        # Creates a random hand if the user specifies it
        if contains_word(hand_input, 'random'):
            new_hand = Hand(player_name, [])
            deck.shuffle()
            random_cards = 5
            if card_number > 0:
                random_cards = card_number
            new_hand.take_from_deck(random_cards)
            return new_hand

        # Splits the inputs into separate elements in a list
        hand_list = hand_input.split(',')
        card_objects = []
        for card_text in hand_list:
            # Removing any white space from the edge of each card input
            text_stripped = card_text.strip()
            card_object = CardInput(text_stripped)
            card_objects.append(card_object)

        cards = validate_hand(card_objects, card_number)
        if cards is not None:
            new_hand = Hand(player_name, cards)
            return new_hand


def get_required_input(
    input_type, message, max_chars=0, duplicates=[]
):
    """
    Requests an input from the user continuously until
    a valid input is given
    """
    user_input = ''
    valid = False
    while not valid:
        user_input = input(message)
        print('')
        user_input = user_input.strip()
        if user_input == '':
            print_error(f'{input_type} is blank')
            continue
        # Checking if the input length is within a limit
        if max_chars > 0 and len(user_input) > max_chars:
            print_error(
                f'{input_type} can only be {max_chars} characters'
            )
            continue
        # For inputs that must be unique
        has_duplicate = False
        for duplicate in duplicates:
            if user_input == duplicate:
                print_error(f'{input_type} already exists')
                has_duplicate = True
                continue
        if not has_duplicate:
            valid = True
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
    can affect the hand. Can have up to 3
    """
    request_message = 'Do you wish to include wildcards in your game?\n'
    request_message += '- Wild cards are cards that can take form of any\n'
    request_message += '  rank or suit to make the best possible hand.'
    if user_allows(request_message):
        while True:
            print('Please enter up to 3 wild cards, separated by a comma')
            print('- Only enter the rank of the card, i.e. 2 - Ace')
            wildcards = input('Wild Cards: ')
            wildcards = wildcards.strip()
            # Adds a gap between the input and the next print
            print('')
            if wildcards == '':
                if user_allows('No wild cards entered. Proceed anyway?'):
                    return []
                else:
                    continue
            wildcard_ranks = validate_wildcards(wildcards)
            if wildcard_ranks is not None:
                return wildcard_ranks
    else:
        return []


def validate_wildcards(wildcard_input):
    """
    Gets a list of wild cards from an input, returning the list if
    valid and printing an error if not
    """
    cards_list = wildcard_input.split(',')
    wildcard_ranks = []
    # Checking each input for a valid rank
    for index in range(len(cards_list)):
        card_text = cards_list[index]
        card_text = card_text.strip()
        # Printing an error if an empty input is detected
        if card_text == '':
            # In case the user entered a comma at the end
            if index == len(cards_list) - 1:
                break
            print_error('Blank card detected')
            return None
        card = CardInput(card_text)
        # Splitting the input into words
        rank_words = card_text.split(' ')
        ranks = card.find_values(rank_words, 'rank', True)
        if len(ranks) == 0:
            print_error(f'No ranks found in "{card_text}"')
            return None
        elif len(ranks) > 1:
            rank_names = []
            for rank in ranks:
                rank_name = get_rank_name(rank['value'])
                rank_names.append(rank_name)
            print_error(
                f'Multiple ranks found in "{card_text}"',
                rank_names
            )
            return None
        for rank in ranks:
            rank_value = rank['value']
            if rank_value not in wildcard_ranks:
                wildcard_ranks.append(rank['value'])
    # Checking if the number of wild cards is less than 3
    wild_number = len(wildcard_ranks)
    if number_in_range('wild card', wild_number, 0, 3):
        return wildcard_ranks
    return None


def get_rank_name(rank_number):
    """
    Returns the rank of a given card as a string,
    consisting of the rank's full name
    """
    # For cards greater than 10
    if rank_number > 10:
        # The 11th rank will be "Jack", which is the first
        # element [0] in CardInput.ranks
        return CardInput.ranks[rank_number - 11]
    return str(rank_number)


def get_rank_value(rank_name):
    """
    Returns the rank of the card as an integer
    """
    if rank_name in CardInput.ranks:
        return CardInput.ranks.index(rank_name) + 11
    return int(rank_name)


def get_hand_names(hands):
    """
    Returns a list of all names from a list of hands
    """
    hand_names = []
    for hand in hands:
        hand_names.append(hand.name)
    return hand_names


def get_best_hand(hands):
    """
    Returns the hand with the best value out of a
    given list of hands
    """
    best_hand = []
    for hand in hands:
        if len(best_hand) == 0:
            best_hand = [hand]
            continue
        hand_score = hand.value['score']
        best_score = best_hand[0].value['score']
        if hand_score < best_score:
            continue
        if hand_score > best_score:
            best_hand = [hand]
            continue
        # If 2 hands have the same value, the hand with the
        # greater subscore will prevail
        hand_sub = hand.value['subscore']
        best_sub = best_hand[0].value['subscore']
        comparison = compare_subscores(hand_sub, best_sub)
        if comparison != '=':
            if comparison == '>':
                best_hand = [hand]
            continue
        # If both the score and subscore match, then check
        # which has the higher ranked cards
        comparison = compare_high_cards(hand, best_hand[0])
        if comparison == '>':
            best_hand = [hand]
        elif comparison == '=':
            best_hand.append(hand)
        # We do nothing if the hand in the loop is less than the best
    return best_hand


def compare_subscores(sub1, sub2):
    """
    Compares 2 subscores and returns a string
    '<', '>' or '='
    """
    # For "of Kind" and Straight hand values
    if isinstance(sub1, int):
        return compare_numbers(sub1, sub2)
    # Two Pair and Full House hand values have
    # subscores of type list
    elif isinstance(sub1, list):
        # Only comparing the first 2 pairs, if more than 2
        for i in range(0, 2):
            comparison = compare_numbers(sub1[i], sub2[i])
            if comparison != '=':
                return comparison
    return '='


def compare_high_cards(hand1, hand2):
    """
    Compares the high cards of 2 hands and returns
    ">" if hand1 has higher cards, "<" if hand2 has
    higher cards, or "=" if they are equal
    """
    index = 0
    cards1 = hand1.combine_all_cards()
    cards2 = hand2.combine_all_cards()
    # Loops through all the cards until a difference is found,
    # or no cards are left
    while True:
        highcard1 = 0
        highcard2 = 0
        if index < len(cards1):
            highcard1 = cards1[index].rank
        if index < len(cards2):
            highcard2 = cards2[index].rank
        # If both hands went through all their cards without finding
        # a difference, then they are identical
        if highcard1 == 0 and highcard2 == 0:
            return '='
        comparison = compare_numbers(highcard1, highcard2)
        # End the function once a difference is found
        if comparison != '=':
            return comparison
        index += 1


def compare_numbers(num1, num2):
    """
    Compares 2 values and returns a string
    '<', '>' or '='
    """
    if num1 > num2:
        return '>'
    if num1 < num2:
        return '<'
    return '='


def print_hand_table(hands, card_number):
    """
    Prints all the hands along with their name and value
    in a table
    """
    # Displaying wild cards first, if any
    print_wildcards()

    # Printing the heading labels
    heading = 'Name:\t\tCards:'
    for i in range(card_number):
        if card_number > 6:
            # 6 spaces for each card, because "*10S*", the
            # longest card string, has 5 chars, plus 1 for
            # spacing. Skipping the first as "Cards:" has
            # 6 characters
            if i > 0:
                heading += '      '
        else:
            heading += '\t'
    heading += 'Value:'
    print(heading)
    for hand in hands:
        hand.set_value()
        hand.print_hand()

    # Displaying the winner for more than one hand
    print_winning_hands(hands)


def print_wildcards():
    """
    Prints a list of wild cards to the terminal,
    surrounding them with two asterices (**)
    """
    if len(deck.wildcards) > 0:
        wild_text = 'Wild cards: '
        for i in range(len(deck.wildcards)):
            wild_card_text = get_rank_name(deck.wildcards[i])
            wild_text += f'*{wild_card_text}*'
            # Commas to separate multiple wild cards
            if i < len(deck.wildcards) - 1:
                wild_text += ', '
        print(wild_text)


def print_winning_hands(hands):
    """
    Finds the winning hand (or hands) and prints
    them to the terminal
    """
    if len(hands) > 1:
        best_hand = get_best_hand(hands)
        winner = ''
        # For only 1 winner
        if len(best_hand) == 1:
            winner = best_hand[0].name
        else:
            # Building the sentence that displays each winner
            winner = 'Draw between '
            winning_names = get_hand_names(best_hand)
            winner += get_list_as_sentence(winning_names)
        print(f'Winning hand: {winner}')


def get_list_as_sentence(my_list):
    """
    Returns a list of elements as a string in a
    readable sentence, with every element separated
    by a comma and an "and" for the last one
    """
    sentence = ''
    length = len(my_list)
    for i in range(length):
        sentence += my_list[i]
        if i == length - 2:
            sentence += ' and '
        elif i < length - 2:
            sentence += ', '
    return sentence


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
    # Integers must contain the full number, in the correct order
    if word.isdigit():
        if word not in input_word:
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

    # For empty inputs
    if len(input_word) == 0:
        return None

    if word.isdigit():
        if word in input_word:
            return word
        else:
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
    return final_string


def user_allows(message):
    """
    Asks a user a yes/no question, and returns True or
    False depending on what the user entered
    """
    while True:
        print(message)
        answer = input('Your answer (Y/N): ')
        answer = answer.strip()
        print('')
        if contains_word(answer, 'Yes'):
            return True
        elif contains_word(answer, 'No'):
            return False
        else:
            print('Please enter Yes (Y) or No (N)\n')


def number_in_range(name, number, low_range, high_range):
    """
    Returns if a given number is within a certain range,
    and prints an error if it isn't
    """
    if number >= low_range and number <= high_range:
        return True
    # Building the error sentence
    error_str = ''
    if low_range == high_range:
        error_str += f'Need exactly {low_range} '
    elif number > high_range:
        error_str = f'Can only have up to {high_range} '
    else:
        error_str = f'Need at least {low_range} '
    error_str += f'{name}s. You have entered {number}'
    print_error(error_str)
    return False


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


def start_round():
    """
    Initiates a round of poker, collecting one or more
    hands and displaying the winner if more than one
    """
    # Resetting the player names and deck each round
    deck.cards = deck.get_full()
    names.clear()

    wildcards = get_wildcards()
    deck.wildcards = wildcards

    player_hands = []
    card_number = 0
    while True:
        hand_input = get_hand_input(card_number)
        player_hands.append(hand_input)
        if card_number == 0:
            card_number = len(hand_input.cards)
        print_hand_table(player_hands, card_number)
        if len(deck.cards) < card_number:
            print('\nNot enough cards for another hand!')
            break
        if not user_allows('\nDo you wish to add another hand?'):
            break
    # Congratulates the winner at the end of the round
    if len(player_hands) > 1:
        winners = get_best_hand(player_hands)
        winning_names = get_hand_names(winners)
        winner_text = 'Congratulations '
        winner_text += get_list_as_sentence(winning_names)
        winner_text += '! You won!\n'
        print(winner_text)


def main():
    """
    Initializes the game.
    """
    # Stores all the cards that haven't been taken
    global deck
    deck = Deck()
    # For storing all the player names
    global names
    names = []

    print('Welcome to Python Poker!\n')
    print('Python Poker will read one or more poker hands,')
    print('taking wild cards into consideration, and will display')
    print('the values of each hand, as well as the winner.\n')

    while True:
        start_round()
        if not user_allows('Do you want to start another round?'):
            break
    print('Thank you for using Python Poker! Goodbye!')


main()
