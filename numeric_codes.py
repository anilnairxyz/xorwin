import itertools
import pickle
import random
import os
from clint.textui import colored, puts, prompt


def solver(words, codes):
    word_sublists = []
    for i, word in enumerate(words):
        sublist_element = words.copy()
        del sublist_element[i]
        word_sublists.extend(list(itertools.permutations(sublist_element)))
    solutions = []
    for sublist in word_sublists:
        if checker(sublist, codes):
            solutions.append(sublist)
    return solutions


def checker(words, codes):
    big_word = ''.join(words)
    alphabets = set(big_word)
    big_code = ''.join(codes)
    numbers_used = set()
    for char in alphabets:
        alphabet_pos = [i for i, c in enumerate(big_word) if char == c]
        number_set = set([big_code[i] for i in alphabet_pos])
        if len(number_set) != 1:
            return False
        elif number_set.issubset(numbers_used):
            return False
        else:
            numbers_used = numbers_used.union(number_set)
    if numbers_used == set(big_code):
        return True
    else:
        return False


def encoder(words, codes, query):
    big_word = ''.join(words)
    big_code = ''.join(codes)
    reply = ''
    for char in query:
        char_pos = big_word.find(char)
        if char_pos >= 0:
            reply += big_code[char_pos]
        else:
            reply += "X"
    return reply


def decoder(words, codes, query):
    big_word = ''.join(words)
    big_code = ''.join(codes)
    reply = ''
    for number in query:
        number_pos = big_code.find(number)
        if number_pos >= 0:
            reply += big_word[number_pos]
        else:
            reply += "X"
    return reply


def picker(f):
    if os.path.exists(f):
        with open(f, 'rb') as rf:
            blocks = pickle.load(rf)
        return blocks
    else:
        raise FileNotFoundError


def selector(blocks):
    query = []
    words_4 = []
    words_3 = []
    while not len(query):
        block = random.choice(blocks)
        words_4 = block["words"].copy()
        attempt = 0
        while not len(query) and attempt <= 6:
            attempt += 1
            words_3 = words_4.copy()
            words_3.remove(random.choice(words_3))
            alphabets = set(''.join(words_3))
            queries = block["query"].copy()
            while len(queries):
                q = random.choice(queries)
                queries.remove(q)
                if set(q).issubset(alphabets):
                    query.append(q)
    return words_4, words_3, query


def questioner(words):
    alphabets = list(set(''.join(words)))
    numbers = ''.join(random.sample("0123456789", len(alphabets)))
    codes = []
    for word in words:
        code = ''.join([numbers[alphabets.index(x)] for x in word])
        codes.append(code)
    return random.sample(codes, len(codes))


def numeric_codes_question():
    solutions = []
    while len(solutions) != 1:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        blocks = picker(os.path.join(dir_path, 'recipes/numeric_codes.pkl'))
        words_4, words_3, queries = selector(blocks)
        query = random.choice(queries)
        codes = questioner(words_3)
        solutions = solver(words_4, codes)
    solution = solutions.pop()
    reply = encoder(solution, codes, query)
    return words_4, codes, query, reply


if __name__ == "__main__":
    i = 0
    c = 0
    alive = True
    while alive:
        words_4, codes, query, reply = numeric_codes_question()
        i += 1
        message = f"{'#'*100} \n"
        message += f"QUESTION {str(i)}\n"
        message += f"{'#'*100} \n"
        message += f"The 4 words are: {colored.cyan('  '.join([x.upper() for x in words_4]))}\n"
        message += f"The 3 codes are: {colored.cyan('  '.join([x.upper() for x in codes]))}\n"
        puts(message)
        question = f"What is the code for {colored.cyan(query.upper())}: "
        user_reply = prompt.query(question)
        message = f"{'='*100} \n"
        if user_reply == "exit":
            message += f"BYE! BYE!\n"
            alive = False
        elif user_reply == reply:
            c += 1
            message += f"{colored.blue('You are RIGHT!')} => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        else:
            message += f"{colored.red('You are WRONG!')} Correct answer is: {colored.red(reply)}"
            message += f" => Score: {colored.blue(str(c)+' / '+str(i))}\n"
        puts(message)
