import random
from lib.discordspeak import Module
from lib.helpers import in_vocabulary, chance

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet

def get_wordnet_pos(word):
    morphy_tag = {'NN':wordnet.NOUN, 'JJ':wordnet.ADJ,
                  'VB':wordnet.VERB, 'RB':wordnet.ADV}
    
    return morphy_tag.get(word.tag[:2], None)

class SimplifySpeech(Module):
    def __init__(self, likelihood=1/10):
        self.likelihood = likelihood

    def process_word(self, word):
        if in_vocabulary(word.string()):
            pos = get_wordnet_pos(word)

            # Bail out early if we don't know the wordnet pos
            if pos is None or chance(1 - self.likelihood):
                return

            synsets = wordnet.synsets(word.string().lower(), pos=pos)
            lemmas = [lemma.name() for wn in synsets for lemma in wn.lemmas()]

            if len(lemmas) > 0:
                min_len = min(len(lemma) for lemma in lemmas)
                candidates = list(filter(lambda lemma: len(lemma) == min_len, lemmas))

                return random.choice(candidates)