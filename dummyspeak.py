from lib.discordspeak import DiscordSpeak, Module

class Outbursts(Module):
    def process_message(self, message):
        message.add_additional_message("I'm a dummy")

class NoMistakes(Module):
    def on_key(self, key):
        if key.name == "backspace":
            return False

class Contractions(Module):
    def process_message(self, message):
        return message.message.replace("i had", "i'd")

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
    ]

    def process_word(self, word):
        if word.string().lower() in Giggles.GIGGLE_WORDS:
            return "*giggles*"

def main():
    app = DiscordSpeak(name="Dummyspeak")

    app.run([
        NoMistakes(),
        Outbursts(),
        Giggles(),
        Contractions(),
    ])

if __name__ == '__main__':
    main()