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
                        required=True, help='Track ids')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Playlist to add track to')
    return parser.parse_args()


def main():
    args = get_args_playlistAdd()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                   client_secret="6f5e550b3da546b89769447f743187b7",
                                                   redirect_uri="http://localhost:3000"))
    sp.playlist_add_items(args.playlist, args.uris)


if __name__ == '__main__':
    main()