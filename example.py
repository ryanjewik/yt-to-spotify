# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python


##api key AIzaSyBcsEhle2A5jxZIO15bym6ilr4iAqX8kdo

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
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query

#retrieve the playlist ID using the channel ID
request = youtube.playlists().list(
    part="snippet",
    channelId="UCz6IPC7i4PQGMPtfhV01H6w",
    maxResults=40
)
response = request.execute()
#print(response['items'][10])
#print(response['items'][0]['snippet']['title'])
for x in range(len(response['items'])):
    if (response['items'][x]['snippet']['title']) == 'JapJam':
        index = x
#print(index)
playlistID = response['items'][index]['id']
#print(playlistID)
#print(response['items'][38])
#we will have to grab the speciic playlist ID from this call

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
#print(loops)
titles = []
for i in range(50):
    titles.append(response['items'][i]['snippet']['title'])
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
        titles.append(response['items'][y]['snippet']['title'])
    #print(response['items'])
# Print the results
print(titles)
print(len(titles))
for x in titles:
    if x == "Deleted video":
        titles.remove(x)
print(len(titles))
#print(response['items'][0]['snippet']['title'])

#now we want to take the total results and divide that by 50. That number will give us how many times we have to get the results and we will change the token page every time
#if we add all of these to a list and get the video title for each one we can then use those titles to search in the spotify API