#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2020/08/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''


class StreamUrl(object):
    name = None
    type = None
    artistNames = None
    albumName = None
    length = 0
    link = None


class Image(object):
    height = 0
    width = 0
    url = None


class Artist(object):
    id = 0
    name = None


class Album(object):
    id = None
    name = None
    total_tracks = 0
    release_date = None
    images = Image()
    artists = Artist()
    tracks = None


class Track(object):
    id = 0
    name = None
    track_number = 0
    disc_number = 0
    duration_ms = 0
    explicit = False
    album = Album()
    artists = Artist()
    trackNumberOnPlaylist = 0


class Playlist(object):
    id = None
    name = None
    description = None
    images = Image()
    tracks = None
