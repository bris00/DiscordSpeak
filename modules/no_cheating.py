from lib.discordspeak import Module
from lib.helpers import choice, in_vocabulary

from modules.outbursts import Outbursts

from nltk.tokenize import WhitespaceTokenizer


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

            if not in_vocabulary(only_alpha):
                return False

            return True

        bad_words = list(filter(filter_fn, words))

        if len(bad_words) > 0:
            message.exit_early()
            message.add_additional_message("Uhhh... thinking is like really difficult right now")
            return choice(Outbursts.OUTBURSTS)

        