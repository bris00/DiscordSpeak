from lib.discordspeak import Module

class Giggles(Module):
    GIGGLE_WORDS = [
        "hah",
        "haha",
        "hahaha",
        "heh",
        "hehe",
        "hehehe",
        "lol",
        "rofl",
        "lmao",
        "laughs",
        "^^",
        ":12:",
    ]

    def process_word(self, word):
        if word.string().lower() in Giggles.GIGGLE_WORDS:
            return "*giggles*"