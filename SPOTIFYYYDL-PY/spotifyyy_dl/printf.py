#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   printf.py
@Time    :   2020/08/16
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import aigpy
import logging
import prettytable
from spotifyyy_dl.lang.language import getLangName, getLang
from spotifyyy_dl.settings import Settings, getSettingsPath
from spotifyyy_dl.model import Album, Track, Playlist, Artist, StreamUrl

__LOGO__ = '''
   _____             __  _ ____                 
  / ___/____  ____  / /_(_) __/_  ____  ____  __
  \__ \/ __ \/ __ \/ __/ / /_/ / / / / / / / / /
 ___/ / /_/ / /_/ / /_/ / __/ /_/ / /_/ / /_/ / 
/____/ .___/\____/\__/_/_/  \__, /\__, /\__, /  
    /_/                    /____//____//____/ 
      
https://github.com/yaronzz/Spotify-Media-Downloader
'''
VERSION = '2021.5.25.0'

class Printf(object):

    @staticmethod
    def logo():
        string = __LOGO__ + '\n                      v' + VERSION
        print(string)
        logging.info(string)

    @staticmethod
    def usage():
        print("=============QOBUZZZ-DL HELP==============")
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green("OPTION"), aigpy.cmd.green("DESC")]
        tb.align = 'l'
        tb.add_row(["-h or --help", "show help-message"])
        tb.add_row(["-v or --version", "show version"])
        tb.add_row(["-o or --output", "download path"])
        tb.add_row(["-l or --link", "url/id/filePath"])
        # tb.add_row(["-q or --quality", "track quality('Normal','High,'HiFi','Master')"])
        # tb.add_row(["-r or --resolution", "video resolution('P1080', 'P720', 'P480', 'P360')"])
        #tb.add_row(["-u or --username", "account-email"])
        #tb.add_row(["-p or --password", "account-password"])
        #tb.add_row(["-a or --accessToken", "account-accessToken"])
        print(tb)

    @staticmethod
    def settings(data:Settings):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green(LANG.SETTING), aigpy.cmd.green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row(["Settings path", getSettingsPath()])
        tb.add_row([LANG.SETTING_DOWNLOAD_PATH, data.downloadPath])
        # tb.add_row([LANG.SETTING_ONLY_M4A, data.onlyM4a])
        # tb.add_row([LANG.SETTING_ADD_EXPLICIT_TAG, data.addExplicitTag])
        # tb.add_row([LANG.SETTING_ADD_HYPHEN, data.addHyphen])
        # tb.add_row([LANG.SETTING_ADD_YEAR, data.addYear])
        # tb.add_row([LANG.SETTING_USE_TRACK_NUM, data.useTrackNumber])
        # tb.add_row([LANG.SETTING_AUDIO_QUALITY, data.audioQuality])
        # tb.add_row([LANG.SETTING_VIDEO_QUALITY, data.videoQuality])
        tb.add_row([LANG.SETTING_CHECK_EXIST, data.checkExist])
        tb.add_row([LANG.SETTING_SHOW_PROGRESS, data.showProgress])
        # tb.add_row([LANG.SETTING_ARTIST_BEFORE_TITLE, data.artistBeforeTitle])
        # tb.add_row([LANG.SETTING_ALBUMID_BEFORE_FOLDER, data.addAlbumIDBeforeFolder])
        # tb.add_row([LANG.SETTING_INCLUDE_EP, data.includeEP])
        tb.add_row([LANG.SETTING_SAVE_COVERS, data.saveCovers])
        tb.add_row([LANG.SETTING_LANGUAGE, getLangName(data.language)])
        tb.add_row([LANG.SETTING_USE_PLAYLIST_FOLDER, data.usePlaylistFolder])
        # tb.add_row([LANG.SETTING_MULITHREAD_DOWNLOAD, data.multiThreadDownload])
        tb.add_row([LANG.SETTING_ALBUM_FOLDER_FORMAT, data.albumFolderFormat])
        tb.add_row([LANG.SETTING_TRACK_FILE_FORMAT, data.trackFileFormat])
        tb.add_row(['Yotube Proxy', data.ytbProxy])
        print(tb)

    @staticmethod
    def choices():
        LANG = getLang()
        print("====================================================")
        tb = prettytable.PrettyTable()
        tb.field_names = [LANG.CHOICE, LANG.FUNCTION]
        tb.align = 'l'
        tb.set_style(prettytable.PLAIN_COLUMNS)
        tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER + " '0':"), LANG.CHOICE_EXIT])
        # tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER + " '1':"), LANG.CHOICE_LOGIN])
        tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER + " '1':"), LANG.CHOICE_SETTINGS])
        # tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER + " '2':"), LANG.CHOICE_LOGOUT])
        # tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER + " '4':"), LANG.CHOICE_SET_ACCESS_TOKEN])
        tb.add_row([aigpy.cmd.green(LANG.CHOICE_ENTER_URLID), LANG.CHOICE_DOWNLOAD_BY_URL])
        print(tb)
        print("====================================================")

    @staticmethod
    def enter(string):
        aigpy.cmd.colorPrint(string, aigpy.cmd.TextColor.Yellow, None)
        ret = input("")
        return ret

    @staticmethod
    def enterPath(string, errmsg, retWord = '0', default = ""):
        LANG = getLang()
        while True:
            ret = aigpy.cmd.inputPath(aigpy.cmd.yellow(string), retWord)
            if ret == retWord:
                return default
            elif ret == "":
                print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterLimit(string, errmsg, limit=[]):
        LANG = getLang()
        while True:
            ret = aigpy.cmd.inputLimit(aigpy.cmd.yellow(string), limit)
            if ret is None:
                print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterFormat(string, current, default):
        ret = Printf.enter(string)
        if ret == '0' or aigpy.string.isNull(ret):
            return current
        if ret.lower() == 'default':
            return default
        return ret

    @staticmethod
    def err(string):
        LANG = getLang()
        print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + string)
        logging.error(string)
    
    @staticmethod
    def info(string):
        LANG = getLang()
        print(aigpy.cmd.blue(LANG.PRINT_INFO + " ") + string)

    @staticmethod
    def success(string):
        LANG = getLang()
        print(aigpy.cmd.green(LANG.PRINT_SUCCESS + " ") + string)

    @staticmethod
    def album(data: Album):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green(LANG.MODEL_ALBUM_PROPERTY), aigpy.cmd.green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.name])
        tb.add_row(["ID", data.id])
        tb.add_row([LANG.MODEL_TRACK_NUMBER, data.total_tracks])
        tb.add_row([LANG.MODEL_RELEASE_DATE, data.release_date])
        # tb.add_row([LANG.MODEL_VERSION, data.version])
        # tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
        print(tb)
        logging.info("====album " + str(data.id) + "====\n" +
                     "title:" + data.name + "\n" + 
                     "track num:" + str(data.total_tracks) + "\n" +
                    #  "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")
        

    @staticmethod
    def track(data:Track):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green(LANG.MODEL_TRACK_PROPERTY), aigpy.cmd.green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.name])
        tb.add_row(["ID", data.id])
        tb.add_row([LANG.MODEL_ALBUM, data.album.name])
        # tb.add_row([LANG.MODEL_VERSION, data.version])
        # tb.add_row(["Max-Q", str(data.maximum_bit_depth) + "-" + str(data.maximum_sampling_rate)])
        # if stream is not None:
            # tb.add_row(["Get-Q", str(stream.bit_depth) + "-" + str(stream.sampling_rate)])
        tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
        print(tb)
        logging.info("====track " + str(data.id) + "====\n" + \
                     "title:" + data.name + "\n" + \
                    #  "version:" + str(data.version) + "\n" + \
                     "==================================")
    
    # @staticmethod
    # def video(data):
    #     LANG = getLang()
    #     tb = prettytable.PrettyTable()
    #     tb.field_names = [aigpy.cmd.green(LANG.MODEL_VIDEO_PROPERTY), aigpy.cmd.green(LANG.VALUE)]
    #     tb.align = 'l'
    #     tb.add_row([LANG.MODEL_TITLE, data.title])
    #     tb.add_row([LANG.MODEL_ALBUM, data.album.title if data.album != None else None])
    #     tb.add_row([LANG.MODEL_VERSION, data.version])
    #     tb.add_row([LANG.MODEL_EXPLICIT, data.explicit])
    #     print(tb)
    #     logging.info("====video " + str(data.id) + "====\n" +
    #                  "title:" + data.title + "\n" +
    #                  "version:" + str(data.version) + "\n" +
    #                  "==================================")

    @staticmethod
    def artist(data:Artist, num):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green(LANG.MODEL_ARTIST_PROPERTY), aigpy.cmd.green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_ID, data.id])
        tb.add_row([LANG.MODEL_NAME, data.name])
        tb.add_row(["Number of albums", num])
        # tb.add_row([LANG.MODEL_TYPE, str(data.type)])
        print(tb)
        logging.info("====artist " + str(data.id) + "====\n" +
                     "name:" + data.name + "\n" +
                     "album num:" + str(num) + "\n" +
                     "==================================")

    @staticmethod
    def playlist(data: Playlist):
        LANG = getLang()
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green(LANG.MODEL_PLAYLIST_PROPERTY), aigpy.cmd.green(LANG.VALUE)]
        tb.align = 'l'
        tb.add_row([LANG.MODEL_TITLE, data.name])
        tb.add_row([LANG.MODEL_TRACK_NUMBER, len(data.tracks)])
        # tb.add_row([LANG.MODEL_VIDEO_NUMBER, data.numberOfVideos])
        print(tb)
        logging.info("====playlist " + str(data.id) + "====\n" +
                     "title:" + data.name + "\n" +
                     "track num:" + str(len(data.tracks)) + "\n" +
                    #  "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")

