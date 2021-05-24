#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   enum.py
@Time    :   2020/08/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
from enum import Enum


class AudioQuality(Enum):
    Normal = 0
    High = 1
    HiFi = 2
    Master = 3

class Type(Enum):
    Album = 0
    Artist = 1
    Playlist = 2
    Track = 3
    Null = 4
