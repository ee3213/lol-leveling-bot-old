import sys
import threading
import tkinter as tk

import globals
import lbot
import listener

window = None

def build():
    global window
    window = tk.Tk()
    window.geometry('300x105+5+180')
    window.title('League Bot')
    window.focus_set()
    window.protocol("WM_DELETE_WINDOW", quit)

    globals.numberOfGamesToPlay = tk.simpledialog.askinteger(title="League Bot", prompt="How many games do you want to play?", 
                                                    minvalue=1, maxvalue=9999, parent=window)
    if(globals.numberOfGamesToPlay is None):
        quit()

    globals.statusLabel = tk.Label(window, width=300,text="Current status: Starting bot...")
    globals.statusLabel.pack()
    globals.gamesPlayedLabel = tk.Label(window, width=300, text="Number of games played so far: %d" % globals.numberOfGamesFinished)
    globals.gamesPlayedLabel.pack()
    if(globals.numberOfGamesToPlay == 1):
        globals.gamesLeftLabel = tk.Label(window, width=300, text="Bot will stop after this game.")
    else:
        globals.gamesLeftLabel = tk.Label(window, width=300, text="Bot will stop after %d more games." % (int)(globals.numberOfGamesToPlay-globals.numberOfGamesFinished))
    globals.gamesLeftLabel.pack()
    quitbutton = tk.Button(window, text="Quit", width=8, command=quit)
    quitbutton.pack(side=tk.RIGHT)

    window.mainloop()

def quit():
    window.destroy()
    listener.stop()
    globals.listenerThread.join()
    sys.exit()
