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
import sqlite3

class Main:
    
    def __init__(self):
        global termChoice
        
        Setup() # Runs config and refresh token setup to be used throughout program.
        HomeGUI() # Runs main GUI.

class ParentGUI(tk.Tk): # Parent class for GUI geometry and settings.
    
    def __init__(self):
        super().__init__()

        self.windowWidth = 600
        self.windowHeight = 500 # Changes window dimensions to 600x500.

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self) # Retrieves window calculations from ScreenCalculations class.

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}") # Centers window on screen.
        self.resizable(False, False) # Disables resizable windows.
        self.configure(
            background="#8edcaa", # Changes backround colour to light green (#8edcaa).
        )

class ScreenCalculations(ParentGUI): # Window geometry calculations.

    def __init__(self):
        super().__init__()
    
    def widthCalc(self): 
        userScreenWidth = self.winfo_screenwidth() # Retrieves width of users screen.
        widthDisplacement = int(((userScreenWidth - self.windowWidth) / 2)) # Calculates x-axis displacement.
        return widthDisplacement

    def heightCalc(self): 
        userScreenHeight = self.winfo_screenheight() # Retrieves height of users screen.
        heightDisplacement = int(((userScreenHeight - self.windowHeight) / 2) - 24) # Calculates x-axis displacement (-24px for Mac toolbar). 
        return heightDisplacement

