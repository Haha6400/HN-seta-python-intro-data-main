"""
Python basics, Problem Set, hangman.py
Name: TODO
Collaborators: TODO
Time spent: TODO
"""

# ---------------------------------------------------------------------------- #
#                                 Hangman Game                                 #
# ---------------------------------------------------------------------------- #


# -------------------------------- Helper code ------------------------------- #
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    with open(WORDLIST_FILENAME, "r") as inFile:
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# ---------------------------- end of helper code ---------------------------- #


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far, assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed, False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    
    return True
    



def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far.
    """
    guessed_word = ""
    for letter in secret_word:
        if letter in secret_word: 
            guessed_word += letter
        else:
            guessed_word += "_"
    return guessed_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not yet been guessed.
    """
    all_letters = string.ascii_lowercase
    available_letters = ""
    for letter in all_letters:
        if letter not in letters_guessed:
            available_letters += letter
    
    return available_letters


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
    letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
    about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
    partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """

    guesses_remaining = 6
    letters_guessed = []
    print("The secret word contains", len(secret_word), "letters.")
    print("You start with", guesses_remaining, "guesses.")
    while guesses_remaining > 0:
        print("You have", guesses_remaining, "guesses left")
        print("Available letters: ", get_available_letters(letters_guessed))
        print("Partially Guessed Word:", get_guessed_word(secret_word, letters_guessed))

        input_guess = input("Please enter your guess: ").lower()

        #Validate the input guess
        if len(input_guess) != 1 or input_guess not in string.ascii_lowercase:
            print("Invalid guess. Please enter another letter")
            continue
        #Check if the input guess has already been made
        if input_guess in letters_guessed:
            print("You have already guesses that letter before. Try again")
            continue

        letters_guessed.append(input_guess)

        #check if the input guess is correct
        if input_guess in secret_word:
            print("Well done!")
        else:
            print("That letter is not in the word")
            guesses_remaining -= 1
        
        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations! You guessed the word:", secret_word)
        else:
            print("Keep guessing!")
    
    if guesses_remaining == 0:
        print("Sorry, you ran out of guesses. The word was: ", secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# ---------------------------------------------------------------------------- #


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    if len(my_word) != len(other_word):
        return False
    
    for i in range(len(my_word)):
        if(my_word[i] == "_"):
            continue
        elif my_word[i] != other_word[i]:
            return False
        
    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word

    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed.
    Therefore, the hidden letter(_ ) cannot be one of the letters in the word
    that has already been revealed.

    """
    matching_word = []

    for word in wordlist:
        if len(word) != len(my_word):
            continue

        is_matching = True
        for i in range(len(my_word)):
            if my_word[i] == "*":
                continue
            elif my_word[i] != word[i]:
                is_matching = False
                break
        
        if is_matching:
            matching_word.append(word)
        
    print("Matching words: ")
    for word in matching_word:
        print(word)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
    letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
    about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
    partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
    matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # TODO: FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses_remaining = 6
    letters_guessed = []
    print("The secret word contains", len(secret_word), "letters.")
    print("You start with", guesses_remaining, "guesses.")
    while guesses_remaining > 0:
        print("You have", guesses_remaining, "guesses left")
        print("Available letters: ", get_available_letters(letters_guessed))
        print("Partially Guessed Word:", get_guessed_word(secret_word, letters_guessed))

        input_guess = input("Please enter your guess: ").lower()

        #Validate the input guess
        if len(input_guess) != 1 or input_guess not in string.ascii_lowercase:
            print("Invalid guess. Please enter another letter")
            continue

        #Check if the input guess is a hint
        if input_guess == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        #Check if the input guess has already been made
        if input_guess in letters_guessed:
            print("You have already guesses that letter before. Try again")
            continue



        letters_guessed.append(input_guess)

        #check if the input guess is correct
        if input_guess in secret_word:
            print("Well done!")
        else:
            print("That letter is not in the word")
            guesses_remaining -= 1
        
        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations! You guessed the word:", secret_word)
        else:
            print("Keep guessing!")
    
    if guesses_remaining == 0:
        print("Sorry, you ran out of guesses. The word was: ", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman(secret_word)

# ---------------------------------------------------------------------------- #

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

# secret_word = choose_word(wordlist)
# hangman_with_hints(secret_word)
