#!/usr/bin/python3

import subprocess 
from subprocess import PIPE
import sys
from time import sleep
from tkinter import Tk, Frame, Canvas, PhotoImage, Label
from PIL import ImageTk

import os

orig_pwd = os.path.abspath(os.curdir)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) < 3:
    light_color = 'green'
else:
    light_color = str(sys.argv[2])


t = Tk()

ec = 256
last_ec = -1
active_image = ImageTk.PhotoImage(file=light_color+"-active.png")
inactive_image = ImageTk.PhotoImage(file=light_color+"-inactive.png")

def show_canv():
    label.configure(image=active_image)

def hide_canv():
    label.configure(image=inactive_image)

# Run command as subprocess
def runSubp():
    os.chdir(orig_pwd)
    p = subprocess.Popen("exec " +sys.argv[1], shell=True, stdout=PIPE)
    p.wait()
    error_code = p.returncode
    out = str(p.communicate()[0])[2:-3].split('\\n')
    print("\n".join(out))
    return error_code


def update_light():
    global ec
    global last_ec
    last_ec = ec
    ec = runSubp()
    if ec != last_ec:
        if str(ec) == '0':
            show_canv()
        else:
            hide_canv()
    t.after(1000, update_light)


t.title("JLight")
t.bind_all("<Control-q>", exit)


photoimage = ImageTk.PhotoImage(file="active.png")

label=Label(t, image=photoimage, bg='black')
label.image = photoimage
label.pack()


if __name__ == "__main__":
    update_light()
    t.mainloop()


