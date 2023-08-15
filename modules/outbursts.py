from lib.discordspeak import Module

class Outbursts(Module):
    def process_message(self, message):
        message.add_additional_message("I'm a dummy")