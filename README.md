Takes my Japanese youtube music playlist and creates a spotify playlist out of it

    uses youtube & spotify API (via spotipy)
    uses Cutlet python library to convert the hiragana, katakana, and kanji to romanji for easier spotify searches

installations:

    pip install -r requirements.txt
    pip install fugashi[unidic]
    python -m unidic download
    pip install fugashi[unidic-lite]
    pip install unidic-lite
    pip install cutlet
    pip install --upgrade google-api-python-client
    pip install --upgrade google-auth-oauthlib google-auth-httplib2
    pip install spotipy

NOTES:

    user must input their own spotify client Id, spotify client Secret, youtube channel Id, and youtube playlist name they are reading from
    cutlet doesn't work on windows because it cannot build wheels, would recommend using an Ubuntu VM

to run: python3 playlistConverter.py -p "{name of the playlist that will be created in spotify}"
