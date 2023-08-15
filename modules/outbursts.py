from lib.discordspeak import Module, helpers

import random

class Outbursts(Module):
    OUTBURSTS = [
        "I'm a dummy",
    ]

    def process_message(self, message):
        if helpers.chance(1/20):
            message.add_additional_message(random.choice(Outbursts.OUTBURSTS))