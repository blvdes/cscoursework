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

class TopTracksParent(tk.Tk): # Top 50 tracks over time frame.
    def __init__(self, termChoice):
        super().__init__()
        
        self.windowWidth = 800
        self.windowHeight = 600 # Changes window dimensions to 800x600.

        self.termChoice = termChoice

        widthDisplacement = ScreenCalculations.widthCalc(self)
        heightDisplacement = ScreenCalculations.heightCalc(self) # Retrieves window calculations from ScreenCalculations class.

        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{widthDisplacement}+{heightDisplacement}") # Centers window on screen.
        self.resizable(False, False) # Disables resizable windows.
        self.configure(
            background="#8edcaa", # Changes backround colour to light green (#8edcaa).
        )
        self.title("Long Term Top Tracks") # Changes window title.

        for rowAmount in range(6):
            self.rowconfigure(rowAmount, weight=1) 
        
        for columnAmount in range(2):
            self.columnconfigure(columnAmount, weight=1)

        # ^ Creates 2x6 object grid.

        self.cfgfile = 'tekore.cfg'
        self.conf = tekore.config_from_file(self.cfgfile, return_refresh=True)
        self.token = tekore.refresh_user_token(*self.conf[:2], self.conf[3])    
        self.spotify = tekore.Spotify(self.token)

        # ^ Retrieves details from tekore.cfg to create token to access Spotify scopes.

        topTracks = self.spotify.current_user_top_tracks(time_range = f'{termChoice}', limit=50) # Returns users top 50 tracks based on the term picked in the previous GUI.
        topTracksNameList = []
        topTracksArtistList = []
        topTracksIDList = []
        topTracksImageList = []
        for track in topTracks.items:
            topTracksNameList.append(track.name)
            topTracksArtistList.append(track.artists[0].name)
            topTracksIDList.append(track.id)
            topTracksImageList.append(track.album.images[2].url)

        # ^ Appends track name, artist name, track ID and album cover URL to separate lists for all 50 tracks.

        global topTrackCount
        topTrackCount = -1

        # ^ Counter creation for pages.

        def nextPage(): # Displays next 10 results.
            
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

                # ^ Appends all track details to temporary lists for object creation.
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)

                tempImageList.append(photo)
                
                # ^ Opens image URL and reads data for image label creation, then appends to temporary list.           

        def previousPage(): # Displays previous 10 results.
            
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

                # ^ Appends all track details to temporary lists for object creation.
                
                URL = topTracksImageList[i]
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                im = Image.open(BytesIO(raw_data))
                resized_image= im.resize((50,50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)                
                
                tempImageList.append(photo)

                # ^ Opens image URL and reads data for image label creation, then appends to temporary list.         

        def showPage(): # GUI to display 10 tracks at a time, including all details and image for each track.

            def forwardCallback(event):
                nextPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()
            
            # ^ Clears GUI for next 10 results.

            def backCallback(event):
                previousPage()
                for widget in self.winfo_children():
                    widget.destroy()
                showPage()
            
            # ^ Clears GUI for previous 10 results.

            if topTrackCount == 49: # Removes the next page button if at the end of the 50 tracks.

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

            elif topTrackCount == 9: # Removes the previous page button if at the end of the 50 tracks.
                
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

            # ^ All ten tkinter label creation and placement for each page.

        nextPage() # Initial details retrieved.       
        showPage() # Initial page displayed.

class TopTracksChoiceGUI(ParentGUI): # Time frame selection.
    
    def __init__(self):
        super().__init__()

        self.title("Top Tracks Menu") # Changes window title.
 
        def shortTermCallback(event): 
            self.destroy()
            termChoice = 'short_term'
            TopTracksParent(termChoice) 

        def mediumTermCallback(event):
            termChoice = 'medium_term'
            self.destroy()
            TopTracksParent(termChoice)

        def longTermCallback(event):
            termChoice = 'long_term'
            self.destroy()
            TopTracksParent(termChoice)

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
            albumURL = recTrack.album.images[2].url

            #Opens URL of album cover, places it middle of grid.
            URL = albumURL
            print(URL)
            u = urlopen(URL)
            raw_data = u.read()
            u.close()
            im = Image.open(BytesIO(raw_data))
            resized_image= im.resize((300,300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

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
            playButton.bind(
                "<space>",
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
        
        def playbackControlLabelEvent(event):
            self.destroy()
            CurrentlyPlayingGUI()

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


        self.mainloop()

class Setup:
    
    def __init__(self):
        databaseConnection = sqlite3.connect('tekoreConfig.db')
        
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