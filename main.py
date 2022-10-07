from calendar import c
from collections import UserDict
from http import client
import ssl
from unicodedata import name
import tekore as tekore
from datetime import datetime
import os
from os.path import exists
import vlc
import time
import tkinter as tk
from tkinter import Button, ttk
from turtle import back, width, window_height
from unicodedata import name
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from itertools import cycle

class Main:
    
    def __init__(self):
        Setup() #Runs config and refresh token setup to be used throughout program.
        HomeGUI() #Runs main GUI.

class ParentGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.windowWidth = 600
        self.windowHeight = 500

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self)

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}")
        self.resizable(False, False)
        self.configure(
            background="#8edcaa",
        )

class ScreenCalculations(ParentGUI):

    def __init__(self):
        super().__init__()
    
    def widthCalc(self): #Centers GUI on x-axis.
        userScreenWidth = self.winfo_screenwidth()
        widthDisplacement = int(((userScreenWidth - self.windowWidth) / 2))
        return widthDisplacement

    def heightCalc(self): #Centers GUI on y-axis.
        userScreenHeight = self.winfo_screenheight()
        heightDisplacement = int(((userScreenHeight - self.windowHeight) / 2) - 24) # -24px for Mac toolbar.
        return heightDisplacement

class LongTermGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.windowWidth = 800
        self.windowHeight = 600

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self)

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}")
        self.resizable(False, False)
        self.configure(
            background="#8edcaa",
        )
        self.title("Long Term Top Tracks")

        for rowAmount in range(6):
            self.rowconfigure(rowAmount, weight=1)
        
        for columnAmount in range(2):
            self.columnconfigure(columnAmount, weight=1)

        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)

        topTracks = self.spotify.current_user_top_tracks(time_range = 'long_term', limit=50)
        topTracksNameList = []
        topTracksArtistList = []
        topTracksIDList = []
        topTracksImageList = []
        for track in topTracks.items:
            topTracksNameList.append(track.name)
            topTracksArtistList.append(track.artists[0].name)
            topTracksIDList.append(track.id)
            topTracksImageList.append(track.album.images[0].url)

        global topTrackCount
        topTrackCount = -1

        def nextPage():
            
            global topTrackCount
            topTrackCount += 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def previousPage():
            
            global topTrackCount
            topTrackCount -= 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def showPage():

            def forwardCallback(event):
                nextPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            def backCallback(event):
                previousPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            if topTrackCount == 49:

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            elif topTrackCount == 9:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )
            
            else:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            firstLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-8} - '{tempNameList[0]}'\n{tempArtistList[0]}",
                compound="right"
            )
            firstLabel.grid(
                row=1,
                column=0
            )

            secondLabel = tk.Label(
                image=tempImageList[1],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-7} - '{tempNameList[1]}'\n{tempArtistList[1]}",
                compound="right"
            )
            secondLabel.grid(
                row=1,
                column=1
            )

            thirdLabel = tk.Label(
                image=tempImageList[2],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-6} - '{tempNameList[2]}'\n{tempArtistList[2]}",
                compound="right"
            )
            thirdLabel.grid(
                row=2,
                column=0
            )

            fourthLabel = tk.Label(
                image=tempImageList[3],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-5} - '{tempNameList[3]}'\n{tempArtistList[3]}",
                compound="right"
            )
            fourthLabel.grid(
                row=2,
                column=1
            )            

            fifthLabel = tk.Label(
                image=tempImageList[4],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-4} - '{tempNameList[4]}'\n{tempArtistList[4]}",
                compound="right"
            )
            fifthLabel.grid(
                row=3,
                column=0
            )

            sixthLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-3} - '{tempNameList[5]}'\n{tempArtistList[5]}",
                compound="right"
            )
            sixthLabel.grid(
                row=3,
                column=1
            )

            seventhLabel = tk.Label(
                image=tempImageList[6],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-2} - '{tempNameList[6]}'\n{tempArtistList[6]}",
                compound="right"
            )
            seventhLabel.grid(
                row=4,
                column=0
            )

            eighthLabel = tk.Label(
                image=tempImageList[7],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-1} - '{tempNameList[7]}'\n{tempArtistList[7]}",
                compound="right"
            )
            eighthLabel.grid(
                row=4,
                column=1
            )

            ninthLabel = tk.Label(
                image=tempImageList[8],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount} - '{tempNameList[8]}'\n{tempArtistList[8]}",
                compound="right"
            )
            ninthLabel.grid(
                row=5,
                column=0
            )

            tenthLabel = tk.Label(
                image=tempImageList[9],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount+1} - '{tempNameList[9]}'\n{tempArtistList[9]}",
                compound="right"
            )
            tenthLabel.grid(
                row=5,
                column=1
            )

        nextPage()        
        showPage()

class MediumTermGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.windowWidth = 800
        self.windowHeight = 600

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self)

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}")
        self.resizable(False, False)
        self.configure(
            background="#8edcaa",
        )
        self.title("Medium Term Top Tracks")

        for rowAmount in range(6):
            self.rowconfigure(rowAmount, weight=1)
        
        for columnAmount in range(2):
            self.columnconfigure(columnAmount, weight=1)

        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)

        topTracks = self.spotify.current_user_top_tracks(time_range = 'medium_term', limit=50)
        topTracksNameList = []
        topTracksArtistList = []
        topTracksIDList = []
        topTracksImageList = []
        for track in topTracks.items:
            topTracksNameList.append(track.name)
            topTracksArtistList.append(track.artists[0].name)
            topTracksIDList.append(track.id)
            topTracksImageList.append(track.album.images[0].url)

        global topTrackCount
        topTrackCount = -1

        def nextPage():
            
            global topTrackCount
            topTrackCount += 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def previousPage():
            
            global topTrackCount
            topTrackCount -= 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def showPage():

            def forwardCallback(event):
                nextPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            def backCallback(event):
                previousPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            if topTrackCount == 49:

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            elif topTrackCount == 9:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )
            
            else:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            firstLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-8} - '{tempNameList[0]}'\n{tempArtistList[0]}",
                compound="right"
            )
            firstLabel.grid(
                row=1,
                column=0
            )

            secondLabel = tk.Label(
                image=tempImageList[1],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-7} - '{tempNameList[1]}'\n{tempArtistList[1]}",
                compound="right"
            )
            secondLabel.grid(
                row=1,
                column=1
            )

            thirdLabel = tk.Label(
                image=tempImageList[2],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-6} - '{tempNameList[2]}'\n{tempArtistList[2]}",
                compound="right"
            )
            thirdLabel.grid(
                row=2,
                column=0
            )

            fourthLabel = tk.Label(
                image=tempImageList[3],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-5} - '{tempNameList[3]}'\n{tempArtistList[3]}",
                compound="right"
            )
            fourthLabel.grid(
                row=2,
                column=1
            )            

            fifthLabel = tk.Label(
                image=tempImageList[4],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-4} - '{tempNameList[4]}'\n{tempArtistList[4]}",
                compound="right"
            )
            fifthLabel.grid(
                row=3,
                column=0
            )

            sixthLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-3} - '{tempNameList[5]}'\n{tempArtistList[5]}",
                compound="right"
            )
            sixthLabel.grid(
                row=3,
                column=1
            )

            seventhLabel = tk.Label(
                image=tempImageList[6],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-2} - '{tempNameList[6]}'\n{tempArtistList[6]}",
                compound="right"
            )
            seventhLabel.grid(
                row=4,
                column=0
            )

            eighthLabel = tk.Label(
                image=tempImageList[7],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-1} - '{tempNameList[7]}'\n{tempArtistList[7]}",
                compound="right"
            )
            eighthLabel.grid(
                row=4,
                column=1
            )

            ninthLabel = tk.Label(
                image=tempImageList[8],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount} - '{tempNameList[8]}'\n{tempArtistList[8]}",
                compound="right"
            )
            ninthLabel.grid(
                row=5,
                column=0
            )

            tenthLabel = tk.Label(
                image=tempImageList[9],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount+1} - '{tempNameList[9]}'\n{tempArtistList[9]}",
                compound="right"
            )
            tenthLabel.grid(
                row=5,
                column=1
            )

        nextPage()        
        showPage()

class ShortTermGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.windowWidth = 800
        self.windowHeight = 600

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self)

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}")
        self.resizable(False, False)
        self.configure(
            background="#8edcaa",
        )
        self.title("Short Term Top Tracks")

        for rowAmount in range(6):
            self.rowconfigure(rowAmount, weight=1)
        
        for columnAmount in range(2):
            self.columnconfigure(columnAmount, weight=1)

        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)

        topTracks = self.spotify.current_user_top_tracks(time_range = 'short_term', limit=50)
        topTracksNameList = []
        topTracksArtistList = []
        topTracksIDList = []
        topTracksImageList = []
        for track in topTracks.items:
            topTracksNameList.append(track.name)
            topTracksArtistList.append(track.artists[0].name)
            topTracksIDList.append(track.id)
            topTracksImageList.append(track.album.images[0].url)

        global topTrackCount
        topTrackCount = -1

        def nextPage():
            
            global topTrackCount
            topTrackCount += 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def previousPage():
            
            global topTrackCount
            topTrackCount -= 10

            global tempNameList
            global tempArtistList
            global tempIDList
            global tempImageList

            tempNameList = []
            tempArtistList = []
            tempIDList = []
            tempImageList = []

            for i in range(topTrackCount - 9, topTrackCount + 1):
                tempNameList.append(topTracksNameList[i])
                tempArtistList.append(topTracksArtistList[i])
                tempIDList.append(topTracksIDList[i])
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

        def showPage():

            def forwardCallback(event):
                nextPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            def backCallback(event):
                previousPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()

            if topTrackCount == 49:

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            elif topTrackCount == 9:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )
            
            else:
                
                forwardButton = tk.Label(
                    text='Next >',
                    bg='black',
                    fg='white'
                )
                forwardButton.grid(
                    row=0,
                    column=1
                )
                forwardButton.bind(
                    "<Button-1>",
                    forwardCallback
                )

                backButton = tk.Label(
                    text="< Back",
                    bg='black',
                    fg='white',
                )
                backButton.grid(
                    row=0,
                    column=0
                )
                backButton.bind(
                    "<Button-1>",
                    backCallback
                )

            firstLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-8} - '{tempNameList[0]}'\n{tempArtistList[0]}",
                compound="right"
            )
            firstLabel.grid(
                row=1,
                column=0
            )

            secondLabel = tk.Label(
                image=tempImageList[1],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-7} - '{tempNameList[1]}'\n{tempArtistList[1]}",
                compound="right"
            )
            secondLabel.grid(
                row=1,
                column=1
            )

            thirdLabel = tk.Label(
                image=tempImageList[2],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-6} - '{tempNameList[2]}'\n{tempArtistList[2]}",
                compound="right"
            )
            thirdLabel.grid(
                row=2,
                column=0
            )

            fourthLabel = tk.Label(
                image=tempImageList[3],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-5} - '{tempNameList[3]}'\n{tempArtistList[3]}",
                compound="right"
            )
            fourthLabel.grid(
                row=2,
                column=1
            )            

            fifthLabel = tk.Label(
                image=tempImageList[4],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-4} - '{tempNameList[4]}'\n{tempArtistList[4]}",
                compound="right"
            )
            fifthLabel.grid(
                row=3,
                column=0
            )

            sixthLabel = tk.Label(
                image=tempImageList[0],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-3} - '{tempNameList[5]}'\n{tempArtistList[5]}",
                compound="right"
            )
            sixthLabel.grid(
                row=3,
                column=1
            )

            seventhLabel = tk.Label(
                image=tempImageList[6],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-2} - '{tempNameList[6]}'\n{tempArtistList[6]}",
                compound="right"
            )
            seventhLabel.grid(
                row=4,
                column=0
            )

            eighthLabel = tk.Label(
                image=tempImageList[7],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount-1} - '{tempNameList[7]}'\n{tempArtistList[7]}",
                compound="right"
            )
            eighthLabel.grid(
                row=4,
                column=1
            )

            ninthLabel = tk.Label(
                image=tempImageList[8],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount} - '{tempNameList[8]}'\n{tempArtistList[8]}",
                compound="right"
            )
            ninthLabel.grid(
                row=5,
                column=0
            )

            tenthLabel = tk.Label(
                image=tempImageList[9],
                background="black", 
                foreground="white", 
                text=f"{topTrackCount+1} - '{tempNameList[9]}'\n{tempArtistList[9]}",
                compound="right"
            )
            tenthLabel.grid(
                row=5,
                column=1
            )

        nextPage()        
        showPage()

