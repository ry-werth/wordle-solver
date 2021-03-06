from words import solution_words, accepted_words
from collections import defaultdict
import pickle


all_words = solution_words + accepted_words

letter_placement_count_dict = {}

for w1 in all_words:
    letter_counter_list = [0,0,0,0,0]
    for w2 in all_words:
        if w1 != w2:
            for ix in range(5):
                if w1[ix] == w2[ix]:
                    letter_counter_list[ix] += 1

    letter_placement_count_dict[w1] = letter_counter_list

print(letter_placement_count_dict["treat"])
with open('letter_placement_dict.pkl', 'wb') as f:
   pickle.dump(letter_placement_count_dict, f)
