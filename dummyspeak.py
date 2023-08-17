from lib.discordspeak import DiscordSpeak, Module

from modules.contractions import Contractions
from modules.outbursts import Outbursts
from modules.no_mistakes import NoMistakes
from modules.max_syllables import MaxSyllables
from modules.giggles import Giggles
from modules.open_porn import OpenPorn
from modules.spelling_mistakes import SpellingMistakes
from modules.no_cheating import NoCheating
from modules.small_vocabulary import SmallVocabulary



def main():
    app = DiscordSpeak(name="Dummyspeak")

    app.run([
        NoMistakes(),
        Outbursts(likelihood=1/10),
        Giggles(),
        Contractions(),
        MaxSyllables(2),
        OpenPorn(likelihood=1/1000),
        SpellingMistakes(likelihood=1/30),
        NoCheating(),
        SmallVocabulary(5000),
    ])

if __name__ == '__main__':
    main()