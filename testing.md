# Manual testing of Python Poker

## Introduction

<hr>

There are several sections of Python Poker that require user input, each having their own set of rules for the data to be valid

For each input, the following will be tested:
- No input will be given
- An input only containing white space (" ") will be given
- Each rule will be broken, depending on the section
- Every valid input will also be entered to ensure they work

For the purposes of testing Python Poker, the following will be defined as:
- *Invalid input*: Any input that asks the user to re-enter their input, correcting their mistakes
- *Valid input*: Any input that triggers the program to move to a different section

## Section 1: Yes or No Questions

<hr>

Upon starting the program, the user is first asked a yes or no question on whether they want to include wild cards in their round.

![Yes/no question displayed on terminal](assets/images/testing/yes-or-no/terminal-display.JPG)

Note: All input requests that are accompanied by the text "Your Answer (Y/N): " use the same function `user_allows()`, which always returns a boolean value (Yes = True, No = False) and takes in no parameters that directly affect the algorithm. What this means is that these input requests use the exact same function to get a yes or no answer from the user with zero differences, so it is unnecessary to document every test case on all of them

Rules:
- 75% of the characters of the input must contain "Yes" or "No"
- The input must start with either "Y" or "N"

### Invalid Inputs

**Test 1: No input**

![Yes/no question's response to no input](assets/images/testing/yes-or-no/no-input.JPG)

**Test 2: White space input**

![Yes/no question's response to white space input](assets/images/testing/yes-or-no/space-input.JPG)

**Test 3: Input that program does not expect**

![An input not expected by the yes/no question](assets/images/testing/yes-or-no/unknown-input.JPG)

**Test 4: Different word that contains an answer**

![An input similar to yes](assets/images/testing/yes-or-no/similar-input.JPG)

- "Yesterday" contains "Yes", which is a valid input
- However, at least 75% of the characters in the input must exist in the word (In this case, "Yes")
- Only 33% of the input contains "Yes", so the word is invalid
- The input would also be invalid if the user entered "Yeah" (50%) or "Nope" (Compared to "No": also 50%)

**Test 5: First letters do not match**

!["Yes" is jumbled in an unrecognisable manner](assets/images/testing/yes-or-no/unordered-input.JPG)

- "eYs" has a 100% letter match with "Yes"
- However, I decided that when it comes to spelling mistakes, it is very uncommon for people to misspell the first letter
- Therefore, it is safe to assume that if the user enters a different first letter, they mean something else
- Non matching first letters will result in the input failing to match the words

**Test 6: Repeating characters that matches an answer**

![Input contains the answer but is too long](assets/images/testing/yes-or-no/input-repeating-letters.JPG)

- At first glance, "Yessss" looks like a valid input since 100% of the letters in the input are in "Yes"
- However, each letter in the answer can only be matched with once, so after the "s" in "Yes" is found, any "s" after will not count
- This brings the matching letters down to 50% in this case, which is not considered a word match

### Valid Inputs

**Test 1: User enters "Yes"**

![User enters "Yes"](assets/images/testing/yes-or-no/input-yes.JPG)

- When the user enters "Yes", the program will proceed to request the ranks of wild cards the user wishes to have

**Test 2: User enters "No"**

![User enters "No"](assets/images/testing/yes-or-no/input-no.JPG)

- When the user enters "No", the program will skip the wild card section and move to entering the first player's name

**Test 3: User enters part of answer**

![User enters "y"](assets/images/testing/yes-or-no/input-y.JPG)

- "y" is a valid input because the first letter of the input (In this case, the only letter) is the same as the first letter of the word,
and 100% of the input is in "Yes"
- Also note the word comparison is not case sensitive
- This also works for the "No" answer ("n")

![User enters "n"](assets/images/testing/yes-or-no/input-n.JPG)


## Section 2: Wild Cards

<hr>

This section of the program only runs if the user answers Section 1 with a "Yes" input. It requests a list of wildcards that will be used in the upcoming round

![Wild card request displayed on terminal](assets/images/testing/wild-cards/terminal-display.jpg)

Rules:
- Each wild card input must contain at least 1 rank (Any number between 2 and 10, or "Jack", "Queen", "King" or "Ace")
- The wild cards must be separated by a comma
- No more than 3 wild cards can be entered

### Invalid Inputs

**Test 1: No rank in any wild card**

![User enters invalid rank](assets/images/testing/wild-cards/invalid-rank-input.jpg)

- The user will be told that the first invalid card rank contains no ranks
- Note that "Pick" and "Sticks" contain the letter "k", which could be attributed to "King".
- However, "k" is not the first letter of these words, so the program correctly identifies them as not this rank

**Test 2: More than 3 wild cards**

![4 wild cards entered](assets/images/testing/wild-cards/too-many-wildcards.JPG)

- The user will be reminded about how many wild cards they can enter, and told how many cards they actually entered

**Test 3: Blank wild card**

![Empty space for one wild card](assets/images/testing/wild-cards/blank-input.JPG)

**Test 4: Multiple ranks in one wild card**

!["Jack" and "Queen" both entered as one wild card](assets/images/testing/wild-cards/multiple-rank-input.JPG)

- If more than one rank is found in an input, then each rank found will be shown to the user, allowing them to correct their mistake easier

**Test 5: No commas separating the wild cards**

![3 wild cards not separated by a comma](assets/images/testing/wild-cards/no-commas.JPG)

- If there are no commas between the ranks, it will treat the input as only one card and produce an error
- The user is told what cards were found in the one input

![3 wild cards in onw word](assets/images/testing/wild-cards/no-spaces.JPG)

- The same is true if the user also didn't enter spaces either

### Valid Inputs

**Test 1: No input**

![Response to no input](assets/images/testing/wild-cards/no-input.JPG)

- In this section, no input is actually a valid input as for this case, the program will assume the user may have changed their mind about including wild cards.

**Test 2: White space input**

![Response to white space input](assets/images/testing/wild-cards/space-input.JPG)

- A white space ("  ") input is treated the exact same as if the user entered no input at all

**Test 3: Trying all valid ranks**

- Note: All possible amounts of wild cards (1 - 3 per round) are also being tested here

2:

![Rank 2 entered](assets/images/testing/wild-cards/valid-ranks/input-2.JPG)
![Rank 2 returned](assets/images/testing/wild-cards/valid-ranks/output-2.JPG)

3 and 4:

![Ranks 3 and 4 entered](assets/images/testing/wild-cards/valid-ranks/input-3-4.JPG)
![Ranks 3 and 4 returned](assets/images/testing/wild-cards/valid-ranks/output-3-4.JPG)

5, 6 and 7:

![Ranks 5, 6 and 7 entered](assets/images/testing/wild-cards/valid-ranks/input-5-6-7.JPG)
![Ranks 5, 6 and 7 returned](assets/images/testing/wild-cards/valid-ranks/output-5-6-7.JPG)

8, 9 and 10:

![Ranks 8, 9 and 10 entered](assets/images/testing/wild-cards/valid-ranks/input-8-9-10.JPG)
![Ranks 8, 9 and 10 returned](assets/images/testing/wild-cards/valid-ranks/output-8-9-10.JPG)

Jack, Queen and King:

![Ranks Jack, Queen and King entered](assets/images/testing/wild-cards/valid-ranks/input-j-q-k.JPG)
![Ranks Jack, Queen and King returned](assets/images/testing/wild-cards/valid-ranks/output-j-q-k.JPG)

Ace:

![Rank Ace entered](assets/images/testing/wild-cards/valid-ranks/input-ace.JPG)
![Rank Ace returned](assets/images/testing/wild-cards/valid-ranks/output-ace.JPG)

**Test 4: Misspelling worded ranks**

![User misspells "Jack", "Queen" and "King"](assets/images/testing/wild-cards/input-misspelled.JPG)

![Program understands user's intended ranks](assets/images/testing/wild-cards/output-misspelled.JPG)

- This section uses the same function as the word interpreter described in Section 1.
- Above, all first letters of the misspelled words are the same as the intended ranks,
and 100% of the characters exist in these ranks, so they are a match

**Test 5: Comma at end of input**

![User ending the input with a comma](assets/images/testing/wild-cards/input-comma-end.JPG)

- It is possible that the user could enter a comma after every rank, including the last one
- If there is no text (or is only white space) after the last comma,
the program does not consider what is after the comma a blank card, which would make the input invalid


## Section 3: Proceeding Without Wildcards

<hr>

- If the user doesn't enter any wild cards when prompted, the program will ask the user if they want to continue without wild cards
- This is a yes/no question that uses the function `user_allows()`.
To see all invalid inputs, see "Section 1: Yes or No Questions"
- Here, we will only be testing the valid ranks (True/False) to see if they result in moving to the intended sections

![Asking the user to proceed without wild cards](assets/images/testing/wild-cards/no-input.JPG)

**Test 1: User enters "Yes"**

![Answering "Yes" to the question](assets/images/testing/yes-or-no/no-wildcards/input-yes.JPG)

- If "Yes", the program will skip the wild card section as if the user originally entered "No" for wild cards

**Test 2: User enters "No"**

![Answering "No" to the question](assets/images/testing/yes-or-no/no-wildcards/input-no.JPG)

- If "No", the program will allow the user to enter wild cards once again


## Section 4: Name Request

<hr>

- After successfully moving from the wild card section, the user will then be asked to enter their name
- Each hand has a player name, in order to tell the user which player is the winner

![Requesting the user for a name]

Rules:
- The name must be 12 characters or under
- If more than one player is entered, each name must be unique (Different cases are acceptable)

### Invalid Inputs

**Test 1: No input**

![Response to no input](assets/images/testing/player-name/no-input.JPG)

**Test 2: White space input**

![Response to white space input](assets/images/testing/player-name/white-space-input.JPG)

**Test 3: More than 12 characters**

![13 character name entered is invalid](assets/images/testing/player-name/too-many-letters.JPG)

**Test 4: Using a name already taken**

![User entering a name that is already taken](assets/images/testing/player-name/taken-input.JPG)

### Valid Inputs

**Test 1: Entering a name that meets all requirements**

![User enters a valid name](assets/images/readme/hand-prompt.jpg)


## Section 5: Hand Request with No Prior Players

<hr>

- Once a valid name is entered, the program will move on to getting that player's cards

Rules:
- The hand must contain between 5 and 8 cards
- Each card must contain a rank and a suit
- Each card must be separated by a comma (unlike with wild cards where it is only recommended)
- Only one rank and suit should be entered
- No card should exist more than once in the hand

### Invalid Inputs

**Test 1: No input**

![Response to no input](assets/images/testing/hand-no-players/no-input.JPG)

**Test 2: White space input**

![Response to white space input](assets/images/testing/hand-no-players/white-space-input.JPG)

**Test 3: Entering a normal string**

![Response to a normal string](assets/images/testing/hand-no-players/single-input.JPG)

- The program treats a simple string as a single input, and tells the user they need more cards

**Test 4: Entering too many cards**

![Too many cards entered](assets/images/testing/hand-no-players/too-many-inputs.JPG)

- The program evaluates how many inputs have been entered before checking if any are valid.
This is why there is no error about only entering numbers
- Also note the error message sentence changes depending on if the user enters not enough or too many cards

**Test 5: Empty string for card**

![One card is left blank](assets/images/testing/hand-no-players/blank-card-input.JPG)

**Test 6: One invalid card entered**

!["Other Card" is not a valid card](assets/images/testing/hand-no-players/invalid-card-input.JPG)

- The program first checks for ranks in a card, which is why it does not mention that there are also no suits present

**Test 7: No rank detected in a card**

![No ranks detected in "S"](assets/images/testing/hand-no-players/missing-rank-input.JPG)

- The same result occurs for an invalid rank as if the card is completely invalid, as seen in Test 6 above

**Test 8: No suit detected in a card**

![No suits detected in "Jack"](assets/images/testing/hand-no-players/missing-suit-input.JPG)

- The same error message is shown as if there were no ranks found, except "rank" is changed to "suit"

**Test 9: Multiple different cards found in one input**

![K-A-S-C contains several different cards](assets/images/testing/hand-no-players/multiple-card-input.JPG)

- If multiple cards are found in a single input, every card found will be shown in a list.
- This makes it easier for the user to find where their mistake was

**Test 10: No commas to divide the cards**

![Cards have no commas to divide them](assets/images/testing/hand-no-players/no-comma-input.JPG)

- Unlike with the wild card section, cards need to have a comma between them because
there is 2 different types of information to get from each input: the rank and the suit
- If commas were not present here, the program could mix up the different ranks and suits to get cards the user did not intend to enter
- If commas aren't used, the program will treat the input as one card

**Test 11: A card in the hand exists twice**

![4 of Diamonds is entered twice](assets/images/testing/hand-no-players/duplicate-card-input.JPG)

- Only one of each card exists in the deck, so the user cannot have more than one

### Valid Inputs

**Test 1: Entering a valid hand**

![The user enters a valid hand](assets/images/testing/hand-no-players/valid-input.JPG)

- When a valid input is entered, the program displays all of the hands entered in a table,
and asks if the user wants to add another hand

**Test 2: All valid ranks and suits**

- For this test, we will also be testing every suit, as well as every hand size

Ranks 2 to 6, and hand size of 5

![Ranks 2 to 6, and hand size of 5](assets/images/testing/hand-no-players/ranks-2-6.JPG)

Ranks 7 to Queen, and hand size of 6

![Ranks 7 to Queen, and hand size of 6](assets/images/testing/hand-no-players/ranks-7-q.JPG)

Ranks King to 6, and hand size of 7

![Ranks King to 6, and hand size of 7](assets/images/testing/hand-no-players/ranks-k-6.JPG)

Ranks 7 to Ace, and hand size of 8

![Ranks 7 to Ace, and hand size of 8](assets/images/testing/hand-no-players/ranks-7-a.JPG)

**Test 2: Misspelling ranks and suits**

![All inputs are misspelled](assets/images/testing/hand-no-players/input-misspell.JPG)

- This input request uses the same word interpreter as the one mentioned in the previous sections
- In the image above, Each rank and suit contains at least 75% of the word it is trying to represent
- If there are no spaces, the rank or suit will then be searched for in the string
- The rank and suit that takes up the most amount of characters in the input will be chosen

**Test 3: Comma at end of hand**

![The user ended the input with a comma](assets/images/testing/hand-no-players/input-comma-end.JPG)

- If a comma is entered at the end, what is after that comma won't be treated like a blank card

**Test 4: "Random"**

!["Random" entered](assets/images/testing/hand-no-players/input-random.JPG)

- If the user enters "random", they will be dealt a random hand

**Test 5: "Random" misspelled**

!["Random" is spelled incorrectly](assets/images/testing/hand-no-players/input-random-misspell.JPG)

- The word interpreter will still recognise "rnadm" as "random", and deal a random hand as normal
- This also works if the user simply enters the letter "r"


## Section 6: Displaying the Hands

<hr>

- After the user successfully enters a hand, a table will be displayed.
This table will show all player hands, any wild cards, and the winner if there are multiple players
- The value of a hand will be determined by the best 5 cards in that hand, i.e. which 5 cards can make the best possible hand
- This is not a direct user input, so there are no invalid test cases, but it heavily depends on the user's previous inputs, so they will be tested

![The table showing one player](assets/images/testing/hand-no-players/valid-input.JPG)

**Test 1: Wild cards**

!["Queen" and "Ace" displaying as wild cards above table](assets/images/testing/display-hand/wild-cards.JPG)

- If any wild cards are present in the game, they will be displayed on top of the grid
- Wild cards are wrapped in asterices (*), so the wild cards displayed over the table are also wapped in this way to make this apparent to the user

**Test 2: Multiple players**

![More than 1 player in the table](assets/images/testing/display-hand/multiple-hands.JPG)

- The winner is displayed underneath the table of hands

**Test 3: More than 5 cards per hand**

![The table showing a hand that has 8 cards](assets/images/testing/display-hand/table-8-cards.JPG)

- The table expands horizontally when there are more cards

**Test 4: Getting every possible hand value**

![Hands ranging from High Card to Flush](assets/images/testing/display-hand/lower-half-values.JPG)

![Hands ranging from Full House to Royal Flush](assets/images/testing/display-hand/upper-half-values.JPG)

- Note: As I added these values in, each time the winner was updated to the newest player, which works as expected as their values got higher

**Test 5: Getting every possible hand value with wild cards**

![Hands with wild cards from High Card to Flush](assets/images/testing/display-hand/lower-half-wild.JPG)

![Hands with wild cards from Full House to 5 of a Kind](assets/images/testing/display-hand/upper-half-wild.JPG)

- Note: Two Pair is impossible to make with wild cards as 3 of a Kind will always take precedence
- Also 5 of a Kind is only possible with wild cards

**Test 6: All the cards in a hand are wild**

![Every card is wild](assets/images/testing/display-hand/all-wild.JPG)

- The program will assign a hand with all wild cards the value of 5 aces, which is unbeatable

**Test 7: Not enough cards to add another hand**

![The round ends when the deck runs out of cards](assets/images/testing/display-hand/no-more-cards.JPG)

- When there are not enough cards to support another player, the winner will be congratulated and the round will end, moving to Section 10


## Section 7: Displaying the Winner

<hr>

- This could be the considered the second part of Displaying the Table. It isn't an input request but it highly depends on what the user enters
- From testing in Section 6, I can confirm that each value is ranked as intended, with "High Card" being the lowest of value and "5 of a Kind" being the highest

**Test 1: Pairs of the same value**

The following rules apply for any value consisting of groups of cards:
- Pair
- Two Pair
- 3 of a Kind
- Full House
- 4 of a Kind
- 5 of a Kind

![Comparing hands that both have Pairs](assets/images/testing/display-winner/pairs-same-value.JPG)

- If the hand value involves pairs of ranks, then the rank of the pairs of the hands will be compared.
- In the image above, player 2 has a pair of 6's, whereas player 1 only has a pair of 4's, so player 2 wins

![Two Pair with both hands having the same ranking high pair](assets/images/testing/display-winner/two-pair-same-value.JPG)

- With Two Pair, the higher ranking pair will be compared first, and if they match then the other pair will be compared

![Comparing 2 Full Houses](assets/images/testing/display-winner/full-house-same-value.JPG)

- With Full House, the 3 of a kind will be compared first, then the pair

**Test 2: Straights of the same value**

The following rules apply to:
- Straight
- Straight Flush
- Royal Flush

![Comparing hands that both have Straights](assets/images/testing/display-winner/straight-same-value.JPG)

- Player 2 has a higher ranking straight, so they win
- If more than 5 cards in the hand and all ranks in the straight are the same, then the highest card outside of the straight will be evaluated

![Checking the other cards if more than 5](assets/images/testing/display-winner/straight-same-rank.JPG)

**Test 3: Comparing Flush Hands**

![Comparing 2 hands that have a Flush value](assets/images/testing/display-winner/flush-same-value.JPG)

- The player with the highest card in their flush is the winner.
- If the highest cards are the same, the hand will move down the ranks until a difference is found

**Test 4: Comparing high cards**

![Both hands have no value](assets/images/testing/display-winner/high-card-same-value.JPG)

- If both hands have only high cards, then the player with the highest card will be the winner
- If the highest cards are the same, then the second highest card will be compared and so on

![The lowest cards are evaluated because the high cards are the same](assets/images/testing/display-winner/high-card-same-ranks.JPG)

- Here, all the card ranks are the same except player 2 has a 4 instead of a 2, so player 2 is the winner
- This evaluation also takes place if pair values (mentioned in Test 1) are of the same rank

![Matching Pairs will have their high cards compared](assets/images/testing/display-winner/pairs-same-rank.JPG)

**Test 5: Draws**

![Exact same hands that have a Pair value](assets/images/testing/display-winner/pairs-draw.JPG)

![Exact same hands that have a Straight Flush value](assets/images/testing/display-winner/straight-draw.JPG)

![Exact same hands that have a Flush value](assets/images/testing/display-winner/flush-draw.JPG)

- The examples above contain hands that are exact copies of each other
- In situations like these, the program simply declares both hands winners


## Section 8: Adding Another Hand

<hr>

- Once the table has been displayed, the user will be asked if they want to enter another hand into the table
- This is a yes/no question that uses the function `user_allows()`.
To see all invalid inputs, see "Section 1: Yes or No Questions"
- Here, we will only be testing the valid ranks (True/False) to see if they result in moving to the intended sections

![Asking the user if they want another hand](assets/images/testing/new-hand/terminal-display.JPG)

**Test 1: User answers "Yes"**

![User responds with "Yes"](assets/images/testing/new-hand/round-continue.JPG)

- If the user answers "Yes", the program will return to Section 4 (name request),
and start the process of getting a new hand from the user over again

**Test 2: User answers "No"**

![User responds with "No"](assets/images/testing/new-hand/round-end.JPG)

- If the user answers "No", the round will end and the program will move to Section 10 below
- If multiple hands are entered, the winner will be congratulated

![Congratulating the winner](assets/images/testing/new-hand/round-end-winner.JPG)

- If multiple winners exist, then all of them will be congratulated

![Congratulating all winners](assets/images/testing/new-hand/multiple-winners.JPG)


## Section 9: Hand Request with Prior Players

<hr>

- This is an extension of Section 5 (Hand Request without Prior Players), so we will only document the added rules.
See Section 5 for the rest of the test cases

Added rules:
- The number of cards must be the same as the previous hand (instead of 5 - 8 cards)
- A card that exists in another player's hand cannot be entered in this hand

![Updated text with multiple players](assets/images/testing/hand-with-players/terminal-display.JPG)

### Invalid Inputs

**Test 1: Different card amount**

![User enters 5 cards instead of 7](assets/images/testing/hand-with-players/unmatching-number-input.JPG)

- Error message is updated to say exactly how many cards the user needs

**Test 2: Card existing somewhere else**

![Another player has the 6 of Clubs](assets/images/testing/hand-with-players/duplicate-card-input.JPG)

- The program will treat this duplicate as if the user entered the same card twice

### Valid Inputs

**Test 1: "Random"**

![User enters "random"](assets/images/testing/hand-with-players/input-random.JPG)

- If the user enters "random", they will be dealt the same number of cards as the previous hand


## Section 10: Starting Another Round

<hr>

- Once a round has ended, the user will be asked if they want to start another
- This is a yes/no question that uses the function `user_allows()`.
To see all invalid inputs, see "Section 1: Yes or No Questions"
- Here, we will only be testing the valid ranks (True/False) to see if they result in moving to the intended sections

![Asking the user if they want another hand](assets/images/testing/new-round/terminal-display.JPG)

**Test 1: User answers "Yes"**

![User responds with "Yes"](assets/images/testing/new-round/input-yes.JPG)

- If the user answers "Yes", the program will restart and begin again at Section 1,
where they will be asked if they want wild cards in their new round
- All hands and wild cards from the previous round are erased

**Test 2: User answers "No"**

![User responds with "No"](assets/images/testing/new-round/input-no.JPG)

- If the user answers "No", the program will terminate with a goodbye message