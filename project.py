#spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="c23b1f6bf08b432ba41e399c5875041d",
                                               client_secret="6f5e550b3da546b89769447f743187b7",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

#youtube
##api key AIzaSyBcsEhle2A5jxZIO15bym6ilr4iAqX8kdo