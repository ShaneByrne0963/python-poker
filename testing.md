# Manual testing of Python Poker

## Introduction

There are several sections of Python Poker that require user input, each having their own set of rules for the data to be valid

For each input, the following will be tested:
- No input will be given
- An input only containing white space (" ") will be given
- Each rule will be broken, depending on the section
- Every valid input will also be entered to ensure they work

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

- Note that "Pick" and "Sticks" contain the letter "k", which could be attributed to "King".
- However, "k" is not the first letter of these words, so the program correctly identifies them as not this rank

### Valid Inputs

**Test 1: No input**

![Response to no input](assets/images/testing/wild-cards/no-input.JPG)

- In this section, no input is actually a valid input as for this case, the program will assume the user may have changed their mind about including wild cards.

**Test 2: White space input**


## Section 3: Proceeding Without Wildcards


## Section 4: Name Request

### Invalid Inputs

**Test 1: No input**

**Test 2: White space input**


## Section 5: Hand Request

### Invalid Inputs

**Test 1: No input**

**Test 2: White space input**


## Section 6: Adding another hand


## Section 7: Starting another round