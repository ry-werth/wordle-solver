"""
This solver will takes a target word and initial guess as imports
It will then walk through the guesses it took to get from guess to the target

It uses letter placement to score words

Takes an optional command line argument "-g" as the guess
it also takes "-t" to specify the target
They must be a valid five letter words
If no guess or target is given it will choose a random word with no repeat characters
"""
import random
import argparse
from words import solution_words, accepted_words

# use the arg parser to overwrite the guess if an initial word is given
parser = argparse.ArgumentParser(description='Wordle Solver')
parser.add_argument('-g', '--guess', default=None)
parser.add_argument('-t', '--target', default=None)

args = parser.parse_args()
guess = args.guess
target = args.target

def check_word(target, guess):
    """
    check a guess against the target word
    returns
    a list of letters in the wrong place
    a list of letters in the right place
    and a list of letters that arent in the target
    """
    correct_placement = []
    correct_letter = []
    wrong_letter = []
    result_string = ""
    for i, l in enumerate(guess):
        if l == target[i]:
            correct_placement.append((l, i))
            result_string = result_string + "X"

        elif l in target:
            correct_letter.append((l, i))
            result_string = result_string + "Y"

        else:
            wrong_letter.append(l)
            result_string = result_string + "O"

    list_dict = {
        "correct_spot" : correct_placement,
        "correct_letter": correct_letter,
        "wrong_letter": wrong_letter
    }


    return(list_dict)


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

def remove_repeat_letter_words(word_list):
    return([x for x in word_list if len(set(x)) == len(x)])


if __name__ == "__main__":
    print("starting solver")

    guess_tries = []
    missed_words = []

    accepted_words = solution_words + accepted_words
    
    if guess is None:
        guess = random.choice(remove_repeat_letter_words(accepted_words))
    if target is None:
        target = random.choice(accepted_words)

    num_guesses = 1
    while guess != target and num_guesses < 6:
        print(f"Guess number {num_guesses}: {guess}")
        print("\n")
        list_dict = check_word(target, guess)
        filtered_list = filter_word_list(accepted_words, list_dict)
        num_guesses += 1
        accepted_words = filtered_list

        if len(filtered_list) > 10:
            no_repeats = remove_repeat_letter_words(filtered_list)
            if len(no_repeats) > 0:
                filtered_list = no_repeats

        try:
            filtered_tuple = rank_words(filtered_list)
            guess_tuple = filtered_tuple[-1]
            score = guess_tuple[0]
            guess = guess_tuple[1]

        except:
            print(f"Error with {target} on with the filtered list {filtered_list}")

    if guess == target:
        print(f"It has to be {guess}")
        print(f"Success! Found in {num_guesses} guesses")
        guess_tries.append(num_guesses)
    else:
        missed_words.append(target)
        print("Missed")









