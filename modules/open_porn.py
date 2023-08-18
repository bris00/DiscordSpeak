from lib.discordspeak import Module
from lib.helpers import chance

import webbrowser

class OpenPorn(Module):
    def __init__(self, likelihood=1/100):
        self.likelihood = likelihood

    def on_key(self, _):
        if chance(self.likelihood):
            webbrowser.open("https://scrolller.com/r/cumsluts")
