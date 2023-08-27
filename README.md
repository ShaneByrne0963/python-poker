# Python Poker

## What is it?

Python Poker is a command-line program that requests a set of poker hands from the user and calculates the value of each hand ([See full list of hand values](https://en.wikipedia.org/wiki/List_of_poker_hands)).

If more than one hand is given, the winner will be displayed after every hand input.

This program is designed to help players that aren't too familiar with the rules of poker learn how to read their hand, as well as remove any uncertainty in determining the winner of a poker game.

This program has been deplyed to Heroku and can be found [here](https://python-poker-272a987b7d1f.herokuapp.com/).

![Python Poker displayed on multiple screens](./assets/images/readme/site-display.jpg)

## Features

### Content

- Python Poker can read hands of 5 to 8 cards, using the best 5 cards out of the hand

![The user is requested to enter their hand](assets/images/readme/hand-input.jpg)

- Up to 3 wild cards, which are special cards that can take form of any rank or suit, can be included and specified by the user
- Wild cards consist of card ranks that already exist in the deck, i.e. 2 - Ace, and will replace these card ranks for the round
- These are commonly used in poker games, and can be tricky for new players to decide what type of card is best used in place of them, so they were included to inform the user the best hand they can make with them

![The user is requested to enter wild cards](assets/images/readme/wild-cards.jpg)

- The user can add as many players as they like, as long as there are enough cards in the deck to accomodate them
- The winner will be determined each time a new hand is entered. If 2 players have the same hand value, the player with the highest ranking cards will win

![Multiple players hands displayed in a table](assets/images/readme/multiple-players.jpg)

- Once the round has concluded, the program will give the option to start an entirely new round, and will continue doing so until the user ends the program

![The option to start a new round](assets/images/readme/multiple-rounds.JPG)

### User Interface

- **Overview**
    - All bodies of text instructing the user on how to navigate through the program are kept as short as possible to prevent overwhelming the user with information
    - Sections of text are separated by a blank line to improve readibility
- **Wild Cards**
    - The user is first asked if their current round of poker includes wild cards. This is a simple yes/no question, which is clearly stated beside the answer input
    - Wild cards are requested before any player hands because all hands share the same wild cards
- ![The introduction to Python Poker](assets/images/readme/introduction.jpg)
    - If the user responds with an answer that does not resemble "Yes" or "No", a message that explains this error will appear and the user will be asked again, until a yes/no answer is detected
- ![Yes or no answer validation](assets/images/readme/yes-or-no.jpg)
    - If the user answers with no, then the wild cards section will be skipped and the program will move on to the next section
    - If answered with yes, the user will be asked to enter their wild cards, requesting each card to be separated by a comma
    - If the user does not follow the instructions, or makes a mistake, the user will be notified of the issue and will be asked to enter their input again
- ![An error is displayed for invalid inputs](assets/images/readme/wild-card-error.JPG)
    - If the user does not enter any values, they will be asked if they want to proceed without wild cards
    - This is done in case the user changed their mind about including wild cards in their game after saying yes
- ![User can continue without wild cards if none entered](assets/images/readme/no-wild-cards.jpg)
- **Getting the User's Hand**
    - Upon receiving the list of wild cards from the user (if any), the program will move on to request the poker hands
    - Each hand requires the name of the player with that hand, so the name of the winner can be displayed for each entry
- ![Requesting a name from the user](assets/images/readme/player-name.jpg)
    - Names can be up to 12 characters, and cannot exist more than once
- ![Names cannot exist more than once](assets/images/readme/existing-name.jpg)
    - After a valid name has been entered, this new player will be welcomed and asked to enter the cards in their hand
    - The program clearly states the hand must contain between 5 and 8 cards, each being separated by a comma, and must contain a rank and a suit
- ![Prompting the user for a list of cards](assets/images/readme/hand-prompt.jpg)
    - Once a hand has been entered, all future hands must have the same amount of cards as the first hand. This will be updated in the instructions
- ![Instructions with updated number of cards](assets/images/readme/static-card-number.JPG)
- **Reading the User's Input**
    - Once the user enters their list of cards, each card will be checked for a rank and a suit.
    - The characters of the input are compared to the characters of each rank and suit. If at least 75% the input's characters also exist in the rank or suit it is evaluating, then the program assumes the user meant to enter that rank/suit. However, the first character has to be the same.
    - This feature allows the text input to be more forgiving to spelling mistakes, and makes the program much easier to use for people with dyslexia
- ![Spelling mistakes are considered when evaluating the cards](assets/images/readme/spelling-mistakes.JPG)
    - If the text input consists of only one word, the characters of the rank and suit will be searched for through the input, attempting to find the best matching rank and suit
- ![Single worded inputs are taken into consideration](assets/images/readme/one-word-input.jpg)
    - This type of word evaluation is done with every input request that is looking for a word, which greatly improves the usability throughout the program
- **Displaying the Hands**
    - Once a valid hand has been entered, a table containing all of the entered hands will be displayed
    - If more than one hand exists, the winner will be added under the table
    - Wild cards are highlighted in asterices (*). To remind the user these cards are wild, the list of wild cards stated above the table is also highlighted in this way
    - The table is laid out in a way that can display a lot of information in an easy to read manner, without requiring the user to scroll through the terminal
- ![A table containing all of the entered hands](assets/images/readme/hand-table.JPG)

### Future Features

- A communal set of cards that are used by all players, for example, the "Flop", "Turn" and "River" in Texas Hold'em
- Joker cards that can be added in the wild cards section
- The option for the user to see every rank and suit to help very new poker players enter their hand
- An explanation as to why a hand has a certain value, and the percentage chance to get such a hand
- An in-depth explanation for why a particular player won

## Data Model

## Testing

### Bugs

### Manual Testing

### Validator Testing

### Unfixed Bugs

## Deployment and Local Development

### Deploy on Heroku

### Cloning Repositories

### Forking Repositories

## Credits