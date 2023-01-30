# -*- coding: utf-8 -*-
import random
import tkinter as tk
import threading
import datetime
import configparser
from misc.wordloader import wordloader

version = "1.2.0"
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
sett = config["Setting"]

class Clock(threading.Thread):
    def __init__(self, funct, count=0):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = count
        self.funct = funct

    def run(self):
        while self.count >= 0 and not self.event.is_set():
            self.funct(self.count)
            self.count -= 1
            self.event.wait(1)

    def stop(self):
        self.event.set()


if __name__ == '__main__':
    None

def choise_word(words: list) -> str:
    max = len(words) - 1
    rando = random.randint(0, max)
    return words[rando]


score = 0
remsec = 61
mistype = 0
store = 0
record = 0
logged = False
unbooted = True

wordlist = sett["List"]
nocap = config.getboolean("Setting", "NoCap")
if nocap is True:
    surd = "NoCap "
else:
    surd = ""
least = config.getint("Setting", "Least")
most = config.getint("Setting", "Most")
ranged = [least, most]
if ranged != [0,0]:
    if least == most:
        reit = f"{least} Letters"
    elif most == 0:
        reit = f"More than {least} Letters"
    else:
        reit = f"{least} to {most} Letters"
else:
    reit = ""
    
loaded = wordloader(wordlist, nocap, ranged)
name = sett["Name"]
wordname =loaded[0]
words = loaded[1]

root = tk.Tk()
root.title("TJTyping")
root.geometry("720x360")
root.configure(background="white")
try:
    root.iconbitmap(default="assets/icon.ico")
except tk.TclError:
    pass
canvas = tk.Canvas(root, width=720, height=360, relief=tk.FLAT, bg="#fff")
canvas.place(relwidth=1.0,relheight=1.0)
root.minsize(width=720, height=360)
textScore = canvas.create_text(
    5, 5, text=f"Score:{score}", anchor="nw", font=('Courier', 15), fill="#333")
textSec = canvas.create_text(
    5, 25, text=f"Time :{remsec - 1}", anchor="nw", font=('Courier', 15), fill="#333")
textMissType = canvas.create_text(
    5, 45, text=f"Miss :{mistype}", anchor="nw", font=('Courier', 15), fill="#333")
textName = canvas.create_text(
    5, 65, text=f"Name :{name}", anchor="nw", font=('Courier', 15), fill="#333")
textWordlist = tk.Label(
    text = f"WordList :{wordname} {surd}{reit}", font=('Consolas', 20), justify='center', background="#fff")

def tick(count: int):
    global remsec
    remsec = count


word = "Press Escape Key\nto start game"
word_show = word
word_get = "READY?"
thread = None


def Booter():
    global score, record, unbooted, logged, word_get, remsec, word, thread, mistype, store, word_show

    logged = False
    score = 0
    remsec = 61
    mistype = 0
    record = 0
    word = choise_word(words)
    textWordlist["text"] = "Press Escape Key to quit game"
    while word == word_show:
        word = choise_word(words)
    word_get = "_"
    word_show = word
    store = len(word)
    unbooted = False
    if thread != None:
        thread.stop()
    thread = Clock(tick, count=remsec)
    thread.start()

def Unbooter():
    global score, record, unbooted, logged, word_get, remsec, word, thread, mistype, store, word_show

    logged = False
    unbooted = True
    score = 0
    remsec = 61
    mistype = 0
    record = 0
    word = "Press Escape Key\nto start game"
    textWordlist["text"] = f"WordList :{wordname} {surd}{reit}"
    word_get = "READY?"
    word_show = word
    thread.stop()
    thread = None
    
textTypingShow = tk.Label(
    text=f"{word_show}", font=('Consolas', 20), justify='center', background="#fff")
textTypingShow.pack(anchor='n',expand=0)

textTypingTarget = tk.Label(
    text=f"{word_get}", font=('Consolas', 72), justify='center', background="#fff")
textTypingTarget.pack(anchor='center',expand=1)

textWordlist.pack(anchor='s',expand=0)
canvas.bind("<1>", lambda event: canvas.focus_set())


def handleKeyInput(event):
    global word, score, scene, remsec, store, mistype, word_show, record, word_get
    if word_get == "READY?":
        if event.keysym == "Escape":
            remsec = 61
            Booter()
    else:
        if event.keysym == "Escape":
            if remsec > 0:
                remsec = 61
                Unbooter()
            else:
                remsec = 61
                Booter()
        else:
            if remsec > 0:
                if word[0] == event.char:
                    word_get = word_get[:-1]+word[0]+"_"
                    word = word[1:]
                    record += 1
                    if len(word) == 0:
                        score += store
                        word = choise_word(words)
                        while word == word_show:
                            word = choise_word(words)
                        word_get = "_"
                        word_show = word
                        store = len(word)
                        record = 0
                elif word[0] != event.char:
                    if event.keysym != "BackSpace" and event.char != " " and event.keysym != "Shift_L" and event.keysym != "Shift_R":
                        word_get = word_get[:-1]+event.char
                        mistype += 1
                render()
 

root.bind("<Key>", handleKeyInput)


def render():
    textTypingTarget["text"]=f"{word_get}"
    if word_get != "READY?" and "_" not in word_get:
        textTypingTarget["fg"]="#f00"
    else:
        textTypingTarget["fg"]="#000"
    textTypingShow["text"]=f"{word_show}"
    textWordlist["text"] = "Press Escape Key to quit game"
    canvas.itemconfigure(textScore, text=f"Score:{score}")
    canvas.itemconfigure(textSec, text=f"Time :{remsec - 1}")
    canvas.itemconfigure(textMissType, text=f"Miss :{mistype}")

def render_fin():
    textTypingTarget["text"]=f"END!"
    textTypingTarget["fg"]="#f00"
    textTypingShow["text"]=f"Result"
    textWordlist["text"] = "Press Escape Key to Restart"
    canvas.itemconfigure(textScore, text=f"Scored:{score} + {record}")
    canvas.itemconfigure(textSec, text=f"Time :-")
    canvas.itemconfigure(textMissType, text=f"Missed :{mistype}")

def render_unboot():
    textTypingTarget["text"]=f"READY?"
    textTypingTarget["fg"]="#000"
    textTypingShow["text"]="Press Escape Key\nto start game"
    textWordlist["text"] = f"WordList :{wordname} {surd}{reit}"
    canvas.itemconfigure(textScore, text=f"Scored:{score}")
    canvas.itemconfigure(textSec, text=f"Time :{remsec - 1}")
    canvas.itemconfigure(textMissType, text=f"Miss :{mistype}")
    
def loop():
    global remsec, logged, score, record, mistype
    if unbooted is False:
        if remsec <= 0:
            render_fin()
            if logged is False:
                with open("score.log", mode="a+") as log:
                    log.write(str(datetime.datetime.now()))
                    log.write(f"\nName: {name}")
                    log.write(f"\nWordList: {wordname} {surd}{reit}")
                    log.write(f"\nScore: {score} + {record}")
                    log.write(f"\nMissed: {mistype}\n\n")
                logged = True
        else:
            render()
    else:
        render_unboot()
    root.after(50, loop)


loop()
root.mainloop()
