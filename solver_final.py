"""
The Final Solver
This solver looks at what letters are in what indexes in the remaining word list to decide its next word

Takes an optional command line argument "-g" as the guess
The guess must be a valid five letter word
If no guess is given it will choose a random word with no repeat characters
"""

# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from words import solution_words, accepted_words
import argparse

# initiate the word list and randomly choose a guess word
word_list = solution_words + accepted_words
def remove_repeat_letter_words(word_list):
    return([x for x in word_list if len(set(x)) == len(x)])
word_list_no_repeats = remove_repeat_letter_words(word_list)
random_word = random.choice(word_list_no_repeats)

# initiate word count to track
previous_word_count = None
current_word_count = len(word_list)

# use the arg parser to overwrite the guess if an initial word is given
parser = argparse.ArgumentParser(description='Wordle Solver')
parser.add_argument('-g', '--guess', default=random_word)
args = parser.parse_args()
guess = args.guess


# filter the remaining words using the feedback
def filter_word_list(word_list, list_dict):
    """
    use the dictionary of letters to filter the word dict
    """
    # filter out words that have the excluded letter
    for l in set(list_dict["wrong_letter"]):
        word_list_without_letters = [w for w in word_list if l not in w]
        word_list = word_list_without_letters

    # filter when letter is in wrong place
    for l_tuple in list_dict["correct_letter"]:

        word_list_with_letters = [w for w in word_list if l_tuple[0] in w and l_tuple[0] != w[l_tuple[1]] ]
        word_list = word_list_with_letters

    # filter for words with correct letters in correct spot
    for l_tuple in list_dict["correct_spot"]:
        word_list_correct_spot = [w for w in word_list if l_tuple[0] == w[l_tuple[1]] ]
        word_list = word_list_correct_spot

    return(word_list)

# a function used to rank the remaining words
def rank_words(word_list):
    """
    recieves a list of remaining words
    Returns a list of tuples with each word and its score
    The score is determined by the count of matcing letters in the same place in other remaining words
    """
    word_score_list = []
    for w1 in word_list:
        letter_placement_list = [0,0,0,0,0]
        for w2 in word_list:
            if w1 != w2:
                for ix in range(5):
                    if w1[ix] == w2[ix]:
                        letter_placement_list[ix] += 1
        word_score_list.append((sum(letter_placement_list), w1))

    return(sorted(word_score_list))


# function used for selenium 
def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot.children', element)
    return shadow_root

# function to type the word using selenium
def type_word(guess, keyboard):
    # loop through each letter in the word and type it on the keyboard element
    for l in guess:
        # keyboard.find_element_by_xpath(f"//button[@data-key='{l}']").click()
        keyboard.find_element(By.XPATH, f"//button[@data-key='{l}']").click()

    # press enter and wait
    # keyboard.find_element_by_xpath(f"//button[@data-key='↵']").click()
    keyboard.find_element(By.XPATH, f"//button[@data-key='↵']").click()

def check_guess(letters):
    """
    takes in a selenium object row of letters
    returns a dictionary with:
    - a list of letters (and their position) in the correct spot
    - a list of letters (and their position) in the wrong spot 
    - a list of letters known not to be in the word
    - the number of correct letters and locations found
    """
    correct_count = 0
    letters_in_word = []
    correct_location_tuples = []
    wrong_location_tuples = []
    letters_not_in_word_tuple = []
    for i, l in enumerate(letters):

        state = l.get_attribute('evaluation')
        letter_text = l.text.lower()
        

        if state == "absent":
            if l not in letters_in_word:
                letters_not_in_word_tuple.append((letter_text, i))


        elif state == "present":
            letters_in_word.append(letter_text)
            wrong_location_tuples.append((letter_text,i))

        else:
            letters_in_word.append(letter_text)
            correct_location_tuples.append((letter_text,i))
            correct_count += 1
        

    letters_not_in_word = [x[0] for x in letters_not_in_word_tuple if x[0] not in letters_in_word]
    wrong_location_tuples += [x for x in letters_not_in_word_tuple if x[0] in letters_in_word]


    list_dict = {
        "correct_spot" : correct_location_tuples,
        "correct_letter": wrong_location_tuples,
        "wrong_letter": letters_not_in_word,
        "correct_count": correct_count

    }

    return(list_dict)

if __name__ == "__main__":
    # create webdriver object
    driver = webdriver.Firefox()
    
    # go to wordle url
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    
    # access game app element
    game_app = driver.find_elements(By.TAG_NAME, "game-app")[0]
    shadow_elements = expand_shadow_element(game_app)
    game = shadow_elements[1].find_element(By.ID, "game")
    time.sleep(1)
    # click to make initial pop up go away
    game.click()
    time.sleep(3)

    # initialize "found word" flag to false
    found_word = False
    print(f"First Guess: {guess}")
    print("\n")
    for guess_num in range(6):

        keyboard = game.find_elements(By.TAG_NAME, "game-keyboard")[0]
        keyboard_shadow_elements = expand_shadow_element(keyboard)[1]

        # type in guess and wait
        type_word(guess, keyboard_shadow_elements)
        time.sleep(3)

        # access the game row and check the answer
        game_row = game.find_elements(By.TAG_NAME, "game-row")[guess_num]
        row_shadow_elements = expand_shadow_element(game_row)
        letters = row_shadow_elements[1].find_elements(By.TAG_NAME, "game-tile")
        list_dict = check_guess(letters)

        # if all 5 letters are correct then return
        if list_dict["correct_count"] == 5:
            found_word = True
            break

        # otherwise use the current word list and the dictionary to filter the list more
        filtered_list = filter_word_list(word_list, list_dict)   
        # set the filtered list as our new word list
        word_list = filtered_list

        previous_word_count = current_word_count
        current_word_count = len(word_list)

        print(f"{previous_word_count - current_word_count} words were eliminated")
        print(f"There are {current_word_count} words left")
        print("\n")

        # remove words with repeat letters so we can eliminate more options
        if len(filtered_list) > 10:
            no_repeats = remove_repeat_letter_words(filtered_list)
            if len(no_repeats) > 0:
                filtered_list = no_repeats

        # rank the words left and designate the next guess
        filtered_tuple = rank_words(filtered_list)
        guess_tuple = filtered_tuple[-1]
        score = guess_tuple[0]
        guess = guess_tuple[1]
        print(f"next guess: {guess}")
        print(f"word score for {guess}: {score}")
        print("\n")



    if found_word:
        print("Found it!")

    else:
        print("Ran out of guesses!")

    

