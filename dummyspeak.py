from lib.discordspeak import DiscordSpeak, Logger, Module

from modules.contractions import Contractions
from modules.outbursts import Outbursts
from modules.no_mistakes import NoMistakes
from modules.max_syllables import MaxSyllables
from modules.giggles import Giggles
from modules.open_porn import OpenPorn
from modules.spelling_mistakes import SpellingMistakes
from modules.no_cheating import NoCheating
from modules.small_vocabulary import SmallVocabulary
from modules.simplify_speech import SimplifySpeech


def main():
    app = DiscordSpeak(name="Dummyspeak")

    app.run([
        #SimplifySpeech(likelihood=1/1),
        #MaxSyllables(2),
        #NoMistakes(),
        #Outbursts(likelihood=1/1),
        #Giggles(),
        #Contractions(),
        #OpenPorn(likelihood=1/1000),
        #Logger(),
        NoCheating(),
        SmallVocabulary(10000),
        #SpellingMistakes(likelihood=1/30),
    ])

if __name__ == '__main__':
    main()