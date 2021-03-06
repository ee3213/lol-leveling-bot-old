# global.py
# File used for storing shared global variables

# Numerical variables
numberOfGamesToPlay = -1 # set to -1 to tell the lbot and listener threads to wait
numberOfGamesFinished = 0
goFlag = 1
stopFlag = 0
timeSinceLastClick = 0
gameFlag = 0 # used in lbot.clickMid() to test if game is finished

# Thread variables
listenerThreadID = None # used for terminating the thread properly
listenerThread = None
guiThread = None
botThread = None

# GUI variables
statusLabel = None
gamesPlayedLabel = None
gamesLeftLabel = None
quitbutton = None
