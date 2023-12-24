

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
