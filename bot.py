#   @author: Mitchell Levesque                                                          #
#   @desc  : A script for the game League of legends which will automatically queue     #
#            a player for intermediate bots, attack move on the enemy nexus until game  #
#            ends, and then repeat.                                                     #

import ctypes
import multiprocessing
import os
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from timeit import default_timer as timer
from tkinter import simpledialog

#test

import cv2
import PIL.ImageGrab
import psutil
import pyautogui
import pyHook
import pythoncom
import win32api
import win32con
import win32gui
from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key
from pywinauto.findwindows import find_window

# Champion select region
champ_select_left = (343,131)
champ_select_right = (934,583)

# Champion Colors
ashe_color = (214,179,211)
annie_color = (234,149,163)

# Button Coordinates
play_coords = (114,40)
party_coords = (127,41)
coop_vs_ai_coords = (121,99)
intermediate_coords = (418,555)
confirm_coords = (512,686)
find_match_coords = (621,673)
accept_coords = (638,531)
lock_in_coords = (637,589)
champ_select_coords = (727,594)
champ_locked_coords = (328,295)
game_recall_coords = (825,711)
game_trinket_coords = (825,685)
game_end_coords = (674,453)
game_health_coords = (582,722)
game_lockscreen_coords = (1068,735)
skip_honor_coords = (641,649)
play_again_coords = (535,676)
ok_levelup_coords = (638,679)
daily_play_coords = (608,69)
daily_play_thresh_coords = (651,309)
daily_play_middle_select_coords = (679,381)
daily_play_ok_coords = (642,677)
riot_client_play_coords = (885,350)


# Button Colors
play_party_color = (236,226,204)
coop_vs_ai_color = (172,183,136)
intermediate_color = (13,31,39)
confirm_color = (29,33,37)
find_match_color = (16, 22, 27)
accept_color = (10,16,22)
lock_in_color = (45,153,164)
champ_select_color = (75,58,24)
champ_locked_color = (203,169,96)
game_recall_color = (189,247,255)
game_trinket_color = (5,13,11)
game_end_color = (165,16,16)
game_health_color = (1,13,7)
game_dead_color = (107, 119, 120)
skip_honor_color = (190,178,132)
play_again_color = (29,33,37)
ok_levelup_color = (184,172,128)
daily_play_color = (233,223,201)
daily_play_thresh_color = (34,115,92)
daily_play_middle_select_color = (29,32,36)
daily_play_ok_color = (194,181,134)
riot_client_play_color = (11,196,226)


# To be removed after daily play is updated to pixel
UPPER_HALF_RECT = [0,0,1280,360]
LOWER_HALF_RECT = [0,360,1280,360]

# Global variables
listOfChampions = [ashe_color, annie_color]
filesToReplace = ['game.cfg', 'input.ini']
clientPath = 'C:\\Riot Games\\League of Legends\\LeagueClient.exe'
numberOfGamesFinished = 0
numberOfGamesToPlay = -1
goFlag = 1
stopFlag = 0
th = None
th2 = None
th2_id = 0
th3 = None
window = None
lastStatus = None
lbl1 = None
lbl2 = None
lbl3 = None
quitbutton = None
gameFlag = 0
timeSinceLastClick = None

keyboard = KeyBoardController()

def SaveUserFiles():
    global filesToReplace
    src = 'C:\\Riot Games\\League of Legends\\Config'
    dst = 'C:\\Program Files (x86)\\League bot\\user_settings'
    for files in filesToReplace:
        shutil.copy(os.path.join(src, files), os.path.join(dst, files))

def SetBotFiles():
    global filesToReplace
    src = 'C:\\Program Files (x86)\\League bot\\bot_settings'
    dst = 'C:\\Riot Games\\League of Legends\\Config'
    for files in filesToReplace:
        shutil.copy(os.path.join(src, files), os.path.join(dst, files))

def SetUserFiles():
    global filesToReplace
    src = 'C:\\Program Files (x86)\\League bot\\user_settings'
    dst = 'C:\\Riot Games\\League of Legends\\Config'
    for files in filesToReplace:
        shutil.copy(os.path.join(src, files), os.path.join(dst, files))

