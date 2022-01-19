"""
This solver will take a word as an input
It will then use the "accepted_words" list from words.py to find that word
"""
import random

from words import solution_words, accepted_words

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

    print(result_string)
    print("\n")
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


        
        


if __name__ == "__main__":
    print("starting solver")

    accepted_words = solution_words + accepted_words
    print(f"There are {len(solution_words)} solution words")
    print(f"There are {len(accepted_words)} accepted words")
    print("\n")

    target = random.choice(solution_words)
    guess = random.choice(accepted_words)

    target = "solar"
    print(f"The target word is {target}")
    guess = "hello"
    print(f"The random first guess is {guess}")


    print("\n")

    num_guesses = 0
    while guess != target and num_guesses < 6:
        list_dict = check_word(target, guess)
        print(list_dict)
        filtered_list = filter_word_list(accepted_words, list_dict)
        num_guesses += 1
        accepted_words = filtered_list
        try:
            guess = random.choice(accepted_words)
            print(f"next guess is {guess}")
        except:
            print(accepted_words)






