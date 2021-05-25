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
from aigpy.modelHelper import ModelBase


class StreamUrl(ModelBase):
    name = None
    type = None
    artistNames = None
    albumName = None
    length = 0
    link = None
    data = None
    


class Image(ModelBase):
    height = 0
    width = 0
    url = None


class Artist(ModelBase):
    id = 0
    name = None


class Album(ModelBase):
    id = None
    name = None
    total_tracks = 0
    release_date = None
    images = Image()
    artists = Artist()
    tracks = None


class Track(ModelBase):
    id = 0
    name = None
    track_number = 0
    disc_number = 0
    duration_ms = 0
    explicit = False
    album = Album()
    artists = Artist()
    trackNumberOnPlaylist = 0


class Playlist(ModelBase):
    id = None
    name = None
    description = None
    images = Image()
    tracks = None
