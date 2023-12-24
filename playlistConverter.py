#spotify imports
import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth


#youtube imports

# API client library
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
loops = response['pageInfo']['totalResults'] / response['pageInfo']['resultsPerPage']
if loops % 1 < .5:
    loops +=1
loops = round(loops)
titles = []
artists = []

for i in range(50):
    if response['items'][i]['snippet']['title'] != "Deleted video" and response['items'][i]['snippet']['title'] != ("Private video"):
        #print("adding: " + response['items'][i]['snippet']['title'])
        titles.append(response['items'][i]['snippet']['title'])
        if response['items'][i]['snippet']['videoOwnerChannelTitle'][-8:] == " - Topic":
                
            try:
                artists.append(response['items'][i]['snippet']['videoOwnerChannelTitle'][:-8])
            except:
                artists.append(response['items'][i]['snippet']['title'])
                print("failed for " + response['items'][y]['snippet']['title'] + " at index " + str(y))
        else:
            try:
                artists.append(response['items'][i]['snippet']['videoOwnerChannelTitle'])
            except:
                artists.append(response['items'][i]['snippet']['title'])
                print("failed for " + response['items'][y]['snippet']['title'] + " at index " + str(y))
for x in range(loops - 1):
    nextPageToken = response['nextPageToken']
    request = youtube.playlistItems().list(
    part="snippet",
    maxResults = 50,
    pageToken = nextPageToken,
    playlistId=playlistID
    )
    response = request.execute()
    for y in range(len(response['items'])):
        if response['items'][y]['snippet']['title'] != "Deleted video" and response['items'][y]['snippet']['title'] != ("Private video"):

            titles.append(response['items'][y]['snippet']['title'])
            #print(response['items'][y]['snippet']['videoOwnerChannelTitle'])
            if response['items'][y]['snippet']['videoOwnerChannelTitle'][-7:] == "- Topic":
                
                try:
                    artists.append(response['items'][y]['snippet']['videoOwnerChannelTitle'][:-8])
                except:
                    artists.append(response['items'][y]['snippet']['title'])
                    print("failed for " + response['items'][y]['snippet']['title'] + " at index " + str(y))
            else:
                try:
                    artists.append(response['items'][y]['snippet']['videoOwnerChannelTitle'])
                except:
                    artists.append(response['items'][y]['snippet']['title'])
                    print("failed for " + response['items'][y]['snippet']['title'] + " at index " + str(y))

# Print the results
#print(titles)
print(artists)
print(len(titles))
for x in range(len(titles)):
    if titles[x] == "Deleted video":
        titles.remove(titles[x])
        artists.remove(artists[x])
print(len(titles))
print(len(artists))

#---------------------------------------------------youtube section-------------------------------------
"""
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

"""
