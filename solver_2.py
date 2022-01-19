"""
This solver will not need a Word as input
You should workwith the solver to get the answer
"""

import random

from words import solution_words, accepted_words


def filter_word_list(word_list, guess, result):
    """
    use the result string of letters to filter the word list
    """

    for i, l  in enumerate(guess):

        if result[i] == "X":
            # letter in correct spot
            filtered_list = [w for w in word_list if l == w[i] ] 

        elif result[i] =="Y":
            # letter in incorrect spot
            filtered_list = [w for w in word_list if l in w and l != w[i]]

        else:
            # wrong letter
            filtered_list = [w for w in word_list if l not in w]

        word_list = filtered_list

    return(word_list)


        
        


if __name__ == "__main__":
    print("starting solver")

    accepted_words = solution_words + accepted_words
    print(f"There are {len(solution_words)} solution words")
    print(f"There are {len(accepted_words)} accepted words")
    print("\n")

    guess = random.choice(accepted_words)

    print(f"The random first guess is {guess}")

    print("\n")
    num_guesses = 0
    solved = False
    while num_guesses < 6 and not solved:
        result = input("What was the result? (X = correct spot, Y=correct letter, 0=wrong letter)")
        if result == "XXXXXX":
            solved = True
        else:
            accepted_words = filter_word_list(accepted_words, guess, result)
            guess = random.choice(accepted_words)

            print(f"Hmmm... ok... I think your next guess should be {guess} \n")

            num_guesses += 1

    if solved:
        print("We got the correct answer!!")

    else:
        print("We ran out of guesses")


    