def GetClientCoords():
    hwnd = win32gui.FindWindow(None, 'League of Legends')
    rect = win32gui.GetWindowRect(hwnd)
    return rect

def GetGameCoords():
    hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client')
    rect = win32gui.GetWindowRect(hwnd)
    return rect

def GetRiotClientCoords():
    hwnd = win32gui.FindWindow(None, 'Riot Client')
    rect = win32gui.GetWindowRect(hwnd)
    return rect

def AttemptToClickOn(picture, region, isGame=False, click=True, conf=0.99):
    global timeSinceLastClick
    if(not goFlag):
        return False
    picture = 'C:\\Program Files (x86)\\League bot\\search_images\\' + picture
    coords = None
    try:
        if(isGame):
            rect = GetGameCoords()
        else:
            rect = GetClientCoords()
        if(region is not None):
            start_x = rect[0]+region[0]
            start_y = rect[1]+region[1]
            width = region[2]
            height = region[3]
            rect = (start_x, start_y, width, height)
        coords = pyautogui.locateCenterOnScreen(picture, region=rect, confidence=conf)
        if(coords is not None):
            if(click):
                pyautogui.click(coords[0], coords[1])
            time.sleep(0.5)
            timeSinceLastClick = timer()
            return True
    except Exception:
        return False

def AttemptToClickOnPix(coords, color, isGame=False, isRiotClient=False ,click=True):
    global timeSinceLastClick
    if(not goFlag):
        return False
    try:
        if(isGame):
            rect=GetGameCoords()
        elif(isRiotClient):
            rect=GetRiotClientCoords()
        else:
            rect=GetClientCoords()
        img = PIL.ImageGrab.grab(bbox=rect)
        pix = img.getpixel(coords)
        if(pix==color):
            if(click):
                x = rect[0]+coords[0]
                y = rect[1]+coords[1]
                pyautogui.click(x=x, y=y)
            time.sleep(0.5)
            timeSinceLastClick = timer()
            return True
        time.sleep(0.15)
        return False
    except Exception:
        time.sleep(0.15)
        return False

def Run():
    global goFlag, stopFlag, lbl1, numberOfGamesToPlay, timeSinceLastClick
    while(numberOfGamesToPlay == -1):
        time.sleep(0.1)
    SetStatus('Current status: Starting bot...')
    SaveUserFiles()
    SetBotFiles()
    # If league is in game
    if(IsLeagueInGame()):
        if(stopFlag):
            return
        FocusGameOrClient()
        ClickMid()
    # Otherwise
    else:
        if(stopFlag):
            return
        RestartClient()
        SetStatus('Current status: Awaiting login...')
        clientOpen = False
        AwaitLogin()
    timeSinceLastClick = timer()
    SetStatus('Current status: Queueing for a game...')
    while(True):
        if(stopFlag):
            return
        # If bot is paused, wait 1 second then try again
        if(not goFlag):
            time.sleep(1)
            timeSinceLastClick = timer()
            continue
        # If we are in game, simply execute the ClickMid() function
        if(IsLeagueInGame()):
            ClickMid()
            continue
        # Check for daily play rewards
        if(AttemptToClickOnPix(daily_play_coords,daily_play_color)):
            DailyPlay()
        # Check for level up rewards
        AttemptToClickOnPix(ok_levelup_coords, ok_levelup_color)

        # Check for buttons
        AttemptToClickOnPix(play_coords,play_party_color)
        AttemptToClickOnPix(party_coords,play_party_color)
        AttemptToClickOnPix(coop_vs_ai_coords,coop_vs_ai_color)
        AttemptToClickOnPix(find_match_coords,find_match_color)
        AttemptToClickOnPix(intermediate_coords,intermediate_color)
        AttemptToClickOnPix(confirm_coords,confirm_color)
        AttemptToClickOnPix(find_match_coords,find_match_color)
        AttemptToClickOnPix(accept_coords,accept_color)
        if(LockInChampion()):
            SetStatus("Current status: In champion select...")
            while(AttemptToClickOnPix(champ_locked_coords,champ_locked_color, click=False)):
                time.sleep(1)
        AttemptToClickOnPix(play_again_coords,play_again_color)
        AttemptToClickOnPix(find_match_coords,find_match_color)
    
        # If 2 minutes has elapsed without doing anything, restart client
        if(DidTimeout(120)):
            ClientStuck()

