from words import solution_words, accepted_words
from collections import defaultdict

all_words = solution_words + accepted_words

d = defaultdict(int)

for w in all_words:
    end_word = w[1:5]
    d[end_word] += 1

item_list = list(d.items())
item_list.sort(key = lambda x: x[1])
# print(item_list[-40:])

end_of_word_string = "ight"
word_list = [x for x in solution_words if x[5-len(end_of_word_string):5] == end_of_word_string]

print(word_list)
print(len(word_list))

