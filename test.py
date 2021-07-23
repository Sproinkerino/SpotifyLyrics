#!coding:utf-8
import requests
import json
import re
song_name = 'Lifetime Justin Bieber'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Refer':'http://music.163.com',
    'Host':'music.163.com'
}
url = 'http://music.163.com/api/search/get?s={}&type=1&limit=1'.format(song_name)

res= requests.get(url,headers=headers)
res = res.json()
id = res['results']['songs'][0]['id']

url = 'http://music.163.com/api/song/lyric?id='+str(id)+'&lv=1&kv=1&tv=-1'
res= requests.get(url,headers=headers)
lyric = res.text

json_obj = json.loads(lyric)

lyric = json_obj['lrc']['lyric']



