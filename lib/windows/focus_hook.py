# Windows focus event listener code inspiered by https://gist.github.com/keturn/6695625

import sys
import ctypes
import ctypes.wintypes

from threading import Thread, Event

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

# https://stackoverflow.com/questions/15927262/convert-dword-event-constant-from-wineventproc-to-name-in-c-sharp
EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_OBJECT_FOCUS = 0x8005
EVENT_OBJECT_SHOW = 0x8002
EVENT_SYSTEM_DIALOGSTART = 0x0010
EVENT_SYSTEM_CAPTURESTART = 0x8
EVENT_SYSTEM_MINIMIZEEND = 0x17
WINEVENT_OUTOFCONTEXT = 0x0000
PM_REMOVE = 0x0001
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
THREAD_QUERY_LIMITED_INFORMATION = 0x0800

# The types of events we want to listen for, and the names we'll use for
# them in the log output. Pick from
# http://msdn.microsoft.com/en-us/library/windows/desktop/dd318066(v=vs.85).aspx
eventTypes = {
    EVENT_OBJECT_FOCUS: "Focus",
}

def get_process_id(dwEventThread, hwnd):
    # It's possible to have a window we can get a PID out of when the thread
    # isn't accessible, but it's also possible to get called with no window,
    # so we have two approaches.
    h_thread = kernel32.OpenThread(THREAD_QUERY_LIMITED_INFORMATION, 0, dwEventThread)

    if h_thread:
        try:
            process_id = kernel32.GetProcessIdOfThread(h_thread)
            if not process_id:
                print("Couldn't get process for thread %s: %s" % (h_thread, ctypes.WinError()))
        finally:
            kernel32.CloseHandle(h_thread)
    else:
        errors = ["No thread handle for %s: %s" % (dwEventThread, ctypes.WinError(),)]

        if hwnd:
            process_id = ctypes.wintypes.DWORD()
            thread_id = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))

            if thread_id != dwEventThread:
                print("Window thread != event thread? %s != %s" % (thread_id, dwEventThread))
            if process_id:
                process_id = process_id.value
            else:
                errors.append("GetWindowThreadProcessID(%s) didn't work either: %s" % (hwnd, ctypes.WinError()))
                process_id = None
        else:
            process_id = None

        if not process_id:
            for err in errors:
                print(err)

    return process_id

def get_process_filename(process_id):
    h_process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, process_id)
    if not h_process:
        print("OpenProcess(%s) failed: %s" % (process_id, ctypes.WinError()))
        return None

    try:
        filename_buffer_size = ctypes.wintypes.DWORD(4096)
        filename = ctypes.create_unicode_buffer(filename_buffer_size.value)
        kernel32.QueryFullProcessImageNameW(h_process, 0, ctypes.byref(filename), ctypes.byref(filename_buffer_size))

        return filename.value
    finally:
        kernel32.CloseHandle(h_process)

def run(sig, callback):
    ole32.CoInitialize(0)

    def _callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        process_id = get_process_id(dwEventThread, hwnd)

        callback(get_process_filename(process_id))

    WinEventProc = WinEventProcType(_callback)
    user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE

    hook_ids = [setHook(WinEventProc, et) for et in eventTypes.keys()]

    if not any(hook_ids):
        print('SetWinEventHook failed')
        sys.exit(1)

    msg = ctypes.wintypes.MSG()

    while not sig.wait(timeout=0.000001):
        while user32.PeekMessageW(ctypes.byref(msg), 0, 0, 0, PM_REMOVE) != 0:
            user32.TranslateMessageW(msg)
            user32.DispatchMessageW(msg)

    # Cleanup
    for hook_id in hook_ids:
        user32.UnhookWinEvent(ctypes.c_void_p(hook_id))

    ole32.CoUninitialize()

class FocusHook:
    def __init__(self, callback=None):
        self.thread = None
        self.kill_sig = Event()
        self.callback = callback

    def start(self):
        foreground_handle = user32.GetForegroundWindow()
        process_id = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(foreground_handle, ctypes.byref(process_id))
        process_filename = get_process_filename(process_id.value)
        self.callback(process_filename)
        
        self.thread = Thread(target = run, args=(self.kill_sig, self.callback))
        self.thread.start()

    def kill(self):
        self.kill_sig.set()
        self.thread.join()

def setHook(WinEventProc, eventType):
    return user32.SetWinEventHook(
        eventType,
        eventType,
        0,
        WinEventProc,
        0,
        0,
        WINEVENT_OUTOFCONTEXT
    )


