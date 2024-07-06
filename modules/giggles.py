from lib.discordspeak import Module
from lib.helpers import match, exact, distance

class Giggles(Module):
    GIGGLE_WORDS = [
        distance("haha", 1),
        distance("hahaha", 1),
        distance("hehe", 1),
        distance("hehehe", 1),
        exact("lol"),
        exact("rofl"),
        exact("lmao"),
        distance("laugh", 2),
        distance("laughing", 2),
        exact("^^"),
        exact(":12:"),
    ]

    def process_word(self, word):
        if match(word.string(), Giggles.GIGGLE_WORDS):
            return "*giggles*"