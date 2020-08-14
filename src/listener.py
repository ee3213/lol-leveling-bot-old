import threading

import pyHook
import pythoncom
import win32api
import win32con
import time

import globals

listenerThreadID = None

def OnKeyboardEvent(event):
    if event.Key == 'F6':
        if(globals.goFlag == 0):
            globals.statusLabel.config(text=globals.lastStatus)
            globals.goFlag = 1
        else:
            globals.lastStatus = globals.statusLabel.cget("text")
            globals.statusLabel.config(text="Bot paused!")
            globals.goFlag = 0
    # return True to pass the event to other handlers
    return True

def hookKeyboard():
    global listenerThreadID

    # wait until the gui thread gets an input
    while(globals.numberOfGamesToPlay == -1):
        time.sleep(0.1)
    # if the user canceled input, then return
    if(globals.numberOfGamesToPlay is None):
        return
    
    print(globals.listenerThread)

    # save the id of the thread
    listenerThreadID = threading.get_ident()

    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()

def createThread():
    globals.listenerThread = threading.Thread(target=hookKeyboard)
    globals.listenerThread.start()

def stop():
    if(listenerThreadID is not None):
        win32api.PostThreadMessage(listenerThreadID, win32con.WM_QUIT, 0, 0)