class TopTracksChoiceGUI(ParentGUI):
    
    def __init__(self):
        super().__init__()

        self.title("Top Tracks Menu")
 
        def shortTermCallback(event):
            self.destroy()
            ShortTermGUI()

        def mediumTermCallback(event):
            self.destroy()
            MediumTermGUI()

        def longTermCallback(event):
            self.destroy()
            LongTermGUI()

        shortTermButton = tk.Label(
            text="Short-term (4 weeks)",
            bg="black",
            fg="white"
        )
        shortTermButton.place(
            relx=0.35,
            rely=0.2,
            relwidth=0.3,
            relheight=0.1
        )
        shortTermButton.bind(
            "<Button-1>",
            shortTermCallback
        )
        
        mediumTermButton = tk.Label(
            text="Medium-term (6 months)",
            bg="black",
            fg="white"
        )
        mediumTermButton.place(
            relx=0.35,
            rely=0.45,
            relwidth=0.3,
            relheight=0.1
        )
        mediumTermButton.bind(
            "<Button-1>",
            mediumTermCallback
        )
        
        longTermButton = tk.Label(
            text="Long-term (All time)",
            bg="black",
            fg="white"
        )
        longTermButton.place(
            relx=0.35,
            rely=0.7,
            relwidth=0.3,
            relheight=0.1
        )
        longTermButton.bind(
            "<Button-1>",
            longTermCallback
        )

