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
    part="id",
    channelId="UC_x5XG1OV2P6uZZ5FSM9Ttw",
    maxResults=40
)
response = request.execute()

#get the video IDs from the playlist, only comes in groups of up to 50
request = youtube.playlistItems().list(
    part="snippet.title",
    playlistId="PLpvIB9kRLD0lV2Um5c_l2kYBAuzA9kPr4"
)
# Query execution
response = request.execute()
# Print the results
print(response)