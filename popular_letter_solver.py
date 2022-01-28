"""
This Solver uses letter popularity to rank words
Words with more common letters will be chosen first


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
import pickle

word_list = solution_words + accepted_words
random_word = random.choice(word_list)
parser = argparse.ArgumentParser(description='Wordle Solver')
parser.add_argument('-g', '--guess', default=random_word)
args = parser.parse_args()

guess = args.guess


 

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot.children', element)
  return shadow_root

def filter_word_list(word_list, list_dict):
    """
    use the dictionary of letters to filter the word dict
    """


    # filter out words that have the excluded letter
    for l in set(list_dict["wrong_letter"]):
        word_list_without_letters = [w for w in word_list if l not in w]
        word_list = word_list_without_letters


    for l_tuple in list_dict["correct_letter"]:

        word_list_with_letters = [w for w in word_list if l_tuple[0] in w and l_tuple[0] != w[l_tuple[1]] ]
        word_list = word_list_with_letters


    for l_tuple in list_dict["correct_spot"]:
        word_list_correct_spot = [w for w in word_list if l_tuple[0] == w[l_tuple[1]] ]
        word_list = word_list_correct_spot


    return(word_list)

with open('sorted_letters.pkl', 'rb') as f:
    letter_order = pickle.load(f)

def word_score(word):
    word_score = 0
    for letter in word:
        letter_score = letter_order.index(letter)
        word_score += letter_score

    return(word_score)

# create webdriver object
driver = webdriver.Firefox()


# get geeksforgeeks.org
driver.get("https://www.powerlanguage.co.uk/wordle/")
 
game_app = driver.find_elements(By.TAG_NAME, "game-app")[0]


shadow_elements = expand_shadow_element(game_app)

game = shadow_elements[1].find_element(By.ID, "game")
time.sleep(1)
game.click()
time.sleep(3)


found_word = False

for guess_num in range(6):

    keyboard = game.find_elements(By.TAG_NAME, "game-keyboard")[0]
    keyboard_shadow_elements = expand_shadow_element(keyboard)[1]

    for l in guess:
        keyboard_shadow_elements.find_element_by_xpath(f"//button[@data-key='{l}']").click()
 
    keyboard_shadow_elements.find_element_by_xpath(f"//button[@data-key='↵']").click()
    time.sleep(3)

    game_row = game.find_elements(By.TAG_NAME, "game-row")[guess_num]
    row_shadow_elements = expand_shadow_element(game_row)

    letters = row_shadow_elements[1].find_elements(By.TAG_NAME, "game-tile")

    correct_count = 0
    correct_location_tuples = []
    wrong_location_tuples = []
    letters_in_word = []
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

    if correct_count == 5:
        found_word = True
        break

    letters_not_in_word = [x[0] for x in letters_not_in_word_tuple if x[0] not in letters_in_word]
    wrong_location_tuples += [x for x in letters_not_in_word_tuple if x[0] in letters_in_word]


    list_dict = {
        "correct_spot" : correct_location_tuples,
        "correct_letter": wrong_location_tuples,
        "wrong_letter": letters_not_in_word

    }


    filtered_list = filter_word_list(word_list, list_dict)   
    word_list = filtered_list

    if len(filtered_list) > 10:
        # remove words with repeat letters
        print("No repeats")
        print(f"{len(filtered_list)} words left")
        no_repeats = [x for x in filtered_list if len(set(x)) == len(x)]
        if len(no_repeats) > 0:
            filtered_list = no_repeats

    filtered_tuple = sorted([(word_score(x), x) for x in filtered_list])
    guess_tuple = filtered_tuple[-1]
    score = guess_tuple[0]
    guess = guess_tuple[1]
    print(f"next guess: {guess}")
    print(f"word score: {score}")



if found_word:
    print("Found it!")

else:
    print("Ran out of guesses!")

    

