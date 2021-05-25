#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
'''
import os
import json
import base64
import aigpy
from aigpy.modelHelper import ModelBase

def __encode__(string):
    sw = bytes(string, 'utf-8')
    st = base64.b64encode(sw)
    return st

def __decode__(string):
    try:
        sr = base64.b64decode(string)
        st = sr.decode()
        return st
    except:
        return string

def getSettingsPath():
    if "XDG_CONFIG_HOME" in os.environ:
        return os.environ['XDG_CONFIG_HOME']
    elif "HOME" in os.environ: 
        return os.environ['HOME']
    else:
        return os.path._getfullpathname("./")

def getLogPath():
    return getSettingsPath() + '/.spotifyyy-dl.log'


class Settings(ModelBase):
    ytbProxy = ""
    downloadPath = "./download/"
    onlyM4a = False
    addExplicitTag = True
    addHyphen = True
    addYear = False
    useTrackNumber = True
    checkExist = True
    artistBeforeTitle = False
    includeEP = True
    addAlbumIDBeforeFolder = False
    saveCovers = True
    language = 0
    usePlaylistFolder = True
    multiThreadDownload = True
    albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    showProgress = True

    @staticmethod
    def getDefaultAlbumFolderFormat():
        return R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"

    @staticmethod
    def getDefaultTrackFileFormat():
        return R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"

    @staticmethod
    def read():
        path = Settings.__getFilePath__()
        txt = aigpy.file.getContent(path, True)
        if txt == "":
            return Settings()
        data = json.loads(txt)
        ret = aigpy.model.dictToModel(data, Settings())
        ret.usePlaylistFolder = ret.usePlaylistFolder == True or ret.usePlaylistFolder is None
        ret.multiThreadDownload = ret.multiThreadDownload == True or ret.multiThreadDownload is None
        if ret.albumFolderFormat is None:
            ret.albumFolderFormat = Settings.getDefaultAlbumFolderFormat()
        if ret.trackFileFormat is None:
            ret.trackFileFormat = Settings.getDefaultTrackFileFormat()
        return ret

    @staticmethod
    def save(model):
        data = aigpy.model.modelToDict(model)
        txt = json.dumps(data)
        path = Settings.__getFilePath__()
        aigpy.file.write(path, txt, 'w+')

    @staticmethod
    def __getFilePath__():
        return getSettingsPath() + '/.spotifyyy-dl.json'

