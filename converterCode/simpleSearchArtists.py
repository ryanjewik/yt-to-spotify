from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

client_credentials_manager = SpotifyClientCredentials(client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                      client_secret="6f5e550b3da546b89769447f743187b7")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='Indigo La End', limit=50)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])