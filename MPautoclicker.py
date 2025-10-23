import pynput
import threading
from tkinter import *
from tkinter import ttk
import time
import re
import sys

Hotkey = pynput.keyboard.Key.f6

mouse = pynput.mouse.Controller()
ThreadStarted = False
Clicking = False

root = Tk()
root.title("MP clicker")

def click(whichButton):
    mouse.click(whichButton,1)
    return

def startAutoclicker(*args):
    global Clicking
    global ThreadStarted
    global delay
    if Clicking == False:
        Clicking = True
        delay = getMs()/1000
        startButton.state(["disabled"])
        stopButton.state(["!disabled"])
        MsDelayEntry.state(["disabled"])
    if ThreadStarted == False:
        print("tee hee?")
        ThreadStarted = True
        print(ThreadStarted)
        thread = threading.Thread(target=clickLoop, daemon = True)
        thread.start()
        
def clickLoop():
    global Clicking
    global delay
    while True:
        time.sleep(delay)
        if Clicking:
            mouse.click(pynput.mouse.Button.left,1)

            
def stopAutoclicker(*args):
    global Clicking
    if Clicking == True:
        Clicking = False
        startButton.state(['!disabled'])
        stopButton.state(['disabled'])
        MsDelayEntry.state(["!disabled"])

def getMs(*args):
    try:
        delay = int(msDelay.get())
        if delay < 10:
            delay = 10
        return delay
    except TclError:
        delay = 10
        return delay

msDelay = IntVar()
msDelay.set(1000)

frame = ttk.Frame(root)
frame.grid(column=0,row=0,sticky=(N,W,E,S))


startButton = ttk.Button(frame, text="Start Autoclicker", command=startAutoclicker)
startButton.grid(column=2,row=2)

stopButton = ttk.Button(frame, text="Stop Autoclicker", command=stopAutoclicker)
stopButton.grid(column=2,row=1)

def changeKeybind():
    listener = pynput.keyboard.Listener(on_press=change_keybind_on_press)
    listener.start()

def changeKeybindLabel():
    global KeybindLabelText
    KeybindLabelText.set(f"Current hotkey: {Hotkey}")

def change_keybind_on_press(key):
    global Hotkey
    Hotkey = key
    changeKeybindLabel()
    return False

def onHotkeyPress(key):
    global Hotkey
    global Clicking
    if key == Hotkey:
        if not Clicking:
            startAutoclicker()
        else:
            stopAutoclicker()
        

keybindButton = ttk.Button(frame, text="Change keybind", command=changeKeybind)
keybindButton.grid(column=2,row=4)


def checkEntry(char):
    return re.match('^[0-9]*$', char) is not None #i copy pasted this line of code from the pynput documentation

checkEntryWrapper = (root.register(checkEntry),'%P') # same thing here

MsDelayEntry = ttk.Entry(frame, width=7, textvariable=msDelay, validate='key', validatecommand=checkEntryWrapper)
MsDelayEntry.grid(column=3,row=3)

MsDelayLabelText = StringVar()
MsDelayLabelText.set("Enter delay between clicks (in ms):")
MsDelayLabel = ttk.Label(frame, text=MsDelayLabelText.get())
MsDelayLabel["textvariable"] = MsDelayLabelText
MsDelayLabel.grid(column=2,row=3,sticky=(N,S,E,W))

KeybindLabelText = StringVar()
KeybindLabelText.set(f"Current hotkey: {Hotkey}")
KeybindLabel = ttk.Label(frame, text=KeybindLabelText.get())
KeybindLabel["textvariable"] = KeybindLabelText
KeybindLabel.grid(column=2,row=6,sticky=(N,S,E,W))

root.iconbitmap(sys.executable) #this assumes that the code is being run within an executable. modify/remove if you are running this inside of an IDE

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
root.resizable(False, False)

stopButton.state(['disabled'])

hotkeyListener = pynput.keyboard.Listener(on_press=onHotkeyPress)
hotkeyListener.start()

root.mainloop()