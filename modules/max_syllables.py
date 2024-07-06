from lib.discordspeak import Module
from lib.helpers import in_vocabulary

import nltk
import nltk.corpus
nltk.download('cmudict')


class MaxSyllables(Module):
    def __init__(self, max):
        self.max = max
        self.cmud = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        try:
            return self.lookup_num_syllables(word)
        except KeyError:
            return self.num_syllables_heuristic(word)

    def lookup_num_syllables(self, word):
        return min([len(list(y for y in x if y[-1].isdigit())) for x in self.cmud[word.lower()]])

    def num_syllables_heuristic(self, word):
        # Reference: stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
        count = 0
        vowels = 'aeiouy'
        word = word.lower()

        if word[0] in vowels:
            count +=1

        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1

        if word.endswith('e'):
            count -= 1

        if word.endswith('le'):
            count += 1

        if count == 0:
            count += 1

        return count

    def process_message(self, message):
        for word in message.tokenize():
            if not in_vocabulary(word.string()):
                continue

            count = self.num_syllables(word.string())

            # len(word.string()) > 4 and 
            if count > self.max:
                return message.message[:word.start].rstrip() + ", uuuhhh what was I talking about again?"
