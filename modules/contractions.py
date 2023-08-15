from lib.discordspeak import Module

class Contractions(Module):
    def process_message(self, message):
        return message.message.replace("i had", "i'd")