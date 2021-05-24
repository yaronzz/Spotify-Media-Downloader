#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   2.1
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import logging
import os
import requests
import prettytable
import ssl
import sys
import getopt
import time
import aigpy

from spotifyyy_dl.spotify import SpotifyAPI
from spotifyyy_dl.settings import Settings, TokenSettings, getLogPath
from spotifyyy_dl.printf import Printf, VERSION
from spotifyyy_dl.download import start
from spotifyyy_dl.enum import AudioQuality
from spotifyyy_dl.lang.language import getLang, setLang, initLang, getLangChoicePrint

ssl._create_default_https_context = ssl._create_unverified_context

API = SpotifyAPI()
CONF = Settings.read()
LANG = initLang(CONF.language)

logging.basicConfig(filename=getLogPath(),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def changeSettings():
    global LANG
    Printf.settings(CONF)
    choice = Printf.enter(LANG.CHANGE_START_SETTINGS)
    if choice == '0':
        return

    CONF.downloadPath = Printf.enterPath(LANG.CHANGE_DOWNLOAD_PATH, LANG.MSG_PATH_ERR, '0', CONF.downloadPath)
    CONF.audioQuality = AudioQuality(int(Printf.enterLimit(
        LANG.CHANGE_AUDIO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    # CONF.videoQuality = AudioQuality(int(Printf.enterLimit(
        # LANG.CHANGE_VIDEO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    # CONF.onlyM4a = Printf.enter(LANG.CHANGE_ONLYM4A) == '1'
    CONF.checkExist = Printf.enter(LANG.CHANGE_CHECK_EXIST) == '1'
    # CONF.includeEP = Printf.enter(LANG.CHANGE_INCLUDE_EP) == '1'
    CONF.saveCovers = Printf.enter(LANG.CHANGE_SAVE_COVERS) == '1'
    CONF.showProgress = Printf.enter(LANG.CHANGE_SHOW_PROGRESS) == '1'
    CONF.language = Printf.enter(LANG.CHANGE_LANGUAGE + "(" + getLangChoicePrint() + "):")
    CONF.albumFolderFormat = Printf.enterFormat(
        LANG.CHANGE_ALBUM_FOLDER_FORMAT, CONF.albumFolderFormat, Settings.getDefaultAlbumFolderFormat())
    CONF.trackFileFormat = Printf.enterFormat(LANG.CHANGE_TRACK_FILE_FORMAT,
                                              CONF.trackFileFormat, Settings.getDefaultTrackFileFormat())

    LANG = setLang(CONF.language)
    Settings.save(CONF)


def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvl:o:q:r:", ["help", "version",
                                                                "link=", "output="])
    except getopt.GetoptError as errmsg:
        Printf.err(vars(errmsg)['msg'] + ". Use 'qobuzzz-dl -h' for useage.")
        return

    link = None
    for opt, val in opts:
        if opt in ('-h', '--help'):
            Printf.usage()
            continue
        if opt in ('-v', '--version'):
            Printf.logo()
            continue
        if opt in ('-l', '--link'):
            link = val
            continue
        if opt in ('-o', '--output'):
            CONF.downloadPath = val
            Settings.save(CONF)
            continue

    if not aigpy.path.mkdirs(CONF.downloadPath):
        Printf.err(LANG.MSG_PATH_ERR + CONF.downloadPath)
        return

    if link is not None:
        Printf.info(LANG.SETTING_DOWNLOAD_PATH + ':' + CONF.downloadPath)
        start(CONF, link)


def main():
    if len(sys.argv) > 1:
        mainCommand()
        return

    Printf.logo()
    Printf.settings(CONF)

    # onlineVer = aigpy.pip.getLastVersion('qobuzzz-dl')
    # if not aigpy.string.isNull(onlineVer):
    #     icmp = aigpy.system.cmpVersion(onlineVer, VERSION)
    #     if icmp > 0:
    #         Printf.info(LANG.PRINT_LATEST_VERSION + ' ' + onlineVer)

    while True:
        Printf.choices()
        choice = Printf.enter(LANG.PRINT_ENTER_CHOICE)
        if choice == "0":
            return
        elif choice == "1":
            changeSettings()
        else:
            start(CONF, choice)


if __name__ == "__main__":
    main()
    # test example
    # track https://open.spotify.com/track/7gXiPiffMrqPe3Q1vzD6uM'
    # album z2u0t8ukvm5pb https://play.qobuz.com/album/0603497899272
    # artist 167422
    # playlist 1452423
