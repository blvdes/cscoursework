import tekore as tk

try:
    redirect_uri = "https://example.com/callback"
    client_id="eb8d88a0f9d143c3b9e234ba69b9516c"
    client_secret="c51987ab9ef745b9a72806ef9ef2cb6b"
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    conf = tk.config_from_file(file, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])    
    refreshToken = True
    pass
except tk.BadRequest:
    refreshToken = False

if refreshToken == False:
    redirect_uri = "https://example.com/callback"
    client_id="eb8d88a0f9d143c3b9e234ba69b9516c"
    client_secret="c51987ab9ef745b9a72806ef9ef2cb6b"
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(file, conf + (token.refresh_token,))
    spotify = tk.Spotify(token)

