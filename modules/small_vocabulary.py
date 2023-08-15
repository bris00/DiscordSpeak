from lib.discordspeak import Module

class SmallVocabulary(Module):
    def on_key(self, key):
        if helpers.chance(1/100):
            if key.name not in keyboard_near or helpers.chance(1/2):
                return []
            else:
                return [random.choice(keyboard_near[key.name])]