class TopTracks(tk.Tk):
    def __init__(self, termChoice):
        super().__init__()

        self.termChoice = termChoice
        self.trackCounter = 0

        self.windowWidth = 800
        self.windowHeight = 600 # Changes window dimensions to 800x600.

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self) # Retrieves window calculations from ScreenCalculations class.

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}") # Centers window on screen.
        self.resizable(False, False) # Disables resizable windows.
        self.configure(
            background="#8edcaa", # Changes backround colour to light green (#8edcaa).
        )
        self.title("Top Tracks") # Changes window title.

        for rowAmount in range(6):
            self.rowconfigure(rowAmount, weight=1) # Adds 6 rows to tkinter grid.
        
        for columnAmount in range(2):
            self.columnconfigure(columnAmount, weight=1) # Adds 2 columns to tkinter grid.

        try:
            databaseConnection = sqlite3.connect('userRequests.db') # Opens database connection to read user data.
            databaseCursor = databaseConnection.cursor()

            if termChoice == 'short_term':
                selectQuery = """SELECT * FROM shorttoptracks""" 
            elif termChoice == 'medium_term':
                selectQuery = """SELECT * FROM mediumtoptracks"""
            else:
                selectQuery = """SELECT * FROM longtoptracks""" # Chooses the correct table for the term that the user picks.

            databaseCursor.execute(selectQuery) # Selects all data from correct table.
            trackArray = databaseCursor.fetchall() # Fetches all data from correct table.
            print('Track items retrieved.')

        except sqlite3.Error as error:
            print("Connecting to database has returned an error:", error) # Error handling for database connection.

        finally:
            if databaseConnection:
                databaseCursor.close()
                databaseConnection.close() # Closes database connections.
                print("The connection has closed.")
        
        def nextPage(self): # Displays next 10 results.
            self.trackCounter += 10 # Counter increases by 10 to show next 10 results.
            global tempImageList
            tempImageList = [] # Creates temporary list to store track images.

            for i in range(self.trackCounter - 10, self.trackCounter):
                URL = trackArray[i][4]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)

                tempImageList.append(photo)
                
                # ^ Opens each image URL for the page and reads data for the 10 image labels, then appends to temporary list.           

        def previousPage(self): # Displays previous 10 results.
            self.trackCounter -= 10 # Counter decreases by 10 to show previous 10 results.
            global tempImageList
            tempImageList = [] # Creates temporary list to store track images.

            for i in range(self.trackCounter - 10, self.trackCounter):
                URL = trackArray[i][4]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

                # ^ Opens each image URL for the page and reads data for the 10 image labels, then appends to temporary list.            

        def showPage(self): # GUI to display 10 tracks at a time, including all details and image for each track.

            def forwardCallback(event):
                nextPage(self)
                for widget in self.winfo_children():
                    widget.destroy()
                showPage(self)
            
            # ^ Clears GUI for next 10 results and calls next 10 results.

            def backCallback(event):
                previousPage(self)
                for widget in self.winfo_children():
                    widget.destroy()
                showPage(self)
            
            # ^ Clears GUI for previous 10 results and calls previous 10 results.

            if self.trackCounter == 50: # Removes the next page button if at the last page.

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

            elif self.trackCounter == 10: # Removes the previous page button if at the first page.
                
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
            
            else:  # Both next and previous page buttons available.
                
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
                text=f"{self.trackCounter - 9} - '{trackArray[self.trackCounter - 10][1]}'\n{trackArray[self.trackCounter - 10][2]}",
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
                text=f"{self.trackCounter - 8} - '{trackArray[self.trackCounter - 9][1]}'\n{trackArray[self.trackCounter - 9][2]}",
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
                text=f"{self.trackCounter - 7} - '{trackArray[self.trackCounter - 8][1]}'\n{trackArray[self.trackCounter - 8][2]}",
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
                text=f"{self.trackCounter - 6} - '{trackArray[self.trackCounter - 7][1]}'\n{trackArray[self.trackCounter - 7][2]}",
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
                text=f"{self.trackCounter - 5} - '{trackArray[self.trackCounter - 6][1]}'\n{trackArray[self.trackCounter - 6][2]}",
                compound="right"
            )
            fifthLabel.grid(
                row=3,
                column=0
            )

            sixthLabel = tk.Label(
                image=tempImageList[5],
                background="black", 
                foreground="white", 
                text=f"{self.trackCounter - 4} - '{trackArray[self.trackCounter - 5][1]}'\n{trackArray[self.trackCounter - 5][2]}",
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
                text=f"{self.trackCounter - 3} - '{trackArray[self.trackCounter - 4][1]}'\n{trackArray[self.trackCounter - 4][2]}",
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
                text=f"{self.trackCounter - 2} - '{trackArray[self.trackCounter - 3][1]}'\n{trackArray[self.trackCounter - 3][2]}",
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
                text=f"{self.trackCounter - 1} - '{trackArray[self.trackCounter - 2][1]}'\n{trackArray[self.trackCounter - 2][2]}",
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
                text=f"{self.trackCounter} - '{trackArray[self.trackCounter - 1][1]}'\n{trackArray[self.trackCounter - 1][2]}",
                compound="right"
            )
            tenthLabel.grid(
                row=5,
                column=1
            )

            # ^ All ten tkinter label creation and placement for each page, containing track data and image.

        nextPage(self) # Initial details retrieved.       
        showPage(self) # Initial page displayed.

class TopTracksChoiceGUI(ParentGUI): # Time frame selection.
    
    def __init__(self):
        super().__init__()

        self.title("Top Tracks Menu") # Changes window title.
 
        def shortTermCallback(event): 
            self.destroy()
            termChoice = 'short_term'
            TopTracks(termChoice) 

        def mediumTermCallback(event):
            termChoice = 'medium_term'
            self.destroy()
            TopTracks(termChoice)

        def longTermCallback(event):
            termChoice = 'long_term'
            self.destroy()
            TopTracks(termChoice)

        # ^ Destroys current window and opens top tracks GUI with respective term to the button pressed.

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
        ) # ^ tkinter button creation, placing and binding.

