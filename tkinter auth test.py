from tkinter import *
from tkinter import ttk
from unicodedata import name
import tekore as tk
import ssl
from unicodedata import name
from datetime import datetime
import os
from os.path import exists

######################################################################################################################################

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
        conf = tk.config_from_file(file, return_refresh=True)
        token = tk.refresh_user_token(*conf[:2], conf[3])    
        refreshToken = True
        pass
    except tk.BadRequest:
        refreshToken = False

root = Tk()
root.title("Instructions")
window_width = 600
window_height = 400

label = Label(root, text='- Log in and authorize the app with Spotify.\n- Copy URL of the redirect website.\n- Paste into terminal.')
label.pack(ipadx=10, ipady=10)

def disable_event():
    pass

root.protocol("WM_DELETE_WINDOW", disable_event)

if refreshToken == False:
    #Assigns client details to config.
    redirect_uri = "https://example.com/callback"
    client_id="eb8d88a0f9d143c3b9e234ba69b9516c"
    client_secret="c51987ab9ef745b9a72806ef9ef2cb6b"
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    #Opens browser for user authentication and refresh token.
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(file, conf + (token.refresh_token,))

#Spotify OAuth using token above.
spotify = tk.Spotify(token)

root.destroy()

######################################################################################################################################

