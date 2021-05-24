#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os
import aigpy
import logging
from pytube import YouTube

from spotifyyy_dl.settings import Settings, TokenSettings
from spotifyyy_dl.spotify import SpotifyAPI, MatchTrack
from spotifyyy_dl.enum import Type, AudioQuality
from spotifyyy_dl.printf import Printf
from spotifyyy_dl.model import Album, Track, Artist, Playlist, StreamUrl

API = SpotifyAPI()

def __getIndexStr__(index):
    pre = "0"
    if index < 10:
        return pre+str(index)
    if index < 99:
        return str(index)
    return str(index)


def __getExtension__(url: StreamUrl):
    # if url.format_id == 5:
    return '.mp3'
    # return ".flac"


def __getArtists__(array):
    ret = []
    for item in array:
        ret.append(item.name)
    return ret


def __setMetaData__(track: Track, album: Album, filepath, contributors):
    # obj = aigpy.tag.TagTool(filepath)
    # obj.album = track.album.title
    # obj.title = track.title
    # # obj.artist = __getArtists__(track.performers)
    # obj.copyright = track.copyright
    # obj.tracknumber = track.track_number
    # obj.discnumber = track.media_number
    # obj.composer = track.performers
    # obj.isrc = track.isrc
    # obj.albumartist = __getArtists__(album.artists)
    # obj.date = album.release_date_original
    # obj.totaldisc = album.media_count
    # if obj.totaldisc <= 1:
    #     obj.totaltrack = album.tracks_count
    # coverpath = album.image.large # API.getCoverUrl(album.cover, "1280", "1280")
    # obj.save(coverpath)
    return


# def __convertToM4a__(filepath, codec):
#     if 'ac4' in codec or 'mha1' in codec:
#         return filepath
#     if '.mp4' not in filepath:
#         return filepath
#     newpath = filepath.replace('.mp4', '.m4a')
#     aigpy.path.remove(newpath)
#     os.rename(filepath, newpath)
#     return newpath


def __stripPathParts__(stripped_path, separator):
    result = ""
    stripped_path = stripped_path.split(separator)
    for stripped_path_part in stripped_path:
        result += stripped_path_part.strip()
        if not stripped_path.index(stripped_path_part) == len(stripped_path) - 1:
            result += separator
    return result.strip()


def __stripPath__(path):
    result = __stripPathParts__(path, "/")
    result = __stripPathParts__(result, "\\")
    return result.strip()

# "{ArtistName}/{Flag} [{AlbumID}] [{AlbumYear}] {AlbumTitle}"

def __getAlbumPath__(conf: Settings, album: Album):
    base = conf.downloadPath + '/Album/'
    artist = aigpy.path.replaceLimitChar(album.artists[0].name, '-')
    # album folder pre: [ME][ID]
    flag = ""#API.getFlag(album, Type.Album, True, "")
    if conf.audioQuality != AudioQuality.Master:
        flag = flag.replace("M", "")
    if not conf.addExplicitTag:
        flag = flag.replace("E", "")
    if not aigpy.string.isNull(flag):
        flag = "[" + flag + "] "

    sid = str(album.id)
    #album and addyear
    albumname = aigpy.path.replaceLimitChar(album.name, '-')
    year = ""
    if album.release_date is not None:
        year = aigpy.string.getSubOnlyEnd(album.release_date, '-')
    # retpath
    retpath = conf.albumFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = Settings.getDefaultAlbumFolderFormat()
    retpath = retpath.replace(R"{ArtistName}", artist.strip())
    retpath = retpath.replace(R"{Flag}", flag)
    retpath = retpath.replace(R"{AlbumID}", sid)
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
    retpath = __stripPath__(retpath.strip())
    return base + retpath


def __getPlaylistPath__(conf: Settings, playlist: Playlist):
    # outputdir/Playlist/
    base = conf.downloadPath + '/Playlist/'
    # name
    name = aigpy.path.replaceLimitChar(playlist.name, '-')
    return base + name + '/'

# "{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
def __getTrackPath__(conf: Settings, track: Track, stream: StreamUrl, album: Album=None, playlist: Playlist=None):
    if album is not None:
        base = __getAlbumPath__(conf, album) + '/'
        # if album.media_count > 1:
        #     base += 'CD' + str(track.media_number) + '/'
    # if playlist is not None:
    #     base = __getPlaylistPath__(conf, playlist)
    # number
    number = __getIndexStr__(track.track_number)
    # if playlist is not None:
    #     number = __getIndexStr__(track.trackNumberOnPlaylist)
    # artist
    artist = aigpy.path.replaceLimitChar(track.artists[0].name, '-')
    # title
    title = track.name
    # if not aigpy.string.isNull(track.version):
    #     title += ' (' + track.version + ')'
    title = aigpy.path.replaceLimitChar(title, '-')
    # get explicit
    explicit = ""# "(Explicit)" if conf.addExplicitTag and track.explicit else ''
    #album and addyear
    albumname = aigpy.path.replaceLimitChar(album.name, '-')
    year = ""
    if album.release_date is not None:
        year = aigpy.string.getSubOnlyEnd(album.release_date, '-')
    # extension
    extension = __getExtension__(stream)
    retpath = conf.trackFileFormat
    if retpath is None or len(retpath) <= 0:
        retpath = Settings.getDefaultTrackFileFormat()
    retpath = retpath.replace(R"{TrackNumber}", number)
    retpath = retpath.replace(R"{ArtistName}", artist.strip())
    retpath = retpath.replace(R"{TrackTitle}", title)
    retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
    retpath = retpath.strip()
    return base + retpath + extension


