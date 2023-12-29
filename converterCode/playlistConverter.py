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
jpnTitles = []
jpnArtist = []

for i in range(50):
    title = ""
    artist = ""
    jpnWord = ""
    jpnChannel = ""
    if response['items'][i]['snippet']['title'] != "Deleted video" and response['items'][i]['snippet']['title'] != ("Private video"):
        
        if response['items'][i]['snippet']['videoOwnerChannelTitle'][-8:] == " - Topic":
            artist = (response['items'][i]['snippet']['videoOwnerChannelTitle'][:-8]).lower()
            
        else:
            artist = (response['items'][i]['snippet']['videoOwnerChannelTitle']).lower()
        artist = artist.replace("official", "")
        artist = artist.replace(" channel", "")
        artist = artist.replace(" youtube", "")
        title = katsu.romaji(response['items'][i]['snippet']['title']).lower()
        title = title.replace(" - ", "")
        title = title.replace("mv", "")
        title = title.replace("eve", "")
        title = title.replace(" official", "")
        title = title.replace(" youtube", "")
        title = title.replace(" video", "")
        title = title.replace(" music video", "")
        title = title.replace(" music ", "")
        title = title.replace(" music", "")
        title = title.replace("(music)", "")
        title = title.replace("[", "")
        title = title.replace("]", "")
        title = title.replace("first take", "")
        title = title.strip()
        artist = artist.strip()
        title.replace(artist, "")
        artists.append(artist)
        titles.append(title)

        jpnWord = (response['items'][i]['snippet']['title']).lower()
        jpnChannel = (response['items'][i]['snippet']['videoOwnerChannelTitle']).lower()
        jpnWord = jpnWord.replace("[", "")
        jpnWord = jpnWord.replace("]", "")
        jpnWord = jpnWord.replace(" - ", "")
        jpnWord = jpnWord.replace("mv", "")
        jpnChannel = jpnChannel.replace(" - topic", "")
        jpnChannel = jpnChannel.replace("official", "")
        jpnChannel = jpnChannel.replace(" channel", "")
        jpnChannel = jpnChannel.replace(" youtube", "")
        jpnChannel = jpnChannel.strip()
        jpnWord = jpnWord.strip()
        jpnWord = jpnWord.replace(jpnChannel, "")

        jpnTitles.append(jpnWord)
        jpnArtist.append(jpnChannel)
        


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
        artist = ""
        title = ""
        jpnWord = ""
        jpnChannel = ""
        if response['items'][y]['snippet']['title'] != "Deleted video" and response['items'][y]['snippet']['title'] != ("Private video"):
            if response['items'][y]['snippet']['videoOwnerChannelTitle'][-8:] == " - Topic":
                artist = (response['items'][y]['snippet']['videoOwnerChannelTitle'][:-8]).lower()
            else:
                artist = (response['items'][y]['snippet']['videoOwnerChannelTitle']).lower()
            jpnChannel = jpnChannel.replace(" - topic", "")
            artist = artist.replace("official", "")
            artist = artist.replace(" channel", "")
            artist = artist.replace(" youtube", "")
            title = katsu.romaji(response['items'][y]['snippet']['title']).lower()
            title = title.replace(" - ", "")
            title = title.replace("mv", "")
            title = title.replace("eve", "")
            title = title.replace(" official", "")
            title = title.replace("official", "")
            title = title.replace(" youtube", "")
            title = title.replace(" video", "")
            title = title.replace(" music video", "")
            title = title.replace(" music ", "")
            title = title.replace(" music", "")
            title = title.replace("(music)", "")
            title = title.replace("[", "")
            title = title.replace("]", "")
            title = title.replace("first take", "")
            title = title.strip()
            artist = artist.strip()
            title.replace(artist, "")
            artists.append(artist)
            titles.append(title)
            jpnWord = (response['items'][y]['snippet']['title']).lower()
            jpnChannel = (response['items'][y]['snippet']['videoOwnerChannelTitle']).lower()
            jpnWord = jpnWord.replace("[", "")
            jpnWord = jpnWord.replace("]", "")
            jpnWord = jpnWord.replace(" - ", "")
            jpnWord = jpnWord.replace("mv", "")
            jpnChannel = jpnChannel.replace("official", "")
            jpnChannel = jpnChannel.replace(" channel", "")
            jpnChannel = jpnChannel.replace(" youtube", "")
            jpnChannel = jpnChannel.strip()
            jpnWord = jpnWord.strip()
            jpnWord = jpnWord.replace(jpnChannel, "")

            jpnTitles.append(jpnWord)
            jpnArtist.append(jpnChannel)

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
    titleName = titles[x]
    jpnTitle = jpnTitles[x]
    jpnName = jpnArtist[x]
    query = "artist:"+artistName
    backupQuery = "artist:" + jpnName
    #query = "artist:Aimer track:Katamoi"
    #print("query:" + query)
    result = sp.search(query,type = 'track', limit = 50, offset = 0)

    #pprint.pprint(result['tracks']['total'])
    loopsForTracks = result['tracks']['total'] / 100
    if loopsForTracks % 1 < 0.5:
        loopsForTracks +=1
    loopsForTracks = round(loopsForTracks)
    found = False
    couldNotFind = False
    #print("title: " + titles[x])
    #print("person: " + artistName)
    while (found == False and couldNotFind == False):
        
        for y in range (len(result['tracks']['items'])):
            if found == False:
                try:
                    if (katsu.romaji(result['tracks']['items'][y]['name'])).lower() in titles[x]:
                        #print(result['tracks']['items'][y]['name'])
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
                except:
                    if  katsu.romaji(result['tracks']['items'][y]['artists'][0]['name']) in titles[x]:
                        #print(result['tracks']['items'][y]['name'])
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
            if found == False:
                result = sp.search(query, limit = 50, offset = y * 50)
                for z in range(len(result['tracks']['items'])):
                    #print(result['tracks']['items'][z]['name'])
                    if (katsu.romaji(result['tracks']['items'][z]['name'])).lower() in titles[x]:
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
        if found == False:
            result = sp.search(backupQuery,type = 'track', limit = 50, offset = 0)
            print("trying: " + jpnTitles[x] + " by " + jpnArtist[x])
            while (found == False and couldNotFind == False):
                for y in range (len(result['tracks']['items'])):
                    if found == False:
                        if ((result['tracks']['items'][y]['name'])) in jpnTitles[x]:
                            #print(result['tracks']['items'][y]['name'])
                            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                                        client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                        client_secret="6f5e550b3da546b89769447f743187b7",
                                                        redirect_uri="http://localhost:3000"))
                            trackID = ['']
                            trackID[0] = result['tracks']['items'][y]['external_urls']['spotify']
                            sp.playlist_add_items(createdPlaylistId, trackID)
                            print("adding: " + jpnTitles[x])
                            #function for adding placed here
                            found = True
                            continue
                if found == False:
                    couldNotFind = True


    if found == False:
        print("Could not find: " + titles[x])
        

print("finished transfer")


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
