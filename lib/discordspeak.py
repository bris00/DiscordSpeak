import wx.adv
import wx
import psutil
import pyperclip

import sys
import random
import os

from nltk.tokenize import TreebankWordTokenizer

TRAY_ICON = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), 'files', 'icon.png')

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, name):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON, name)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Site', self.on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Quit', self.on_exit)
        return menu

    def set_icon(self, path, name):
        icon = wx.Icon(path)
        self.SetIcon(icon, name)

    def on_left_down(self, event):      
        print('Tray icon was left-clicked.')

    def on_hello(self, event):
        print('Hello, world!')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class Message:
    def __init__(self, message, tokenizer):
        self.message = message
        self.additional_messages = []
        self.tokenizer = tokenizer
    
    def add_additional_message(self, message):
        self.additional_messages.append(message)

    def tokenize(self):
        words = []
        words.extend([Word(span, self, words, i) for i, span in enumerate(self.tokenizer(self.message))])

        return words

class Word:
    def __init__(self, span, message, words, index):
        self.start = span[0]
        self.end = span[1]
        self.message = message
        self.words = words
        self.index = index
    
    def string(self):
        return self.message.message[self.start:self.end]

class Module:
    def on_key(self, event):
        pass

    def process_message(self, message: Message):
        pass

    def process_word(self, word: Word):
        pass

class DiscordSpeak:
    def __init__(self, name, tokenizer=None):
        self.current_window = None
        self.name = name

        self.tokenizer = (lambda s: TreebankWordTokenizer().span_tokenize(s)) if tokenizer is None else tokenizer

    def process(self, modules, input):
        message = Message(input, self.tokenizer)

        for module in modules:
            res = module.process_message(message)

            if res is not None:
                message.message = res

        words = message.tokenize()

        for i, word in enumerate(words):
            for module in modules:
                new = module.process_word(word)

                if new is not None:
                    message.message = message.message[:word.start] + new + message.message[word.end:]
                    
                    extra_len = len(new) - (word.end - word.start)
                    word.end += extra_len

                    for w in words[i:]:
                        w.start += extra_len
                        w.end += extra_len

        return message

    def run_cli(self, modules, input):
        message = self.process(modules, input)

        print('\n-------------------------\n'.join((*message.additional_messages, message.message)))

    def run(self, modules):
        if len(sys.argv) > 1:
            self.run_cli(modules, ' '.join(sys.argv[1:]))
            return
        
        # Windows only imports
        from .windows.focus_hook import FocusHook

        import keyboard

        name = self.name
        frame = None

        class App(wx.App):
            def OnInit(self):
                nonlocal frame
                frame = wx.Frame(None)
                self.SetTopWindow(frame)
                TaskBarIcon(frame, name)
                return True

        app = App(False)

        processes = []

        for p in psutil.process_iter():
            try:
                filename = p.exe()

                if not filename:
                    continue

                if "\\Microsoft\\" in filename:
                    continue

                if "\\Windows\\System32\\" in filename:
                    continue

                if not '\\' in filename:
                    continue

                processes.append(filename)
            except psutil.AccessDenied as _:
                continue

        processes = list(set(processes))

        listen_to_process = None

        for p in processes:
            if "discord.exe" in p.lower():
                listen_to_process = p
        
        def handle_copied_message():
            message = self.process(modules, pyperclip.paste())

            for m in message.additional_messages:
                keyboard.write(m)
                keyboard.press("enter")

            keyboard.write(message.message)
            keyboard.press("enter")

        def copy_message():
            keyboard.send("ctrl+x")
            keyboard.call_later(handle_copied_message, args=(), delay=0.0001)

        def on_key(module, event):
            res = module.on_key(event)

            return [event.name] if res is None else res

        def on_press(event):
            print(self.current_window, event.name)

            if self.current_window != listen_to_process:
                keyboard.press(event.scan_code)
                return

            if event.name == "enter":
                keyboard.send("ctrl+a")
                keyboard.call_later(copy_message, args=(), delay=0.0001)
            else:
                
                keys = [event]

                for module in modules:
                    f = lambda event: module.on_key(event)
                    keys = flatten([on_key(module, keyboard.KeyboardEvent("down", key_to_scan_codes(key)[0])) for key in keys])
                
                for key in keys:
                    keyboard.send(key)

        def on_focus(filename):
            self.current_window = filename

        hook = FocusHook(callback=on_focus)
        hook.start()

        keyboard.on_press(on_press, suppress=True)
        app.MainLoop()

        hook.kill()

class helpers:
    @staticmethod
    def chance(odds):
        return random.random() < odds