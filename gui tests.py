import tkinter as tk
from tkinter import Button, ttk
from turtle import window_height
from unicodedata import name
import tekore as tekore
import ssl
from unicodedata import name
from datetime import datetime
import os
from os.path import exists
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

gui = tk.Tk()

gui.title("alie")

windowWidth = 600
windowHeight = 600

userScreenWidth = gui.winfo_screenwidth()
userScreenHeight = gui.winfo_screenheight()

widthDisplacement = int(((userScreenWidth - windowWidth) / 2))
heightDisplacement = int(((userScreenHeight - windowHeight) / 2) - 24) # -24px for Mac toolbar.

gui.geometry(f"{windowWidth}x{windowHeight}+{widthDisplacement}+{heightDisplacement}")
gui.resizable(False, False)
gui.configure(
    background="#8edcaa",
)

gui.columnconfigure(0, weight=1)
gui.rowconfigure(0, weight=1)

gui.columnconfigure(1, weight=1)
gui.rowconfigure(1, weight=1)

gui.columnconfigure(2, weight=1)
gui.rowconfigure(2, weight=1)

URL = "https://i.scdn.co/image/ab67616d0000b2732b1a62237771427afb899387"
u = urlopen(URL)
raw_data = u.read()
u.close()
im = Image.open(BytesIO(raw_data))
resized_image= im.resize((300,300), Image.Resampling.LANCZOS)

photo = ImageTk.PhotoImage(resized_image)
imageLabel = tk.Label(
    gui, 
    image=photo, 
    background="#8edcaa", 
    foreground="black", 
    text="Everything Goes On\nPorter Robinson",
    compound="top"
)
imageLabel.grid(
    column=1,
    row=1
)

def yesCallback(event):
    print("yes works")
    return

def noCallback(event):
    print("no works")
    return

yesLabel = tk.Label(
    text=">",
    cursor="circle",
    padx=20,
    pady=100,
    bg="green",
    fg="black"
)
yesLabel.grid(
    column=2,
    row=1
)
yesLabel.bind(
    "<Button-1>",
    yesCallback
)

noLabel = tk.Label(
    text="<",
    cursor="X_cursor",
    padx=20,
    pady=100,
    bg="red",
    fg="black"
)
noLabel.grid(
    column=0,
    row=1
)
noLabel.bind(
    "<Button-1>",
    noCallback
)

yesLabel.focus()
noLabel.focus()
gui.mainloop()