def DidTimeout(seconds):
    global timeSinceLastClick
    if(timer() - timeSinceLastClick > seconds):
        return True
    else:
        return False

def LockInChampion():
    global listOfChampions
    if(not AttemptToClickOnPix(champ_select_coords, champ_select_color, click=False)):
        return False
    for champion in listOfChampions:
        if(ScanForChamp(champion)):
            if(AttemptToClickOnPix(lock_in_coords,lock_in_color)):
                return True
            else:
                return False
    return False

def ScanForChamp(champColor):
    try:
        rect = GetClientCoords()
        img = PIL.ImageGrab.grab(bbox=rect)
        for x in range(champ_select_left[0], champ_select_right[0]):
            for y in range(champ_select_left[1], champ_select_right[1]):
                pix = img.getpixel((x,y))
                if(pix == champColor):
                    xCoord = rect[0]+x
                    yCoord = rect[1]+y
                    pyautogui.click(x=xCoord, y=yCoord)
                    time.sleep(0.5)
                    return True
    except Exception:
        return

def IsLeagueInGame():
    try:
        find_window(title='League of Legends (TM) Client')
        return True
    except:
        return False

def IsClientOpen():
    try:
        find_window(title='League of Legends')
        return True
    except:
        return False

def IsRiotClientOpen():
    try:
        find_window(title='Riot Client')
        return True
    except:
        return False

def ClickMid():
    global goFlag, stopFlag, numberOfGamesFinished, gameFlag, lbl1, lbl2, lbl3, timeSinceLastClick
    SetStatus('Current status: Waiting for game to start...')
    # Wait until recall is visible, then we know we're in game
    while(not AttemptToClickOnPix(game_recall_coords, game_recall_color, isGame=True, click=False)):
        if(stopFlag):
            return
        if(not goFlag):
            time.sleep(1)
            continue
        time.sleep(1)
    # Lock the screen once we're in game
    LockScreen()
    # Test to see if the game just started, or if the bot started mid game (check trinket)
    if(AttemptToClickOnPix(game_trinket_coords, game_trinket_color, isGame=True, click=False)):
        SetStatus('Current status: Waiting for minions to spawn...')
        rect = GetGameCoords()
        x = rect[0]+1170
        y = rect[1]+666
        win32api.SetCursorPos((x,y))
        time.sleep(15)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        for i in range(70):
            if(stopFlag):
                return
            time.sleep(1)
    # Click mid
    SetStatus('Current status: Running it down mid...')
    gameFlag = 1
    while(gameFlag):
        if(stopFlag):
            return
        if(not goFlag):
            time.sleep(1)
            continue
        # If we're out of game
        if(not IsLeagueInGame()):
            gameFlag=0
            continue
        try:
            rect = GetGameCoords()
        except Exception as e:
            time.sleep(3)
            continue
        x = rect[0]+1260
        y = rect[1]+592
        # Right click down mid
        for i in range(5):
            if(not goFlag):
                continue
            #if(AttemptToClickOnPix(game_health_coords, game_health_color, isGame=True, click=False)):
                #FallBack()
            try:
                win32api.SetCursorPos((x,y))
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,x,y,0,0)
                time.sleep(1)
            except Exception:
                time.sleep(3)
                continue
    if(not stopFlag):
        IncrementGames()
        if(numberOfGamesFinished == numberOfGamesToPlay):
            SetStatus("The bot successfully finished %d out of %d games!" % (numberOfGamesFinished, numberOfGamesToPlay))
            lbl3.config(text="")
            lbl2.config(text="")
            stopFlag = 1
            win32api.PostThreadMessage(th2_id, win32con.WM_QUIT, 0, 0)
            return
        SetStatus("Currently queueing for a game...")
        timeSinceLastClick = timer()
        while(not AttemptToClickOnPix(skip_honor_coords,skip_honor_color)):
            if(stopFlag):
                return
            if(DidTimeout(30)):
                ClientStuck()
                return
            time.sleep(1)

