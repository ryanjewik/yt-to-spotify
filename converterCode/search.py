# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Radiohead'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                                         client_secret="6f5e550b3da546b89769447f743187b7"))
result = sp.search(search_str,limit = 50, offset = 0)
pprint.pprint(result['tracks']['items'][49]['name'])
pprint.pprint(result['tracks']['total'])
for x in range(int(result['tracks']['total'] / 50)):
    result = sp.search(search_str, limit = 50, offset = x)
    for y in range(50):
        pprint.pprint(result['tracks']['items'][y]['name'])

#pprint.pprint(result['tracks']['items'][6]['name'])
#pprint.pprint(result['tracks']['items'][6]['external_urls']['spotify'])
