from lib.discordspeak import DiscordSpeak, Module

from modules.contractions import Contractions
from modules.outbursts import Outbursts
from modules.no_mistakes import NoMistakes
from modules.max_syllables import MaxSyllables
from modules.giggles import Giggles


def main():
    app = DiscordSpeak(name="Dummyspeak")

    app.run([
        NoMistakes(),
        Outbursts(),
        Giggles(),
        Contractions(),
        MaxSyllables(2),
    ])

if __name__ == '__main__':
    main()