def ClientStuck():
    global timeSinceLastClick, goFlag, stopFlag
    SetStatus('Current status: Program stuck.  Rebooting...')
    RestartClient()
    SetStatus('Current status: Awaiting login...')
    AwaitLogin()
    timeSinceLastClick = timer()
    SetStatus('Current status: Queueing for a game...')

def AwaitLogin():
    while(True):
        if(stopFlag):
            return
        elif(not goFlag):
            time.sleep(1)
            continue
        elif(AttemptToClickOnPix(play_coords, play_party_color)):
            return
        elif(AttemptToClickOnPix(party_coords, play_party_color)):
            return
        elif(AttemptToClickOnPix(daily_play_coords, daily_play_color)):
            DailyPlay()
            return
        elif(AttemptToClickOnPix(riot_client_play_coords, riot_client_play_color, isRiotClient=True)):
            pass

def LockScreen():
    try:
        rect = GetGameCoords()
        x,y = game_lockscreen_coords
        x = rect[0]+x
        y = rect[1]+y
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    except:
        pass

def FallBack():
    if(not goFlag):
        return
    try:
        rect = GetGameCoords()
    except:
        return
    x = rect[0]+20
    y = rect[1]+720
    for i in range(2):
        if(not goFlag):
            return
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        time.sleep(3)
    time.sleep(2)
    x = rect[0]+824
    y = rect[1]+711
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    if(AttemptToClickOnPix(game_health_coords, game_health_color, isGame=True, click=False)):
        for i in range(12):
            if(not goFlag):
                time.sleep(1)

def OpenClient():
    global clientPath
    try:
        subprocess.Popen(clientPath)
    except Exception as e:
        print(e)
        sys.exit()

def RestartClient():
    if(IsClientOpen()):
        SetStatus('Current status: Restarting client...')
        try:
            for proc in psutil.process_iter():
                if proc.name() == "LeagueClient.exe":
                    proc.kill()
                    break
        except Exception as e:
            print(e)
        while(IsClientOpen()):
            if(stopFlag):
                return
            time.sleep(1)
    else:
        SetStatus('Current status: Starting client...')
    OpenClient()
    for i in range(5):
        if(stopFlag):
            return
        time.sleep(1)

def DailyPlay():
    global timeSinceLastClick
    SetStatus('Current status: Collecting daily play rewards...')
    done = False
    start = timer()
    while(not done):
        if(stopFlag):
            return
        if(not goFlag):
            timeSinceLastClick = timer()
            time.sleep(1)
            continue
        # If we don't find anything within 30 seconds, the client is probably stuck
        if(DidTimeout(30)):
            ClientStuck()
        AttemptToClickOn('dailyplay_caitlyn.png', None)
        AttemptToClickOn('dailyplay_illaoi.png', None)
        AttemptToClickOn('dailyplay_ziggs.png', None)
        if(AttemptToClickOnPix(daily_play_thresh_coords, daily_play_thresh_color)):
            AttemptToClickOnPix(daily_play_middle_select_coords, daily_play_middle_select_color)
        AttemptToClickOn('dailyplay_ekko.png', None)
        AttemptToClickOn('select_daily.png', LOWER_HALF_RECT)
        done = AttemptToClickOnPix(daily_play_ok_coords, daily_play_ok_color)
    return

def MoveWindows():
    try:
        hwnd = win32gui.FindWindow(None, 'League Bot')
        win32gui.MoveWindow(hwnd, 10, 180, 300, 110, True)
        if(IsClientOpen()):
            hwnd = win32gui.FindWindow(None, 'League of Legends')
            win32gui.MoveWindow(hwnd, 350, 180, 1280, 720, True)
        if(IsLeagueInGame()):
            hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client')
            win32gui.MoveWindow(hwnd, 600, 180, 1280, 720, True)
    except Exception as e:
        return
    
