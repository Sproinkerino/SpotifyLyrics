from lyrics import Lyrics
import time
import textwrap
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from color_config import *
os.environ["SPOTIPY_CLIENT_ID"] = "20940ca7312e480b9aaf33f3efd11aa8"
os.environ["SPOTIPY_CLIENT_SECRET"] = "615a1e40381d43e287bd25b84546ce8b"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"
from datetime import datetime


def get_spotify_current():
    scope = "user-read-currently-playing"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_playing_track()
    song_name = results['item']['name']
    artist = results['item']['artists'][0]['name']
    search = song_name + ', ' + artist
    return search, results['progress_ms'] * 1.0 / 1000 ,results['item']['duration_ms'] * 1.0/1000


class LyricTimer:
    def __init__(self):
        self.starttime = datetime.now()
        pass

    def print_song(self, song_name, progress=0, duration =0):
        print("Searching Lyrics")
        lrc = Lyrics().run(song_name)
        # delay = 5
        song_name, progress, duration = get_spotify_current()
        print(progress)

        if lrc is not None:
            time_list, lyric_list = self.parse_lyrics(lrc)
            first = True
            delay = (datetime.now() - self.starttime).microseconds / 1000000
            delay = 0

            progress = progress + delay


            pp = progress
            tt = 0

            for i in range(0, len(time_list)):
                time_paused = time_list[i]
                tt = tt + time_paused


                if tt >= pp:
                    if first:
                        first = False
                        time.sleep(max((tt - pp) , 0))
                    else:
                        time.sleep(max(time_list[i], 0))
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"{On_Blue}" + song_name + " " + f"{Color_Off}" + "\n")
                    #os.system('clear')
                    if (i -1) >= 0:
                        print('\n' + textwrap.fill(lyric_list[i -1], 30) + "\n")
                    print(f"{Red}"+textwrap.fill(lyric_list[i], 30) + f"{Color_Off}" )
                    if (i + 1) <= (len(lyric_list) - 1):
                        print('\n' + textwrap.fill(lyric_list[i + 1], 20))
                    # if (i + 2) <= (len(lyric_list) - 2):
                    #     print('\n' + textwrap.fill(lyric_list[i + 1], 20))

            time.sleep(duration - tt)
        else:
            print("Lyrics not found.")
            time.sleep(10)

    def parse_lyrics(self, lrc):
        lrc_list = lrc.split('\n')[2:]
        time_list = []
        lyrics_list = []
        tf = 0
        pt = 0
        for x in lrc_list:
            if len(x) > 11:
                t = x[0:11]
                a = t.split(':')[0][1:]
                b = t.split(':')[1].split('.')[0]
                c = t.split(':')[1].split('.')[1].split(']')[0]
                tf = int(a) * 60 * 1000 + int(b) * 1000 + int(c)

                time_list.append((tf - pt) * 1.0 / 1000)

                lyrics_list.append(x.split(']')[1])
                # lyrics_list.append(x)
                pt = tf

        return time_list, lyrics_list


if __name__ == '__main__':
    while True:
        print("Query Spotify...")
        song_name, progress , duration = get_spotify_current()
        LyricTimer().print_song(song_name, progress, duration)
        time.sleep(0.5)

