import requests
import json
import re


class Lyrics:
    def __init__(self):
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
            'Refer': 'http://music.163.com',
            'Host': 'music.163.com'
        }
        pass

    def run(self, song):
        id = self.search_id(song)
        if id is None:
            return None
        else:
            lyrics = self.get_lyrics(id)
            return lyrics

        pass

    def search_id(self, song):
        url = 'http://music.163.com/api/search/get?s={}&type=1&limit=1&total=true'.format(song)

        res = requests.get(url, headers=self.headers)
        res = res.json()
        try:
            id = res['result']['songs'][0]['id']
        except:
            return None
        return id

    def get_lyrics(self, id):
        try:
            url = 'http://music.163.com/api/song/lyric?id=' + str(id) + '&lv=1&kv=1&tv=-1'
            res = requests.get(url, headers=self.headers)
            lyric = res.text

            json_obj = json.loads(lyric)

            lyric = json_obj['lrc']['lyric']
        except:
            lyric = None
            pass

        return lyric