def FocusGameOrClient():
    pass
    # if(IsLeagueInGame()):
    #     SetForegroundWindow(find_window(title='League of Legends (TM) Client'))
    # elif(IsClientOpen()):
    #     SetForegroundWindow(find_window(title='League of Legends'))

def Launch():
    global th, th2, th3

    th = threading.Thread(target=Listener)
    th.start()

    th3 = threading.Thread(target=BuildGUI)
    th3.start()

    th2 = threading.Thread(target=Run)
    th2.start()

def QuitBot():
    global goFlag, stopFlag, th3, th2, window, th2_id
    if(stopFlag==0):
        goFlag = 0
        stopFlag = 1
        win32api.PostThreadMessage(th2_id, win32con.WM_QUIT, 0, 0)
        th.join()
        th2.join()
    window.destroy()
    SetUserFiles()
    
def OnKeyboardEvent(event):
    global goFlag, lastStatus
    if event.Key == 'F6':
        if(goFlag == 0):
            lbl1.config(text=lastStatus)
            goFlag = 1
        else:
            lastStatus = lbl1.cget("text")
            lbl1.config(text="Bot paused!")
            goFlag = 0
    # return True to pass the event to other handlers
    return True

def Listener():
    global numberOfGamesToPlay, th2_id
    th2_id = threading.get_ident()
    while(numberOfGamesToPlay == -1):
        time.sleep(0.1)
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()

def BuildGUI():
    global window, lbl1, lbl2, lbl3, quitbutton, numberOfGamesToPlay
    window = tk.Tk()
    window.geometry('300x105+5+180')
    window.title('League Bot')
    window.focus_set()
    window.protocol("WM_DELETE_WINDOW", QuitBot)
    numberOfGamesToPlay = simpledialog.askinteger(title="League Bot", prompt="How many games do you want to play?", 
                                                    minvalue=1, maxvalue=100, parent=window)
    if(not numberOfGamesToPlay):
        numberOfGamesToPlay = 100
    lbl1 = tk.Label(window, width=300,text="Current status: Starting bot...")
    lbl1.pack()
    lbl2 = tk.Label(window, width=300, text="Number of games played so far: %d" % numberOfGamesFinished)
    lbl2.pack()
    if(numberOfGamesToPlay == 1):
        lbl3 = tk.Label(window, width=300, text="Bot will stop after this game.")
    else:
        lbl3 = tk.Label(window, width=300, text="Bot will stop after %d more games." % (int)(numberOfGamesToPlay-numberOfGamesFinished))
    lbl3.pack()
    quitbutton = tk.Button(window, text="Quit", width=8, command=QuitBot)
    quitbutton.pack(side=tk.RIGHT)
    gamesButton = tk.Button(window, text="Edit Games", width=8, command=QuitBot)
    gamesButton.pack(side=tk.LEFT)

    window.mainloop()

def SetStatus(status):
    global lbl1, stopFlag
    if(stopFlag):
        return
    lbl1.config(text=status)

def IncrementGames():
    global numberOfGamesFinished, numberOfGamesToPlay, lbl2, lbl3
    numberOfGamesFinished = numberOfGamesFinished + 1
    lbl2.config(text="Number of games played so far: %d" % numberOfGamesFinished)
    gamesLeft = numberOfGamesToPlay-numberOfGamesFinished
    if(gamesLeft == 1):
        lbl3.config(text="Bot will stop after this game")
    else:
        lbl3.config(text="Bot will stop after %d more games." % (int)(numberOfGamesToPlay-numberOfGamesFinished))

def GetColor(coords, isGame=False, isRiotClient=False):
    if(isGame):
        rect=GetGameCoords()
    elif(isRiotClient):
        rect=GetRiotClientCoords()
    else:
        rect=GetClientCoords()
    img = PIL.ImageGrab.grab(bbox=rect)
    pix = img.getpixel(coords)
    print(pix)

Launch()
