from lib.discordspeak import Module
from lib.helpers import chance

import random

class Outbursts(Module):
    OUTBURSTS = [
        "I'm a dummy",
        "I'm a legit snack",
    ]

    def __init__(self, likelihood=1/100):
        self.likelihood = likelihood

    def process_message(self, message):
        if chance(self.likelihood):
            message.add_additional_message(random.choice(Outbursts.OUTBURSTS))