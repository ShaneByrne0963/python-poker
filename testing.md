# Manual testing of Python Poker

## Introduction

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

This section of the program only runs if the user answers Section 1 with a "Yes" input. It requests a list of wildcards that will be used in the upcoming round

![Wild card request displayed on terminal](assets/images/testing/wild-cards/terminal-display.jpg)

Rules:
- Each wild card input must contain at least 1 rank (Any number between 2 and 10, or "Jack", "Queen", "King" or "Ace")
- The wild cards should be separated by a comma
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

### Valid Inputs

**Test 1: No input**

![Response to no input](assets/images/testing/wild-cards/no-input.JPG)

- In this section, no input is actually a valid input as for this case, the program will assume the user may have changed their mind about including wild cards.

**Test 2: White space input**

![Response to white space input](assets/images/testing/wild-cards/space-input.JPG)

- A white space ("  ") input is treated the exact same as if the user entered no input at all

**Test 3: No commas separating ranks**

![User entering wild cards with no commas](assets/images/testing/wild-cards/input-no-comma.JPG)

![The result of the input](assets/images/testing/wild-cards/output-no-comma.JPG)

- Despite what the instructions suggest, commas are not necessary to enter wild cards
- However, if the user enters a list of wildcards without using commas and one of the ranks is invalid,
the program will not notify the user that there was an error and continue without using the invalid card
- Giving the user feedback on any invalid input is why separating ranks with commas is recommended

![User entering an invalid input without separating other words with commas](assets/images/testing/wild-cards/input-one-invalid.JPG)

![The result of the invalid input](assets/images/testing/wild-cards/output-one-invalid.JPG)

- Also, if multiple ranks are found in one word, without commas the program will use all ranks found

![Input that contains both "Queen" and "Ace"](assets/images/testing/wild-cards/multiple-rank-word.JPG)

![Result of this input](assets/images/testing/wild-cards/multiple-rank-word-output.JPG)

- I decided to keep this feature for users more familiar with the program, who are less likely to make mistakes
- This feature reduces the amount of characters needed to type for this input

**Test 4: Trying all valid ranks**

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

**Test 5: Misspelling worded ranks**

![User misspells "Jack", "Queen" and "King"](assets/images/testing/wild-cards/input-misspelled.JPG)

![Program understands user's intended ranks](assets/images/testing/wild-cards/output-misspelled.JPG)

- This section uses the same function as the word interpreter described in Section 1.
- Above, all first letters of the misspelled words are the same as the intended ranks,
and 100% of the characters exist in these ranks, so they are a match

**Test 6: Comma at end of input**

![User ending the input with a comma](assets/images/testing/wild-cards/input-comma-end.JPG)

- It is possible that the user could enter a comma after every rank, including the last one
- If there is no text (or is only white space) after the last comma,
the program does not consider what is after the comma a blank card, which would make the input invalid


## Section 3: Proceeding Without Wildcards

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

- After successfully moving from the wild card section, the user will then be asked to enter their name
- Each hand has a player name, in order to tell the user which player is the winner

![Requesting the user for a name]

Rules:
- The name must be 12 characters or under
- If more than one player is entered, each name must be unique (Different cases are acceptable)

### Invalid Inputs

**Test 1: No input**

**Test 2: White space input**


## Section 5: Hand Request

### Invalid Inputs

**Test 1: No input**

**Test 2: White space input**


## Section 6: Displaying the Hands


## Section 7: Adding Another Hand


## Section 8: Starting Another Round