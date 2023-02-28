import tekore as tekore

file = 'tekore.cfg'
conf = tekore.config_from_file(file, return_refresh=True)
token = tekore.refresh_user_token(*conf[:2], conf[3])
spotify = tekore.Spotify(token)

topTrack = spotify.current_user_top_tracks(time_range = 'short_term', limit=2)
print(topTrack.items[1].album.images[0].url)
