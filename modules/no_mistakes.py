from lib.discordspeak import Module

class NoMistakes(Module):
    def on_key(self, key):
        if key.name == "backspace":
            return []