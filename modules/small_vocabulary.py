from lib.discordspeak import Module
from lib.helpers import vocabulary, vocabulary_words, in_vocabulary

class SmallVocabulary(Module):
    def __init__(self, vocabulary_size=20000):
        self.neg_vocabulary = vocabulary - set(vocabulary_words(vocabulary_size))

    def process_word(self, word):
        if in_vocabulary(word.string(), vocab=self.neg_vocabulary):
            return "*mumble*"
