import os
import pickle
import random

corpus_file = 'corpus/numeric_codes_4letters.txt'
recipe_file = 'recipes/numeric_codes.pkl'
if os.path.exists(corpus_file):
    with open(corpus_file, 'r') as cf:
        words = cf.read().splitlines()

blocks = []
if os.path.exists(recipe_file):
    with open(recipe_file, 'rb') as rf:
        blocks = pickle.load(rf)

for i in range(4000):
    selection = set(random.sample(words, 4))
    alphabets = set(''.join(selection))
    if len(alphabets) <= 10:
        remaining = set(words).difference(selection)
        query = []
        while len(query) < 4 and len(remaining):
            q = random.choice(list(remaining))
            remaining.remove(q)
            if set(q).issubset(alphabets):
                query.append(q)
        blocks.append({"words": list(selection), "order": len(alphabets), "query": query})

with open(recipe_file, 'wb') as rf:
    pickle.dump(blocks, rf)
