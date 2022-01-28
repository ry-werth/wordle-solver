"""
Creates a list of letters A-Z orderd by frequency in the set of words
Pickles this list for future use
"""

from words import solution_words, accepted_words
from collections import defaultdict
import pickle


all_words = solution_words + accepted_words

d = defaultdict(int)

for w in all_words:
    for letter in w:
        d[letter] += 1

sorted_tuple  = sorted(d.items(), key =lambda kv:(kv[1], kv[0]))
sorted_letters = [x[0] for x in sorted_tuple]

print(sorted_letters)

with open('sorted_letters.pkl', 'wb') as f:
   pickle.dump(sorted_letters, f)
