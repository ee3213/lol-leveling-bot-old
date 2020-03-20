import threading

import pyHook
import pythoncom

import globals

def OnKeyboardEvent(event):
    if event.Key == 'F6':
        print("clicked!")
    # return True to pass the event to other handlers
    return True

def hookKeyboard():
    # save the id of the thread
    globals.listenerThreadID = threading.get_ident()

    # wait until the gui thread gets an input
    while(globals.numberOfGamesToPlay == -1):
        time.sleep(0.1)
    # if the user canceled input, then return
    if(globals.numberOfGamesToPlay is None):
        return
    
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