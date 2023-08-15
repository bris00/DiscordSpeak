from lib.discordspeak import Module

from modules.outbursts import Outbursts

from nltk.tokenize import WhitespaceTokenizer
import random

class NoCheating(Module):
    def process_message(self, message):
        words = WhitespaceTokenizer().tokenize(message.message)

        def filter_fn(word):
            if word[-1] == ",":
                word = word[:-1]

            if word[0] == ":" and word[-1] == ":":
                word = word[1:-1]

            if word.isalpha():
                return False

            non_alpha = list([l for l in word if not l.isalpha()])

            if len(non_alpha) == 1 and non_alpha[0] == "'":
                return False

            if len(non_alpha) < (len(word) // 3):
                return False

            only_alpha = ''.join(filter(lambda l: l.isalpha(), word))

            # TODO: Check if only_alpha is a word in the vocabulary

            print(only_alpha)

            return True

        bad_words = list(filter(filter_fn, words))

        if len(bad_words) > 0:
            message.add_additional_message("Uhhh... thinking is like really difficult right now")
            return random.choice(Outbursts.OUTBURSTS)
        