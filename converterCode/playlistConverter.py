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

#user must input these themselves
clientId = "c23b1f6bf08b432ba41e399c5875041d"
clientSecret = "6f5e550b3da546b89769447f743187b7"
playlistName = 'JapJam'
channel_id = "UCz6IPC7i4PQGMPtfhV01H6w"


#retrieve the playlist ID using the channel ID
request = youtube.playlists().list(
    part="snippet",
    channelId=channel_id,
    maxResults=40
)
response = request.execute()
for x in range(len(response['items'])): #looks for my playlist named "JapJam"
    if (response['items'][x]['snippet']['title']) == playlistName:
        index = x
playlistID = response['items'][index]['id']


#get the video IDs from the playlist, only comes in groups of up to 50
request = youtube.playlistItems().list(
    part="snippet",
    maxResults = 50,
    playlistId=playlistID
)
# Must find the number of pages that we must sift through
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
    #will not add the video if the video is private or deleted
    if response['items'][i]['snippet']['title'] != "Deleted video" and response['items'][i]['snippet']['title'] != ("Private video"):
        
        #cleaning the titles and artist names to make it easier for spotify to read
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
        


for x in range(loops - 1): #will loop through the pages of youtube call
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
            #same text cleaning as before
            if response['items'][y]['snippet']['videoOwnerChannelTitle'][-8:] == " - Topic":
                artist = (response['items'][y]['snippet']['videoOwnerChannelTitle'][:-8]).lower()
            else:
                artist = (response['items'][y]['snippet']['videoOwnerChannelTitle']).lower()
            
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
            jpnChannel = jpnChannel.replace(" - topic", "")
            jpnChannel = jpnChannel.replace("official", "")
            jpnChannel = jpnChannel.replace(" channel", "")
            jpnChannel = jpnChannel.replace(" youtube", "")
            jpnChannel = jpnChannel.strip()
            jpnWord = jpnWord.strip()
            jpnWord = jpnWord.replace(jpnChannel, "")

            jpnTitles.append(jpnWord)
            jpnArtist.append(jpnChannel)


#---------------------------------------------------youtube section above-------------------------------------

#creates the playlist
logger = logging.getLogger('examples.create_playlist')


def get_args_playlistCreate(): #will read the playlist name and description if the user decides to add
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlists')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    return parser.parse_args()


#this call will create the playlist using the argument that was passed in
args = get_args_playlistCreate()
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                client_id=clientId,
                                                client_secret=clientSecret,
                                                redirect_uri="http://localhost:3000"))
user_id = sp.me()['id']
playlistName = args.playlist
sp.user_playlist_create(user_id, playlistName)
print("playlist created")


#first we will want to get the playlist ID to add the playlist we just created
scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=clientId,
                                               client_secret=clientSecret,
                                               redirect_uri="http://localhost:3000"))

#we will find the playlist that we just created and use that playlist to add to
results = sp.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
    if item['name'] == playlistName:
        createdPlaylistId = item['uri'][17:]
print("playlist id: " + createdPlaylistId)

#then we will use the list of artists names and titles to get the links for the songs



sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=clientId,
                                                                         client_secret=clientSecret))
for x in range(len(titles)):
    artistName = artists[x]
    titleName = titles[x]
    jpnTitle = jpnTitles[x]
    jpnName = jpnArtist[x]
    query = "artist:"+artistName #this query is the romanized query
    backupQuery = "artist:" + jpnName # the backup query is the japanese character query
    result = sp.search(query,type = 'track', limit = 50, offset = 0)

    #we must calculate how many pages to loop through
    loopsForTracks = result['tracks']['total'] / 100
    if loopsForTracks % 1 < 0.5:
        loopsForTracks +=1
    loopsForTracks = round(loopsForTracks)
    found = False
    couldNotFind = False
    while (found == False and couldNotFind == False):
        
        for y in range (len(result['tracks']['items'])): # will loop through the intial call
            if found == False:
                try: # we will use 'in' because the youtube title name is often longer than the spotify name
                    if (katsu.romaji(result['tracks']['items'][y]['name'])).lower() in titles[x]:
                        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                                    client_id=clientId,
                                                    client_secret=clientSecret,
                                                    redirect_uri="http://localhost:3000"))
                        trackID = ['']
                        trackID[0] = result['tracks']['items'][y]['external_urls']['spotify']
                        sp.playlist_add_items(createdPlaylistId, trackID)
                        print("adding: " + titles[x])
                        found = True
                        continue
                except: #if the lowercase romaji name returns an error just run the same call without the lower
                    if  katsu.romaji(result['tracks']['items'][y]['artists'][0]['name']) in titles[x]:
                        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                                    client_id=clientId,
                                                    client_secret=clientSecret,
                                                    redirect_uri="http://localhost:3000"))
                        trackID = ['']
                        trackID[0] = result['tracks']['items'][y]['external_urls']['spotify']
                        sp.playlist_add_items(createdPlaylistId, trackID)
                        print("adding: " + titles[x])
                        found = True
                        continue


        #will search through the additional pages to find the track
        for y in range(loopsForTracks):
            if found == False:
                result = sp.search(query, limit = 50, offset = y * 50)
                for z in range(len(result['tracks']['items'])):
                    if (katsu.romaji(result['tracks']['items'][z]['name'])).lower() in titles[x]:
                        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                                client_id=clientId,
                                                client_secret=clientSecret,
                                                redirect_uri="http://localhost:3000"))
                        trackID = ['']
                        trackID[0] = result['tracks']['items'][z]['external_urls']['spotify']
                        sp.playlist_add_items(createdPlaylistId, trackID)
                        print("adding: " + titles[x])
                        #function for adding placed here
                        found = True
                        continue

        #this will use the japanese character title & artist name to search on spotify if the romanji version fails
        if found == False: 
            result = sp.search(backupQuery,type = 'track', limit = 50, offset = 0)
            print("trying: " + jpnTitles[x] + " by " + jpnArtist[x])
            while (found == False and couldNotFind == False):
                for y in range (len(result['tracks']['items'])):
                    if found == False:
                        if ((result['tracks']['items'][y]['name'])) in jpnTitles[x]:
                            #print(result['tracks']['items'][y]['name'])
                            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                                        client_id=clientId,
                                                        client_secret=clientSecret,
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

    #notifies user if it fails to find the track
    if found == False:
        print("Could not find: " + titles[x])
        

print("finished transfer")

