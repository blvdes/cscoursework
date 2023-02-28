#Libraries.
import ssl
from unicodedata import name
import tekore as tekore
from datetime import datetime
import os
from os.path import exists
import vlc
import time

refreshToken = False

#If the config file exists AND has a valid refresh token.
if exists('tekore.cfg') == True:
    try:
        #Assigns client details to config.
        redirect_uri = "https://example.com/callback"
        client_id="eb8d88a0f9d143c3b9e234ba69b9516c"
        client_secret="c51987ab9ef745b9a72806ef9ef2cb6b"
        conf = (client_id, client_secret, redirect_uri)
        file = 'tekore.cfg'

        #Gets refresh token from config file to then authenticate user.
        conf = tekore.config_from_file(file, return_refresh=True)
        token = tekore.refresh_user_token(*conf[:2], conf[3])    
        refreshToken = True
        pass
    except tekore.BadRequest:
        refreshToken = False


if refreshToken == False:
    #Assigns client details to config.
    redirect_uri = "https://example.com/callback"
    client_id="eb8d88a0f9d143c3b9e234ba69b9516c"
    client_secret="c51987ab9ef745b9a72806ef9ef2cb6b"
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    #Opens browser for user authentication and refresh token.
    token = tekore.prompt_for_user_token(*conf, scope=tekore.scope.every)
    tekore.config_to_file(file, conf + (token.refresh_token,))

#Spotify OAuth using token above.
spotify = tekore.Spotify(token)
print(spotify)
continueChoice = ''

#Choose between modes (temp), looking to have tkinter UI.
while continueChoice != 'N':
    initChoice = int(input("\n1: top tracks.\n2: search.\n3: currently playing.\n4: recently played.\n5: log out.\n\nInput: "))

    #Top tracks scope.
    if initChoice == 1:    
        timeRangeChoice = int(input("\n1: 4 weeks.\n2: 6 months.\n3: All-time.\n\nInput:"))
        print()
        #Could make all the processes a function.
        #Short-term range (4 weeks).
        if timeRangeChoice == 1:
            topTracks = spotify.current_user_top_tracks(time_range = 'short_term', limit=50)
            count = 0
            #Prints track name and artist name from topTracks class.
            for track in topTracks.items:
                count += 1
                print(str(count) + " - " + track.name + " - " + track.artists[0].name)
        #Medium-term range (6 months).
        elif timeRangeChoice == 2:
            topTracks = spotify.current_user_top_tracks(time_range = 'medium_term', limit=50)
            count = 0
            for track in topTracks.items:
                count += 1
                print(str(count) + " - " + track.name + " - " + track.artists[0].name)
        #Long-term range (All time).
        elif timeRangeChoice == 3:
            topTracks = spotify.current_user_top_tracks(time_range = 'long_term', limit=50)
            count = 0
            for track in topTracks.items:
                count += 1
                print(str(count) + " - " + track.name + " - " + track.artists[0].name)
        else:
            print("Value not in choice range.")
    
    #Search scope.
    elif initChoice == 2:
        analysisSearchChoice = int(input("\n1 to return top 15.\n2 to return analysis.\n\nInput: "))
        if analysisSearchChoice == 1:
            userSearch = input("\nWhat would you like to search for.\n\nInput: ")
            #Gets first 15 results and saves both track search and artist search results.
            resultsArtists, resultsTracks, = spotify.search(userSearch, types=('track', 'artist',), limit=15)
            
            trackNameList = []
            artistNameList = []
            
            #Appends track name to track list and artist name to artist list using same index number.
            for track in resultsTracks.items:
                trackNameList.append(track.name)
                # print(track.name)
                artistNameList.append(track.artists[0].name)
            
            #Prints the track name and it's associated artist name.
            print("Search results:\n")
            for rangeCount in range(15):
                print(trackNameList[rangeCount] + ' - ' + artistNameList[rangeCount])
        #Improvement needed.
        #First result song analysis.
        elif analysisSearchChoice == 2:
            userSearch = input("\nWhat would you like to search for.\n\nInput: ")
            #Gets first result for both track and artist search.
            resultsArtists, resultsTracks, = spotify.search(userSearch, types=('track', 'artist',), limit=1)
            #Prints the tempo for each section of the song.
            for track in resultsTracks.items:
                analysis = spotify.track_audio_analysis(track.id)
                for sections in analysis.sections:
                    print(sections.tempo)

    #Currently playing scope.
    elif initChoice == 3:
        currentlyPlaying = spotify.playback_currently_playing()
        print()
        #Uses currently_playing scope return to print track name and artist name.
        print("You are currently playing " + "'" + currentlyPlaying.item.name + "'" + " by " + currentlyPlaying.item.artists[0].name + ".")

    #Recently played scope.
    elif initChoice == 4:
        recentlyPlayed = spotify.playback_recently_played(limit=20)
        #Prints timestamp and the track name and artist in order.
        for track in recentlyPlayed.items:
            #Formats timestamp for good aesthetic.
            timeStamp = str(track.played_at)
            timeStamp = timeStamp.replace("Z", " ")
            timeStamp = timeStamp.replace("T", " ")
            print(timeStamp + ": " + track.track.name + " - " + track.track.artists[0].name)

    #Log out.
    elif initChoice == 5:
        print("Logging out.")
        #Deletes user config file for next time program is ran.
        os.remove("tekore.cfg")
        file = 'tekore.cfg'
        exit()

    elif initChoice == 6:
        trackIDList = []

        recentlyPlayedGenre = spotify.playback_recently_played(limit=5)
        for track in recentlyPlayedGenre.items:
            recentlyPlayedTrackID = track.track.id
            trackIDList.append(recentlyPlayedTrackID)

        recentlyPlayedRecommendations = spotify.recommendations(track_ids=trackIDList)

        for i in range(0,20):
            print()
            print(recentlyPlayedRecommendations.tracks[i].id)
            print(str(spotify.track(recentlyPlayedRecommendations.tracks[i].id).name) + " - " + str(spotify.track(recentlyPlayedRecommendations.tracks[i].id).artists[0].name))
            trackPreviewURL = spotify.track(recentlyPlayedRecommendations.tracks[i].id).preview_url
            print(trackPreviewURL)

            if trackPreviewURL != None:
                player = vlc.MediaPlayer(trackPreviewURL)
                player.play()
                time.sleep(30)
                player.stop()

    continueChoice = input("\nENTER: Continue.\nN: Stop application.\n\nInput: ")
    continueChoice = continueChoice.upper()
