import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.create_playlist')
logging.basicConfig(level='DEBUG')


def get_args():
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlists')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    return parser.parse_args()


def main():
    args = get_args()
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   client_id="c23b1f6bf08b432ba41e399c5875041d",
                                                   client_secret="6f5e550b3da546b89769447f743187b7",
                                                   redirect_uri="http://localhost:3000"))
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, args.playlist)


if __name__ == '__main__':
    main()