class RecommendationsGUI(ParentGUI):
    
    def __init__(self):
        super().__init__()
        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)
        
        self.title("Recommendations")

        for gridAmount in range(3):
            self.columnconfigure(gridAmount, weight=1)
            self.rowconfigure(gridAmount, weight=1)

        def playlistCheck(): #Checks if app curated playlist has already been created, if not then create playlist.
            userID = self.spotify.current_user().id
            playlistPaging = self.spotify.playlists(userID).items
            playlistExists = False
            for playlists in playlistPaging:
                if playlists.name == 'Spotipython':
                    playlistExists = True
                    playlistID = playlists.id
                    break
                else:
                    playlistExists = False
            
            if playlistExists == False:
                playlistCreation = self.spotify.playlist_create(user_id=userID, name='Spotipython')
                playlistExists = True
                playlistID = playlistCreation.id
                
            return playlistID
            
        playlistID = playlistCheck()

        def trackRecGet(): #Gets song recommendation track ID from recently played track ID seeds.
            trackIDList = []

            recentlyPlayedGenre = self.spotify.playback_recently_played(limit=5)
            for track in recentlyPlayedGenre.items:
                recentlyPlayedTrackID = track.track.id
                trackIDList.append(recentlyPlayedTrackID)

            recentlyPlayedRecommendation = self.spotify.recommendations(track_ids=trackIDList, limit=1).tracks[0].id
            print(recentlyPlayedRecommendation)
            return recentlyPlayedRecommendation

        def recScreen():
            recID = trackRecGet()
            recURIList = []
            recURIList.append(self.spotify.track(track_id=recID).uri)

            #Opens URL of album cover, places it middle of grid.
            URL = f"{self.spotify.track(recID).album.images[0].url}"
            print(URL)
            u = urlopen(URL)
            raw_data = u.read()
            u.close()
            im = Image.open(BytesIO(raw_data))
            resized_image= im.resize((300,300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            panel = tk.Label(
                self, 
                image=photo,
                background="black", 
                foreground="white", 
                text=f"'{self.spotify.track(recID).name}'\n{self.spotify.track(recID).artists[0].name}",
                compound="top"
            )
            panel.photo = photo
            panel.grid(
                column=1,
                row=1
            )

            def playCallback(event):
                playerCheck = media_player.is_playing()

                if playerCheck == 0:
                    media_player.play()
                else:
                    media_player.set_pause(1)
                
            def replayCallback(event):
                media_player.pause()
                media_player.set_media(media)
                media_player.play()

            def yesCallback(event): #Adds recommendation to app curated playlist, goes to next recommendation.
                self.spotify.playlist_add(playlist_id=playlistID, uris=recURIList)

                for widget in self.winfo_children():
                    widget.destroy()
                
                media_player.set_pause(1)
                recScreen()
            
            def noCallback(event): #**EDIT THIS**
                print('no code needed\n')
                
                for widget in self.winfo_children():
                    widget.destroy()
                
                media_player.set_pause(1)
                recScreen()

            #'Yes' button for song recommendation.
            greenButton = tk.Label(
                    text=">",
                    padx=20,
                    pady=100,
                    bg="green",
                    fg="black"
            )
            greenButton.grid(
                row = 1,
                column = 2
            )
            greenButton.bind(
                "<Button-1>",
                yesCallback
            )

            #'No' button for song recommendation.
            redButton = tk.Label(
                text="<",
                padx=20,
                pady=100,
                bg= "red",
                fg= "black"
                )
            redButton.grid(
                row=1,
                column=0 
            )
            redButton.bind(
                "<Button-1>",
                noCallback
            )
            
            trackPreviewURL = self.spotify.track(track_id=recID).preview_url
            media_player = vlc.MediaPlayer()
            try:
                media = vlc.Media(trackPreviewURL)
            except TypeError:
                noPreviewButton = tk.Label(
                    text="No preview available, sorry!",
                    padx=7.5,
                    pady=10,
                    bg='black',
                    fg='white'
                )
                noPreviewButton.grid(
                    row=2,
                    column=1
                )
            media_player.set_media(media)

            playButton = tk.Label(
                text="⏯️",
                padx=7.5,
                pady=10,
                bg='black',
                fg='white'
            )
            playButton.grid(
                row=2,
                column=0
            )
            playButton.bind(
                "<Button-1>",
                playCallback
            )

            replayButton = tk.Label(
                text="🔁",
                padx=7.5,
                pady=10,
                bg='black',
                fg='white'
            )
            replayButton.grid(
                row=2,
                column=2
            )
            replayButton.bind(
                "<Button-1>",
                replayCallback
            )

            menubar = tk.Menu(self)
            self.config(menu=menubar)
            
            options_menu = tk.Menu(
                menubar,
                tearoff=0
            )
            
            def goHome():
                media_player.set_pause(1)
                self.destroy()
                HomeGUI()

            options_menu.add_command(
                label='Home',
                command=goHome
            )
            options_menu.add_command(
                label='Exit',
                command=self.destroy,
            )

            menubar.add_cascade(
                label="Options",
                menu=options_menu,
                underline=0
            )

        recScreen()
        self.mainloop()
        
class HomeGUI(ParentGUI):
    
    def __init__(self): #GUI creation and config.
        super().__init__()
        self.title("Spotipython Home")

        def recommendationsLabelEvent(event): #Switches window to recommendations GUI.
            self.destroy()
            RecommendationsGUI()

        def topTracksLabelEvent(event):
            self.destroy()
            TopTracksChoiceGUI()

        #Recommendations button.
        recommendationsLabel = tk.Label(
            text='Recommendations',
            background='black',
            foreground='white'
        )
        recommendationsLabel.bind(
            "<Button-1>",
            recommendationsLabelEvent
        )
        recommendationsLabel.place(
            relx=0.1,
            rely=0.05,
            relwidth=0.25,
            relheight=0.1
        )
        
        topTracksLabel = tk.Label(
            text='Top Tracks',
            background='black',
            foreground='white'
        )
        topTracksLabel.place(
            relx=0.1,
            rely=0.175,
            relwidth=0.25,
            relheight=0.1
        )
        topTracksLabel.bind(
            "<Button-1>",
            topTracksLabelEvent
        )

        self.mainloop()

class Setup:
    
    def __init__(self):
        self.redirect_uri = "https://example.com/callback"
        self.client_id = "eb8d88a0f9d143c3b9e234ba69b9516c"
        self.client_secret = "c51987ab9ef745b9a72806ef9ef2cb6b"
        self.refreshToken = False
        self.configExists = exists('tekore.cfg')
        self.spotify = ''

        self.setupFunction()
    
    def spotifyOAuth(self, token):
        self.spotify = tekore.Spotify(token)
        return self.spotify

    def setupConfigFile(self, refreshToken):
        if refreshToken == False and self.configExists == False:
            #Assigns client details to config.
            conf = (self.client_id, self.client_secret, self.redirect_uri)
            file = 'tekore.cfg'

            #Opens browser for user authentication and refresh token.
            token = tekore.prompt_for_user_token(*conf, scope=tekore.scope.every)
            tekore.config_to_file(file, conf + (token.refresh_token,))

            self.spotifyOAuth(token)
    
    def setupFunction(self):
        if self.configExists == True: 
            try:
                #Assigns client details to config.
                conf = (self.client_id, self.client_secret, self.redirect_uri)
                file = 'tekore.cfg'

                #Gets refresh token from config file to then authenticate user.
                conf = tekore.config_from_file(file, return_refresh=True)
                token = tekore.refresh_user_token(*conf[:2], conf[3])    
                refreshToken = True
                
                self.spotifyOAuth(token)
                pass
            except tekore.BadRequest:
                self.setupConfigFile(False)
        else:
            self.setupConfigFile(False)

#Runs program.
def instance():
    thisInstance = Main()
    print('Program terminated.')

if __name__ == '__main__':
    instance()