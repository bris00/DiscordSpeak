from lib.discordspeak import Module
import os
import sys

class SmallVocabulary(Module):
    def __init__(self, vocabulary_size=5000):
        lines = open(os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), 'files', 'enwiki-words-frequency.txt'))

        for _ in range(vocabulary_size):
            next(lines)

        self.neg_vocabulary = set(line.split(" ")[0] for line in lines)

    def process_word(self, word):
        if word.string().lower() in self.neg_vocabulary:
            return "*mumble*"
