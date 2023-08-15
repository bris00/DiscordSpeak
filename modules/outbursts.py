from lib.discordspeak import Module, helpers

import random

class Outbursts(Module):
    OUTBURSTS = [
        "I'm a dummy",
    ]

    def __init__(self, likelihood=1/100):
        self.likelihood = likelihood

    def process_message(self, message):
        if helpers.chance(self.likelihood):
            message.add_additional_message(random.choice(Outbursts.OUTBURSTS))