def __isNeedDownload__(path, url):
    curSize = aigpy.file.getSize(path)
    if curSize <= 0:
        return True
    netSize = aigpy.net.getSize(url)
    if curSize >= netSize:
        return False
    return True


# def __downloadTrack__(conf: Settings, track, album=None, playlist=None):
def __downloadTrack__(conf, track, album=None, playlist=None):
    try:
        msg, streams = API.getStreamUrls(track)
        Printf.track(track)
        if not aigpy.string.isNull(msg) or streams is None:
            Printf.err(track.title + "." + msg)
            return
        if len(streams) <= 0:
            Printf.err(track.title + ". streamUrls num is 0.")
            return
        
        bestValue, bestStreams = MatchTrack.getBestMatchItems(track, streams)
        if len(bestStreams) > 0:
            stream = bestStreams[0]
        else:
            Printf.err(track.name + ". not match track.")
            return
        
        Printf.info("Match track:" + stream.name + ('-' + stream.albumName if stream.albumName != '' else ''))
        path = __getTrackPath__(conf, track, stream, album, playlist)
        youtubeHandler = YouTube(stream.link, proxies={
                                 "http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"})
        trackAudioStream = youtubeHandler.streams.filter(only_audio=True).order_by('bitrate').last()

        # check exist
        if conf.checkExist and __isNeedDownload__(path, trackAudioStream.url) == False:
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return
        logging.info("[DL Track] name=" + aigpy.path.getFileName(path) + "\nurl=" + trackAudioStream.url)
        tool = aigpy.download.DownloadTool(path + '.part', [trackAudioStream.url], proxies={
            "http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"})
        check, err = tool.start(conf.showProgress)

        if not check:
            Printf.err("Download failed! " + aigpy.path.getFileName(path) + ' (' + str(err) + ')')
            return
        # encrypted -> decrypt and remove encrypted file
        os.replace(path + '.part', path)

        # path = __convertToM4a__(path, stream.codec)

        __setMetaData__(track, album, path, None)
        Printf.success(aigpy.path.getFileName(path))
        return
    except Exception as e:
        print("Download failed! " + track.name + ' (' + str(e) + ')')


def __downloadCover__(conf, album: Album):
    if album == None:
        return
    path = __getAlbumPath__(conf, album) + '/cover.jpg'
    url = album.images[0].url  # API.getCoverUrl(album.cover, "1280", "1280")
    if url is not None:
        aigpy.net.downloadFile(url, path, 5)


# def __album__(conf, obj: Album):
#     Printf.album(obj)
#     # msg, tracks, videos = API.getItems(obj.id, Type.Album)
#     # if not aigpy.string.isNull(msg):
#     #     Printf.err(msg)
#     #     return
#     tracks = obj.tracks
#     if conf.saveCovers:
#         __downloadCover__(conf, obj)
#     for item in tracks:
#         item.album = obj
#         __downloadTrack__(conf, item, obj)


def __track__(conf, obj):
    # Printf.track(obj)
    msg, album = API.getAlbum(obj.album.id)
    if conf.saveCovers:
        __downloadCover__(conf, album)
    __downloadTrack__(conf, obj, album)


# def __artist__(conf, obj: Artist):
#     # msg, albums = API.getArtistAlbums(obj.id, conf.includeEP)
#     Printf.artist(obj, len(obj.albums))
#     # if not aigpy.string.isNull(msg):
#     #     Printf.err(msg)
#     #     return
#     for item in obj.albums:
#         mag, album = API.getAlbum(item.id)
#         if album is None:
#             album = item.album
#         __album__(conf, album)


# def __playlist__(conf, obj: Playlist):
#     Printf.playlist(obj)
#     # msg, tracks, videos = API.getItems(obj.uuid, Type.Playlist)
#     # if not aigpy.string.isNull(msg):
#     #     Printf.err(msg)
#     #     return
#     tracks = obj.tracks
#     for index, item in enumerate(tracks):
#         mag, album = API.getAlbum(item.album.id)
#         if album is None:
#             album = item.album

#         item.trackNumberOnPlaylist = index + 1
#         __downloadTrack__(conf, item, album, obj)


def __file__(conf, string):
    txt = aigpy.file.getContent(string)
    if aigpy.string.isNull(txt):
        Printf.err("Nothing can read!")
        return
    array = txt.split('\n')
    for item in array:
        if aigpy.string.isNull(item):
            continue
        if item[0] == '#':
            continue
        if item[0] == '[':
            continue
        start(conf, item)


def start(conf, string):
    if aigpy.string.isNull(string):
        Printf.err('Please enter something.')
        return

    strings = string.split(" ")
    for item in strings:
        if aigpy.string.isNull(item):
            continue
        if os.path.exists(item):
            __file__(conf, item)
            return

        msg, etype, obj = API.getByString(item)
        if etype == Type.Null or not aigpy.string.isNull(msg):
            Printf.err(msg + " [" + item + "]")
            return

        # if etype == Type.Album:
        #     __album__(conf, obj)
        if etype == Type.Track:
            __track__(conf, obj)
        # if etype == Type.Artist:
        #     __artist__(conf, obj)
        # if etype == Type.Playlist:
        #     __playlist__(conf, obj)

