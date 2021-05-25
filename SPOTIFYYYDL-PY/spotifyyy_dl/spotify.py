#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  spotify.py
@Date    :  2021/05/21
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
'''

import re
import base64
import aigpy
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic

from spotifyyy_dl.model import Album, Track, Artist, Playlist, StreamUrl
from spotifyyy_dl.enum import Type


class MatchTrack(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def calcWeight(spotObj: Track, ytObj: StreamUrl) -> int:
        value = 0

        if spotObj.name == ytObj.name:
            value += 40
        else:
            spotName = spotObj.name.lower()
            ytName = ytObj.name.lower()
            if spotName == ytName:
                value += 30
            elif spotName in ytName:
                value += 20
            else:
                punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
                spotName = re.sub(r"[%s]+" % punc, "", spotName)
                ytName = re.sub(r"[%s]+" % punc, "", ytName)
                if spotName in ytName:
                    value += 10

        if value <= 0:
            return 0

        if spotObj.album.name == ytObj.albumName:
            value += 20

        if spotObj.artists[0].name in ytObj.artistNames:
            value += 20
        elif spotObj.artists[0].name.lower() == ytObj.artistNames.lower():
            value += 10
        elif spotObj.artists[0].name.lower() == ytObj.name.lower():
            value += 5

        spotDur = spotObj.duration_ms / 1000
        if abs(spotDur - ytObj.length) < 1:
            value += 10

        return value

    @staticmethod
    def getBestMatchItems(spotObj: Track, streamUrls: list) -> (list):
        bestValue = 0
        array = []
        for item in streamUrls:
            value = MatchTrack.calcWeight(spotObj, item)
            if value <= 0:
                continue
            if len(array) <= 0 or bestValue == value:
                bestValue = value
                array.append(item)
                continue
            if value > bestValue:
                bestValue = value
                array.clear()
                array.append(item)
                continue
        return array


class SpotifyAPI(object):
    def __init__(self):
        self.ytm = YTMusic()

        sid = base64.b64decode("MjhhNmQ1ZWJjZTNhNDAyNGJjNWIwMGFiYjZmOWZkZjg=").decode()
        sec = base64.b64decode("MzkyYjJmNGExMDViNDdmOWFkYTUyMWU0NTg2NDFhZmM=").decode()
        self.auth = SpotifyClientCredentials(client_id=sid,
                                             client_secret=sec)
        self.spotf = spotipy.Spotify(auth_manager=self.auth)

    def __getItems__(self, type: str, id: str = '') -> list:
        offset = 0
        limit = 50
        array = []
        while True:
            if type == "playlist":
                result = self.spotf.playlist_items(id, limit=limit, offset=offset)
            elif type == "album":
                result = self.spotf.album_tracks(id, limit=limit, offset=offset)
            elif type == "artist":
                result = self.spotf.artist_albums(id, limit=limit, offset=offset)

            items = result['items']
            for item in items:
                if type == "artist":
                    model = aigpy.model.dictToModel(item, Album())
                else:
                    model = aigpy.model.dictToModel(item, Track())
                array.append(model)

            size = len(items)
            if size < limit:
                break
            offset += limit
        return array

    def getAlbum(self, id):
        try:
            data = self.spotf.album(id)
            model = aigpy.model.dictToModel(data, Album())
            model.tracks = self.__getItems__("album", id)
            return None, model
        except Exception as e:
            return "Get album failed." + str(e), None

    def getPlaylist(self, id):
        try:
            data = self.spotf.playlist(id)
            model = aigpy.model.dictToModel(data, Playlist())
            model.tracks = self.__getItems__("playlist", id)
            return None, model
        except Exception as e:
            return "Get playlist failed." + str(e), None

    def getArtist(self, id):
        try:
            data = self.spotf.artist(id)
            model = aigpy.model.dictToModel(data, Artist())
            model.albums = self.__getItems__("artist", id)
            return None, model
        except Exception as e:
            return "Get artist failed." + str(e), None

    def getTrack(self, id):
        try:
            data = self.spotf.track(id)
            return None, aigpy.model.dictToModel(data, Track())
        except Exception as e:
            return "Get track failed." + str(e), None

    def getStreamUrls(self, track: Track, proxies: dict = {}):
        try:
            searchStr = f'{track.artists[0].name} - {track.name}'

            self.ytm.proxies = proxies
            searchResult = self.ytm.search(searchStr)

            array = []
            for result in searchResult:
                if result['resultType'] in ['song', 'video']:
                    artists = ", ".join(map(lambda a: a['name'], result['artists']))
                    video_id = result['videoId']
                    if video_id is None:
                        return {}
                    obj = StreamUrl()
                    obj.data = result
                    obj.name = result['title']
                    obj.type = result['resultType']
                    obj.artistNames = artists
                    obj.albumName = result['album']['name'] if 'album' in result else ''
                    obj.length = aigpy.time.strToSecond(result['duration'])
                    obj.link = f'https://www.youtube.com/watch?v={video_id}'
                    array.append(obj)

            return '', array
        except Exception as e:
            return "Get stream url failed." + str(e), None

    @staticmethod
    def getArtistsName(artists=[]):
        if artists is None:
            return ""
        array = []
        return " / ".join(array.append(item.name) for item in artists)

    def parseUrl(self, url):
        etype = Type.Null
        sid = ""
        if "spotify.com" not in url:
            return etype, sid

        if 'artist/' in url:
            etype = Type.Artist
        if 'album/' in url:
            etype = Type.Album
        if 'track/' in url:
            etype = Type.Track
        if 'playlist/' in url:
            etype = Type.Playlist

        if etype == Type.Null:
            return etype, sid

        sid = aigpy.string.getSub(url, etype.name.lower() + '/', '?')
        return etype, sid

    def getByString(self, string):
        etype = Type.Null
        obj = None

        if aigpy.string.isNull(string):
            return "Please enter something.", etype, obj
        etype, sid = self.parseUrl(string)
        if aigpy.string.isNull(sid):
            sid = string

        if obj is None and (etype == Type.Null or etype == Type.Track):
            msg, obj = self.getTrack(sid)
        if obj is None and (etype == Type.Null or etype == Type.Album):
            msg, obj = self.getAlbum(sid)
        if obj is None and (etype == Type.Null or etype == Type.Playlist):
            msg, obj = self.getPlaylist(sid)
        if obj is None and (etype == Type.Null or etype == Type.Artist):
            msg, obj = self.getArtist(sid)

        if obj is None or etype != Type.Null:
            return msg, etype, obj
        if obj.__class__ == Album:
            etype = Type.Album
        if obj.__class__ == Artist:
            etype = Type.Artist
        if obj.__class__ == Track:
            etype = Type.Track
        if obj.__class__ == Playlist:
            etype = Type.Playlist
        return msg, etype, obj


# api = SpotifyAPI()
# api.getByString('https://open.spotify.com/track/7gXiPiffMrqPe3Q1vzD6uM')
# msg, obj = api.getArtist("06HL4z0CvFAxyc27GXpf02")
# msg, obj = api.getTrack("2RqL3arTKhlTkJsbLPqLN4")
# msg, array = api.getStreamUrls(obj)

# for item in array:
#     wei = MatchTrack.calcWeight(obj, item)
#     print(item.name + "-" + item.albumName + ":" + str(wei))
# msg, obj = api.getAlbum("6BjUjvxxjrEYDp7jN8XYau")
# msg, obj = api.getPlaylist("2iZIBO5yTorFZnPjNaS1WF")
# msg = 0