class CurrentlyPlayingGUI(ParentGUI): # Miniature Spotify playback control (only works with Premium).
   
    def __init__(self):
        super().__init__()
        self.title("Playback Control") # Changes title.

        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)

        # ^ Retrieves details from tekore.cfg to create token to access Spotify scopes.

        def currentlyPlayingScreen():
            if self.spotify.playback_currently_playing() == None: # If user either does not have Spotify open, or no song is currently playing.
                nonePlayingLabel = tk.Label(
                    text="No track recognised!\nPlease restart the app.",
                    background='black',
                    foreground='white'
                )
                nonePlayingLabel.place(
                    rely=0.4,
                    relx=0.35,
                    relheight=0.2,
                    relwidth=0.3
                )
            else:
                currentlyPlaying = self.spotify.playback_currently_playing() # Retrieves field for song.

                songID = currentlyPlaying.item.id
                progressTime = currentlyPlaying.progress_ms
                albumCover = currentlyPlaying.item.album.images[0].url

                # ^ Retrieves track ID, timestamp and album cover for song.

                URL = albumCover
                print(URL)
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((300,300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)

                # ^ Opens image URL and reads data for image label creation.

                albumCoverLabel = tk.Label(
                    image=photo
                )
                albumCoverLabel.photo = photo
                albumCoverLabel.place(
                    relx=0.25,
                    rely=0.175,
                )

                # ^ Image label creation and placing.

        currentlyPlayingScreen()
        self.mainloop()

class RecommendationsGUI(ParentGUI): # Displays song recommendation GUI.
    
    def __init__(self):
        super().__init__()
        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)
        
        # ^ Retrieves details from tekore.cfg to create token to access Spotify scopes.

        self.title("Recommendations") # Changes window title.

        for gridAmount in range(3):
            self.columnconfigure(gridAmount, weight=1)
            self.rowconfigure(gridAmount, weight=1)

        # ^ Creates 3x3 object grid.

        def playlistCheck(): #Checks if app curated playlist has already been created, if not then create playlist.
            userID = self.spotify.current_user().id # Retrieves user ID.
            playlistPaging = self.spotify.playlists(userID).items # Retrieves all users playlists.
            playlistExists = False
            for playlists in playlistPaging:
                if playlists.name == 'Spotipython':
                    playlistExists = True
                    playlistID = playlists.id
                    break
                else:
                    playlistExists = False
                
                # Searches through all playlists for matching playlist name.
            
            if playlistExists == False:
                playlistCreation = self.spotify.playlist_create(user_id=userID, name='Spotipython') # Creates playlist if playlist not found.
                playlistExists = True
                playlistID = playlistCreation.id
                
            return playlistID
            
        playlistID = playlistCheck()

        def trackRecGet(): #Gets song recommendation track ID from recently played track ID seeds.
            trackIDList = []

            recentlyPlayedGenre = self.spotify.playback_recently_played(limit=5) # Retrieves the 5 most recent songs in users listening history.
            for track in recentlyPlayedGenre.items:
                recentlyPlayedTrackID = track.track.id
                trackIDList.append(recentlyPlayedTrackID) # Appends all 5 track IDs to list.

            recentlyPlayedRecommendation = self.spotify.recommendations(track_ids=trackIDList, limit=1).tracks[0].id # Retrieves recommendation using 5 track IDs retrieved above for seeding. 
            print(recentlyPlayedRecommendation)
            return recentlyPlayedRecommendation

        def recScreen():
            recID = trackRecGet()
            recURIList = []
            recURIList.append(self.spotify.track(track_id=recID).uri)
            recTrack = self.spotify.track(recID)
            albumURL = recTrack.album.images[0].url

            # ^ Appends track URI to list and retrieves album cover URL.

            URL = albumURL
            print(URL)
            u = urlopen(URL)
            raw_data = u.read()
            u.close()
            im = Image.open(BytesIO(raw_data))
            resized_image= im.resize((300,300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            # ^ Opens image URL and reads data for image label creation.

            panel = tk.Label(
                image=photo,
                background="black", 
                foreground="white", 
                text=f"'{self.spotify.track(recID).name}'\n{self.spotify.track(recID).artists[0].name}",
                compound="top"
            )
            panel.photo = photo
            panel.grid(
                column=1,
                row=1,
            )

            # ^ Creates and centers image in window with border containing track name and artist.

            def playCallback(event):
                playerCheck = media_player.is_playing() # Returns 0 or 1 if preview is paused or playing.

                if playerCheck == 0:
                    media_player.play() # Plays track preview using VLC.
                else:
                    media_player.set_pause(1) # Pauses track preview using VLC.
                
            def replayCallback(event):
                media_player.pause()
                media_player.set_media(media)
                media_player.play()

                # ^ Pauses then refreshes media in VLC to replay preview.

            def yesCallback(event): # Adds recommendation to app curated playlist, goes to next recommendation.
                self.spotify.playlist_add(playlist_id=playlistID, uris=recURIList)

                for widget in self.winfo_children():
                    widget.destroy() # Clears GUI to move onto next recommendation.
                
                media_player.set_pause(1) # Pauses preview to move onto next recommendation.
                recScreen() # Generates next screen.
            
            def noCallback(event):
                for widget in self.winfo_children():
                    widget.destroy()
                
                media_player.set_pause(1)
                recScreen()

                # ^ Clears GUI and skip to next recommendation without modifying playlists.

            # 'Add' button for song recommendation.
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

            # 'Skip' button for song recommendation.
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
            
            trackPreviewURL = self.spotify.track(track_id=recID).preview_url # Retrieves audio file URL for VLC.
            media_player = vlc.MediaPlayer() # Creates VLC player.
            try: # Exception to prevent no preview URL error, and displays message to user.
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
                # ^ 'No preview' dialogue box creation and placing.
            media_player.set_media(media) # Sets VLC media to player to listen to preview.

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
            playButton.bind(
                "<space>",
                playCallback
            )
            # ^ Preview play button creation and placing.

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
            # ^ Preview replay button creation and placing.

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

            # ^ Menubar creation (WINDOWS ONLY)

        recScreen() # Initial recommendation screen.
        self.mainloop()
        
class HomeGUI(ParentGUI):
    
    def __init__(self): #GUI creation and config.
        super().__init__()
        self.title("Spotipython Home") # Changes title.

        def recommendationsLabelEvent(event): # Switches window to recommendations GUI.
            self.destroy() # Clears old GUI.
            RecommendationsGUI()

        def topTracksLabelEvent(event): # Switches window to top track term choice GUI.
            self.destroy() # Clears old GUI.
            TopTracksChoiceGUI()
        
        def playbackControlLabelEvent(event): # Switches window to playback control GUI.
            self.destroy() # Clears old GUI.
            CurrentlyPlayingGUI()

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
        # ^ Recommendations button creation, binding and relative placing.
        
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
        # ^ Top Tracks button creation, binding and relative placing.

        playbackControlLabel = tk.Label(
            text='Playback (Premium)',
            background='black',
            foreground='white'
        )        
        playbackControlLabel.place(
            relx=0.1,
            rely=0.3,
            relwidth=0.25,
            relheight=0.1
        )
        playbackControlLabel.bind(
            "<Button-1>",
            playbackControlLabelEvent
        )
        # ^ Playback Control button creation, binding and relative placing.

        self.mainloop()

class Setup():
    
    def __init__(self):

        self.redirect_uri = "https://example.com/callback"
        self.client_id = "eb8d88a0f9d143c3b9e234ba69b9516c"
        self.client_secret = "c51987ab9ef745b9a72806ef9ef2cb6b"

        self.refreshToken = False # Makes sure token is refreshed on every launch.
        self.configExists = exists('tekore.cfg') # Checks if config file exists.
        self.spotify = ''

        self.setupFunction()

    def mainDatabase(self, token):
        self.spotify = tekore.Spotify(token)
        
        try: # Exception handling for database connection.
            databaseConnection = sqlite3.connect('userRequests.db') # Opens connection to database, creates database on first run.
            databaseCursor = databaseConnection.cursor()
            
            def shortTermTopTracksTable():
                databaseCursor.execute("""DROP TABLE IF EXISTS shorttoptracks""")
                databaseConnection.commit()
                databaseCursor.execute("""CREATE TABLE IF NOT EXISTS shorttoptracks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, artist TEXT, trackid TEXT, imageurl TEXT)""")
                databaseConnection.commit()
                
                userTopTracks = self.spotify.current_user_top_tracks(time_range = 'short_term', limit=50)

                # Creates table in database to store short-term tracks.

                for track in userTopTracks.items:
                    databaseCursor.execute("""INSERT INTO shorttoptracks (name, artist, trackid, imageurl) VALUES (?, ?, ?, ?)""", (track.name, track.artists[0].name, track.id, track.album.images[2].url))
                    databaseConnection.commit()

                    # Retrieves all user data for short-term top tracks and inserts into table.
            
            def mediumTermTopTracksTable():
                databaseCursor.execute("""DROP TABLE IF EXISTS mediumtoptracks""")
                databaseConnection.commit()
                databaseCursor.execute("""CREATE TABLE IF NOT EXISTS mediumtoptracks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, artist TEXT, trackid TEXT, imageurl TEXT)""")
                databaseConnection.commit()
                
                userTopTracks = self.spotify.current_user_top_tracks(time_range = 'medium_term', limit=50)

                # Creates table in database to store medium-term tracks.

                for track in userTopTracks.items:
                    databaseCursor.execute("""INSERT INTO mediumtoptracks (name, artist, trackid, imageurl) VALUES (?, ?, ?, ?)""", (track.name, track.artists[0].name, track.id, track.album.images[2].url))
                    databaseConnection.commit()

                    # Retrieves all user data for medium-term top tracks and inserts into table.

            def longTermTopTracksTable():
                databaseCursor.execute("""DROP TABLE IF EXISTS longtoptracks""")
                databaseConnection.commit()
                databaseCursor.execute("""CREATE TABLE IF NOT EXISTS longtoptracks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, artist TEXT, trackid TEXT, imageurl TEXT)""")
                databaseConnection.commit()
                
                userTopTracks = self.spotify.current_user_top_tracks(time_range = 'long_term', limit=50)

                # Creates table in database to store long-term tracks.

                for track in userTopTracks.items:
                    databaseCursor.execute("""INSERT INTO longtoptracks (name, artist, trackid, imageurl) VALUES (?, ?, ?, ?)""", (track.name, track.artists[0].name, track.id, track.album.images[2].url))
                    databaseConnection.commit()

                    # Retrieves all user data for medium-term top tracks and inserts into table.


            longTermTopTracksTable()
            mediumTermTopTracksTable()
            shortTermTopTracksTable()
            # Function calling.

            print(databaseConnection.total_changes, 'changes to database.')
        except sqlite3.Error as error:
            print("Connecting to database has returned an error: %s" % (' '.join(error.args))) # Returns specific error if problem with database.
        finally:
            if databaseConnection:
                databaseCursor.close()
                databaseConnection.close() # Closes connection with database.
                print("The connection has closed.")
        return
    
    def spotifyOAuth(self, token):
        self.spotify = tekore.Spotify(token)
        self.mainDatabase(token) # Passes token for data retrieval.

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
            try: # Exception to determine if refresh token is not out-of-date using BadRequest errors.
                # Assigns client details to config.
                conf = (self.client_id, self.client_secret, self.redirect_uri)
                file = 'tekore.cfg'

                # Gets refresh token from config file to then authenticate user.
                conf = tekore.config_from_file(file, return_refresh=True)
                token = tekore.refresh_user_token(*conf[:2], conf[3])    
                refreshToken = True
                
                self.spotifyOAuth(token)
                pass
            except tekore.BadRequest:
                self.setupConfigFile(False) # Bad request results in token being refreshed.
        else:
            self.setupConfigFile(False) # Skips straight to browser authentication if config file does not exist.

#Runs program.
def instance():
    thisInstance = Main() # Runs program.
    print('Program terminated.') # Displays if program closes.

if __name__ == '__main__':
    instance() # Creates instance of program.