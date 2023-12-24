# Shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Whoops, need a username!")
    print("usage: python user_playlists.py [username]")
    sys.exit()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="c23b1f6bf08b432ba41e399c5875041d",
                                               client_secret="6f5e550b3da546b89769447f743187b7",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-library-read"))

playlists = sp.user_playlists(username)

for playlist in playlists['items']:
    print(playlist['name'])
    print(playlist['uri'][17:])
    