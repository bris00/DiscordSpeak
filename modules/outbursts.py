from lib.discordspeak import Module
from lib.helpers import chance, item, choice

class Outbursts(Module):
    OUTBURSTS = [
        item("I'm a dummy", weight=3),
        item("I'm a legit snack"),
    ]

    def __init__(self, likelihood=1/100):
        self.likelihood = likelihood

    def process_message(self, message):
        if chance(self.likelihood):
            message.add_additional_message(choice(Outbursts.OUTBURSTS))