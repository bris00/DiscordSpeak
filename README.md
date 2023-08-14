## Requirements
- Windows

## Setup environment
- Download and install [Python](https://www.python.org/downloads/).
- Run `python -m venv .venv`
- Run `./.venv/Scripts/activate`
- Run `pip install -r requirements.txt`

## Run DiscordSpeak under development
```powershell
$ ./.venv/Scripts/activate

# Run a message through the modules
$ python dummyscript.py "This is a test hehe"
This is a test *giggles*

# Start listener daemon, quit with ctrl+c or right click trayicon -> quit
$ python dummyscript.py
[snip]
```

## Package exe for dummies
```powershell
$ ./.venv/Scripts/activate

# This outputs a distributable folder in the dist folder, the exe should be
# executable on windows and can easily be made into a shortcut
$ pyinstaller --add-data="files/icon.png;files" .\dummyspeak.py

# Run exe to test it
$ ./dist/dummyspeak/dummyspeak.exe
[snip]
```

## Requirements
Tested on 
- Windows 10
- Python 3.10.11