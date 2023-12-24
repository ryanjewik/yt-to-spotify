#spotify imports
import argparse
import logging
import sys
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

import cutlet
katsu = cutlet.Cutlet()
katsu.use_foreign_spelling = False
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
        titles.append(katsu.romaji(response['items'][i]['snippet']['title']))
        if response['items'][i]['snippet']['videoOwnerChannelTitle'][-8:] == " - Topic":
                
            try:
                artists.append(response['items'][i]['snippet']['videoOwnerChannelTitle'][:-8])
            except:
                artists.append(response['items'][i]['snippet']['title'])
                print("failed for " + response['items'][i]['snippet']['title'] + " at index " + str(y))
        else:
            try:
                artists.append(response['items'][i]['snippet']['videoOwnerChannelTitle'])
            except:
                artists.append(response['items'][i]['snippet']['title'])
                print("failed for " + response['items'][i]['snippet']['title'] + " at index " + str(y))
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

            titles.append(katsu.romaji(response['items'][y]['snippet']['title']))
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
#print(artists)
#print(len(titles))
for x in range(len(titles)):
    if titles[x] == "Deleted video":
        titles.remove(titles[x])
        artists.remove(artists[x])
#for x in range(len(titles)):
    #print("Track: " + titles[x] + " by " + artists[x])
#print(len(titles))
#print(len(artists))

#---------------------------------------------------youtube section-------------------------------------

#creates the playlist
logger = logging.getLogger('examples.create_playlist')
#logging.basicConfig(level='DEBUG')


def get_args_playlistCreate():
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlists')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    
    #parser.add_argument(playlist = "test2")
    return parser.parse_args()


args = get_args_playlistCreate()
#print(args)

scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                client_secret="6f5e550b3da546b89769447f743187b7",
                                                redirect_uri="http://localhost:3000"))
user_id = sp.me()['id']
playlistName = args.playlist
sp.user_playlist_create(user_id, playlistName)

print("playlist created")

#first we will want to get the playlist ID to add the playlist we just created


scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id="c23b1f6bf08b432ba41e399c5875041d",
                                               client_secret="6f5e550b3da546b89769447f743187b7",
                                               redirect_uri="http://localhost:3000"))

results = sp.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
    if item['name'] == playlistName:
        #createdPlaylistId = item['id']
        createdPlaylistId = item['uri'][17:]
    #print("%d %s" % (i, item['id']))
print("playlist id: " + createdPlaylistId)

#then we will use the list of artists names and titles to get the links for the songs






sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                                         client_secret="6f5e550b3da546b89769447f743187b7"))
for x in range(len(titles)):
    artistName = artists[x]
    result = sp.search(artistName,limit = 50, offset = 0)
    #pprint.pprint(result['tracks']['items'][49]['name'])
    #pprint.pprint(result['tracks']['total'])
    loopsForTracks = result['tracks']['total'] / 100
    if loopsForTracks % 1 < 0.5:
        loopsForTracks +=1
    loopsForTracks = round(loopsForTracks)
    found = False
    giveUp = False
    #print("title: " + titles[x])
    #print("person: " + artistName)
    while (found == False and giveUp == False):
        for y in range (50):
            if katsu.romaji(result['tracks']['items'][y]['name']) in titles[x]:
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                               client_id="c23b1f6bf08b432ba41e399c5875041d",
                                               client_secret="6f5e550b3da546b89769447f743187b7",
                                               redirect_uri="http://localhost:3000"))
                trackID = ['']
                trackID[0] = result['tracks']['items'][y]['external_urls']['spotify']
                sp.playlist_add_items(createdPlaylistId, trackID)
                print("adding: " + titles[x])
                #function for adding placed here
                found = True
                continue
        
        for y in range(loopsForTracks):
            result = sp.search(artistName, limit = 50, offset = y * 50)
            for z in range(50):
                if katsu.romaji(result['tracks']['items'][z]['name']) in titles[x]:
                    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                               client_id="c23b1f6bf08b432ba41e399c5875041d",
                                               client_secret="6f5e550b3da546b89769447f743187b7",
                                               redirect_uri="http://localhost:3000"))
                    trackID = ['']
                    trackID[0] = result['tracks']['items'][z]['external_urls']['spotify']
                    sp.playlist_add_items(createdPlaylistId, trackID)
                    print("adding: " + titles[x])
                    #function for adding placed here
                    found = True
                    continue
        
        giveUp = True
    if giveUp == True:
        print("failed to find: " + titles[x] + " by "+ artistName)
    elif found == True:
        print("found: " + titles[x] + " by "+ artistName)



#then we will use the add function to add the songs to the playlist

#adds to playlist using a link

"""
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
