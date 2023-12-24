import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.add_tracks_to_playlist')
logging.basicConfig(level='DEBUG')
scope = 'playlist-modify-public'


def get_args_playlistAdd():
    parser = argparse.ArgumentParser(description='Adds track to user playlist')
    parser.add_argument('-u', '--uris', action='append',
                        required=False, help='Track ids')
    parser.add_argument('-p', '--playlist', required=False,
                        help='Playlist to add track to')
    return parser.parse_args()


def main():
    #parser = argparse.ArgumentParser(description='Adds track to user playlist')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                   client_secret="6f5e550b3da546b89769447f743187b7",
                                                   redirect_uri="http://localhost:3000"))
    #print("test: " + args.playlist)
    #sp.playlist_add_items(args.playlist, args.uris)
    
    playlist = "https://open.spotify.com/playlist/6AP88Ok6DnSYBM0B30qgc8?si=6f4f92f6553f4f9d"
    uris = []
    uris.append("https://open.spotify.com/track/3y5v0rYHHY9DrkZUM6H2kA?si=bce87e5c36394b15")
    #args = parser.parse_args()
    #args.playlist = playlist
    #args.uris = uris

    args = get_args_playlistAdd()
    #args = get_args_playlistAdd(playlist, uris)
    #print(args.playlist)
    #print(args.uris)
    #sp.playlist_add_items(args.playlist, args.uris)
    sp.playlist_add_items(playlist, uris)


if __name__ == '__main__':
    main()