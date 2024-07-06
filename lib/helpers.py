import os, sys
import random
from itertools import repeat
from nltk.metrics.distance import edit_distance

def vocabulary_words(n=None):
    if n is None:
        for line in open(vocabulary_filename, encoding='utf-8'):
            yield line.split(" ")[0]
    else:
        lines = open(vocabulary_filename, encoding='utf-8')

        for _ in range(n):
            yield next(lines).split(" ")[0]

def in_vocabulary(word, vocab=None):
    if vocab is None:
        return word.lower() in vocabulary
    else:
        return word.lower() in vocab

def chance(odds):
    return random.random() < odds

vocabulary_filename = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), 'files', 'enwiki-words-frequency.txt')

vocabulary = set(vocabulary_words())

def match(word, list):
    return any(fn(word.lower()) for fn in list)

def distance(word, d):
    return lambda x: edit_distance(word, x) <= d

def exact(word):
    return lambda x: x == word

def choice(list):
    return random.choice([
        instance for item in list for instance in repeat(item[1], item[0])
    ])

def item(x, weight=1):
    return (weight, x)