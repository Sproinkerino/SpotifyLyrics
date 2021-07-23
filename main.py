from lyrics import  Lyrics
import time

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = "20940ca7312e480b9aaf33f3efd11aa8"
os.environ["SPOTIPY_CLIENT_SECRET"] = "615a1e40381d43e287bd25b84546ce8b"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"


def get_spotify_current():
    scope = "user-read-currently-playing"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_playing_track()
    song_name = results['item']['name']
    artist = results['item']['artists'][0]['name']
    search = song_name + ', ' + artist
    return search, results['progress_ms'] *1.0 / 1000

class LyricTimer:
    def __init__(self):

        pass

    def print_song(self, song_name, progress = 0):
        lrc = Lyrics().run(song_name)
        if lrc is not None:
            time_list , lyric_list = self.parse_lyrics(lrc)
        print(song_name)
        pp = progress
        tt = 0
        first = True
        for i in range(0, len(time_list)):
            time_paused = time_list[i]
            tt = tt + time_paused

            if tt >= pp:
                if first:
                    time.sleep(max(time_list[i] - (tt-pp), 0))
                else:
                    time.sleep(max(time_list[i], 0))
                print((lyric_list[i]))
            first = False



    def parse_lyrics(self, lrc):
        lrc_list = lrc.split('\n')[2:]
        time_list = []
        lyrics_list = []
        tf = 0
        pt = 0
        for x in lrc_list:
            if len(x) > 11:
                t = x[0:11]

                tf= int(t[1:3]) * 60 * 1000 + int(t[4:6])  * 1000 +  int(t[7:10])

                time_list.append((tf - pt)*1.0 / 1000)

                lyrics_list.append(x[11:])
                pt = tf

        return time_list, lyrics_list

if __name__ == '__main__':
    # while True:
    song_name, progress= get_spotify_current()
    LyricTimer().print_song(song_name, progress)