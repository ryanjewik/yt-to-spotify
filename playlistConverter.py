#spotify imports
import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#youtube imports
import googleapiclient.discovery
# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "AIzaSyBcsEhle2A5jxZIO15bym6ilr4iAqX8kdo"
# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

#retrieve the playlist ID using the channel ID
request = youtube.playlists().list(
    part="snippet",
    channelId="UCz6IPC7i4PQGMPtfhV01H6w",
    maxResults=40
)
response = request.execute()
#finds the playlistID
for x in range(len(response['items'])):
    if (response['items'][x]['snippet']['title']) == 'JapJam':
        index = x
playlistID = response['items'][index]['id']


#get the video IDs from the playlist, only comes in groups of up to 50
request = youtube.playlistItems().list(
    part="snippet",
    maxResults = 50,
    playlistId=playlistID
)
# Query execution
response = request.execute()

#finds the number pages it must loop through
loops = response['pageInfo']['totalResults'] / response['pageInfo']['resultsPerPage']
if loops % 1 < .5:
    loops +=1
loops = round(loops)
titles = []
for i in range(50):#adds the first 50 from the first call
    titles.append(response['items'][i]['snippet']['title'])
for x in range(loops - 1): #finds the next page
    nextPageToken = response['nextPageToken']
    request = youtube.playlistItems().list(
    part="snippet",
    maxResults = 50,
    pageToken = nextPageToken,
    playlistId=playlistID
    )
    response = request.execute()
    for y in range(len(response['items'])): #adds the next group of songs
        titles.append(response['items'][y]['snippet']['title'])

# Print the results
print(titles)
print(len(titles))
for x in titles:
    if x == "Deleted video":
        titles.remove(x)
print(len(titles))

#---------------------------------------------------youtube section-------------------------------------

#creates the playlist
logger = logging.getLogger('examples.create_playlist')
logging.basicConfig(level='DEBUG')


def get_args_playlistCreate():
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlists')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    return parser.parse_args()


args = get_args_playlistCreate()
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                client_secret="6f5e550b3da546b89769447f743187b7",
                                                redirect_uri="http://localhost:3000"))
user_id = sp.me()['id']
sp.user_playlist_create(user_id, args.playlist)


"""
Must combine the playlist creation and adding of tracks together
Some questions that I must answer:
 - how do I use the playlist I just created?
  - how do I convert the tracks to links?

"""



#adds to playlist


logger = logging.getLogger('examples.add_tracks_to_playlist')
logging.basicConfig(level='DEBUG')
scope = 'playlist-modify-public'


def get_args_playlistAdd():
    parser = argparse.ArgumentParser(description='Adds track to user playlist')
    parser.add_argument('-u', '--uris', action='append',
                        required=True, help='Track ids')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Playlist to add track to')
    return parser.parse_args()



args = get_args_playlistAdd()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                client_secret="6f5e550b3da546b89769447f743187b7",
                                                redirect_uri="http://localhost:3000"))
sp.playlist_add_items(args.playlist, args.uris)


