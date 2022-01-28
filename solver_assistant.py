"""
This solver will not use a driver and open a browser
You will have to work with the program to feed it results while you play wordle
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

# removes words with duplicate letters
def remove_repeat_letter_words(word_list):
    return([x for x in word_list if len(set(x)) == len(x)])

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
            filtered_list = accepted_words
            # remove words with repeat letters so we can eliminate more options
            if len(accepted_words) > 10:
                no_repeats = remove_repeat_letter_words(accepted_words)
                if len(no_repeats) > 0:
                    filtered_list = no_repeats

            filtered_tuple = rank_words(filtered_list)
            guess_tuple = filtered_tuple[-1]
            score = guess_tuple[0]
            guess = guess_tuple[1]


            print( 
                random.choice(
                    [
                        f"Hmmm... ok... I think your next guess should be {guess} \n",
                        f"Interesting feedback...your next guess should probably be {guess} \n",
                        f"Easy Peezy, your next guess is {guess}",
                        f"Idk try {guess}",
                        f"Beep Boop Bop, enter {guess} as your next guess\n",
                    ]
                )
            )


            num_guesses += 1

    if solved:
        print("We got the correct answer!!")

    else:
        print("We ran out of guesses")


    

