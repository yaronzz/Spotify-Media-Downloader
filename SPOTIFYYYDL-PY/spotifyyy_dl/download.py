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
from spotifyyy_dl.settings import Settings
from spotifyyy_dl.spotify import SpotifyAPI, MatchTrack
from spotifyyy_dl.enum import Type
from spotifyyy_dl.printf import Printf
from spotifyyy_dl.model import Album, Track, Artist, Playlist, StreamUrl

API = SpotifyAPI()
TMPEXT = '.part'

def __getIndexStr__(index):
    pre = "0"
    if index < 10:
        return pre+str(index)
    if index < 99:
        return str(index)
    return str(index)


def __getArtists__(array):
    ret = []
    for item in array:
        ret.append(item.name)
    return ret


def __setMetaData__(track: Track, album: Album, filepath, contributors):
    obj = aigpy.tag.TagTool(filepath)
    obj.album = track.album.name
    obj.title = track.name
    obj.artist = __getArtists__(track.artists)
    # obj.copyright = track.copyright
    obj.tracknumber = track.track_number
    obj.discnumber = track.disc_number
    # obj.composer = track.performers
    # obj.isrc = track.isrc
    obj.albumartist = __getArtists__(album.artists)
    obj.date = album.release_date
    # obj.totaldisc = album.media_count
    # if obj.totaldisc <= 1:
    #     obj.totaltrack = album.tracks_count
    coverpath = album.images[0].url # API.getCoverUrl(album.cover, "1280", "1280")
    obj.save(coverpath)
    return


def __convert__(filepath, codec, bitrate):
    if 'mp4' in codec:
        srcpath = filepath.replace(TMPEXT,'.mp4')
    elif 'webm' in codec:
        srcpath = filepath.replace(TMPEXT, '.webm')
    descpath = filepath.replace(TMPEXT, '')
    
    os.rename(filepath, srcpath)
    
    check, msg = aigpy.ffmpeg.convert(srcpath, descpath, bitrate)
    if check is False:
        Printf.err("Convert failed. " + msg)
        return srcpath
    
    aigpy.path.remove(srcpath)
    return descpath

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
    if not conf.addExplicitTag:
        flag = flag.replace("E", "")
    if not aigpy.string.isNull(flag):
        flag = "[" + flag + "] "

    sid = str(album.id)
    
    #album and addyear
    albumname = aigpy.path.replaceLimitChar(album.name, '-')
    year = "" if album.release_date is None else aigpy.string.getSubOnlyEnd(album.release_date, '-')
    
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
    if playlist is not None:
        base = __getPlaylistPath__(conf, playlist)
    # number
    number = __getIndexStr__(track.track_number)
    if playlist is not None:
        number = __getIndexStr__(track.trackNumberOnPlaylist)
    # artist
    artist = aigpy.path.replaceLimitChar(track.artists[0].name, '-')
    # title
    title = track.name
    # if not aigpy.string.isNull(track.version):
    #     title += ' (' + track.version + ')'
    title = aigpy.path.replaceLimitChar(title, '-')
    # get explicit
    explicit = "(Explicit)" if conf.addExplicitTag and track.explicit else ''
    #album and addyear
    albumname = aigpy.path.replaceLimitChar(album.name, '-')
    year = ""
    if album.release_date is not None:
        year = aigpy.string.getSubOnlyEnd(album.release_date, '-')
    # extension
    extension = ".mp3"
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
    return False

def __getProxy__(conf: Settings):
    if conf.ytbProxy != '':
        return {"http": "http://" + conf.ytbProxy, "https": "http://" + conf.ytbProxy}
    return {}

# def __downloadTrack__(conf: Settings, track, album=None, playlist=None):
def __downloadTrack__(conf, track, album=None, playlist=None):
    try:
        proxies = __getProxy__(conf)
        
        msg, streams = API.getStreamUrls(track, proxies)
        Printf.track(track)
        if not aigpy.string.isNull(msg) or streams is None:
            Printf.err(msg + "({track.name})")
            return
        if len(streams) <= 0:
            Printf.err("StreamUrls num is 0.({track.name})")
            return
        
        bestStreams = MatchTrack.getBestMatchItems(track, streams)
        if len(bestStreams) > 0:
            stream = bestStreams[0]
        else:
            Printf.err("No match track.({track.name})")
            return
        
        Printf.info("Matching track:" + stream.name + ('-' + stream.albumName if stream.albumName != '' else ''))
        path = __getTrackPath__(conf, track, stream, album, playlist)
        ytb = YouTube(stream.link, proxies=proxies)
        ytbStreams = ytb.streams.filter(only_audio=True).order_by('bitrate')
        trackAudioStream = ytbStreams.last()

        # check exist
        if conf.checkExist and __isNeedDownload__(path, trackAudioStream.url) == False:
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return
        # logging.info("[DL Track] name=" + aigpy.getFileName(path) + "\nurl=" + trackAudioStream.url)
        tool = aigpy.download.DownloadTool(path + TMPEXT, [trackAudioStream.url], proxies=proxies)
        check, err = tool.start(conf.showProgress)

        if not check:
            Printf.err("Download failed! " + aigpy.path.getFileName(path) + ' (' + str(err) + ')')
            return
        
        # convert
        path = __convert__(path + TMPEXT, trackAudioStream.mime_type, trackAudioStream.bitrate)

        __setMetaData__(track, album, path, None)
        Printf.success(aigpy.path.getFileName(path))
        return
    except Exception as e:
        print("Download failed! " + track.name + ' (' + str(e) + ')')


def __downloadCover__(conf, album: Album):
    if album is None:
        return
    path = __getAlbumPath__(conf, album) + '/cover.jpg'
    url = album.images[0].url
    if url is not None:
        aigpy.net.downloadFile(url, path, 5)






def __album__(conf, obj: Album):
    Printf.album(obj)
    tracks = obj.tracks
    if conf.saveCovers:
        __downloadCover__(conf, obj)
    for item in tracks:
        item.album = obj
        __downloadTrack__(conf, item, obj)


def __track__(conf, obj):
    msg, album = API.getAlbum(obj.album.id)
    if aigpy.string.isNotNull(msg):
        Printf.err(msg)
    if conf.saveCovers:
        __downloadCover__(conf, album)
    __downloadTrack__(conf, obj, album)


def __artist__(conf, obj: Artist):
    Printf.artist(obj, len(obj.albums))
    for item in obj.albums:
        mag, album = API.getAlbum(item.id)
        if album is None:
            album = item.album
        __album__(conf, album)


def __playlist__(conf, obj: Playlist):
    Printf.playlist(obj)
    tracks = obj.tracks
    for index, item in enumerate(tracks):
        mag, album = API.getAlbum(item.album.id)
        if album is None:
            album = item.album

        item.trackNumberOnPlaylist = index + 1
        __downloadTrack__(conf, item, album, obj)




def __urlsfile__(conf, string):
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
            __urlsfile__(conf, item)
            return

        msg, etype, obj = API.getByString(item)
        if etype == Type.Null or not aigpy.string.isNull(msg):
            Printf.err(msg + " [" + item + "]")
            return

        if etype == Type.Album:
            __album__(conf, obj)
        if etype == Type.Track:
            __track__(conf, obj)
        if etype == Type.Artist:
            __artist__(conf, obj)
        if etype == Type.Playlist:
            __playlist__(conf, obj)

