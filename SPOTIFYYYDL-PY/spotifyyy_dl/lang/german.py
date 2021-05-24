#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   german.py
@Time    :   2021/01/04
@Authors :   Sematre, MineClashTV
@Version :   1.0
@Contact :   
@Desc    :   
'''

class LangGerman(object):
    SETTING = "EINSTELLUNG"
    VALUE = "WERT"
    SETTING_DOWNLOAD_PATH = "Download Pfad"
    SETTING_ONLY_M4A = "mp4 in m4a konvertieren"
    SETTING_ADD_EXPLICIT_TAG = "Explicit Tag hinzufügen"
    SETTING_ADD_HYPHEN = "Bindestrich hinzufügen"
    SETTING_ADD_YEAR = "Jahr vor Album-Ordner hinzufügen"
    SETTING_USE_TRACK_NUM = "Benutzerdefinierte Titelnummer hinzufügen"
    SETTING_AUDIO_QUALITY = "Tonqualität"
    SETTING_VIDEO_QUALITY = "Videoqualität"
    SETTING_CHECK_EXIST = "Existenz überprüfen"
    SETTING_ARTIST_BEFORE_TITLE = "Künstlername vor Songtitel"
    SETTING_ALBUMID_BEFORE_FOLDER = "ID vor Album-Ordner"
    SETTING_INCLUDE_EP = "Einschließlich single&ep"
    SETTING_SAVE_COVERS = "Cover speichern"
    SETTING_LANGUAGE = "Sprache"
    SETTING_USE_PLAYLIST_FOLDER = "Playlist-Ordner verwenden"
    SETTING_MULITHREAD_DOWNLOAD = "Multi-Thread-Download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album-Ordnerformat"
    SETTING_TRACK_FILE_FORMAT = "Track-Dateiformat"
    SETTING_SHOW_PROGRESS = "Fortschritt anzeigen"

    CHOICE = "AUSWAHL"
    FUNCTION = "FUNKTION"
    CHOICE_ENTER = "Mit"
    CHOICE_ENTER_URLID = "'Url/ID' eingeben:"
    CHOICE_EXIT = "Beenden"
    CHOICE_LOGIN = "AccessToken überprüfen"
    CHOICE_SETTINGS = "Einstellungen"
    CHOICE_SET_ACCESS_TOKEN = "AccessToken setzen"
    CHOICE_DOWNLOAD_BY_URL = "Herunterladen per URL oder ID"
    CHOICE_LOGOUT = "Logout"

    PRINT_ERR = "[FEHLER]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[ERFOLG]"

    PRINT_ENTER_CHOICE = "Auswahl:"
    PRINT_LATEST_VERSION = "Neueste Version:"
    PRINT_USERNAME = "Benutzername:"
    PRINT_PASSWORD = "Passwort:"
    
    CHANGE_START_SETTINGS = "Einstellungen starten ('0'-Zurück,'1'-Ja):"
    CHANGE_DOWNLOAD_PATH = "Downloadpfad ('0' nicht ändern):"
    CHANGE_AUDIO_QUALITY = "Tonqualität ('0'-Normal,'1'-Hoch,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Videoqualität ('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "mp4 in m4a konvertieren ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_EXPLICIT_TAG = "Explicit Tag zum Dateiname hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_HYPHEN = "Verwende Bindestriche statt Leerzeichen im Dateinamen ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_YEAR = "Jahr zu Album-Ordnernamen hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_USE_TRACK_NUM = "Titelnummer vor Dateinamen hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_CHECK_EXIST = "Vor dem Download überprüfen, ob die Datei existiert ('0'-Nein,'1'-Ja):"
    CHANGE_ARTIST_BEFORE_TITLE = "Künstlername vor den Songtitel hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_INCLUDE_EP = "Singles und EPs beim Download von Alben eines Künstlers einbeziehen ('0'-Nein,'1'-Ja):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "ID vor Album-Ordner hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_SAVE_COVERS = "Cover speichern ('0'-Nein,'1'-Ja):"
    CHANGE_LANGUAGE = "Sprache auswählen"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album-Ordnerformat('0' überspringen):"
    CHANGE_TRACK_FILE_FORMAT = "Track-Dateiformat('0' überspringen):"
    CHANGE_SHOW_PROGRESS = "Fortschritt anzeigen('0'-Nein,'1'-Ja):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starte Loginprozess..."
    AUTH_LOGIN_CODE = "Dein Logincode ist {}"
    AUTH_NEXT_STEP = "Gehe auf {} in den nächsten {} um das Setup abzuschließen."
    AUTH_WAITING = "Auf Autorisierung warten..."
    AUTH_TIMEOUT = "Zeitüberschreitung der Operation."
    
    MSG_VALID_ACCESSTOKEN = "AccessToken gültig für {}."
    MSG_INVAILD_ACCESSTOKEN = "AccessToken abgelaufen. Versuche zu erneuern."
    MSG_PATH_ERR = "Ungültiger Pfad!"
    MSG_INPUT_ERR = "Eingabefehler!"

    MODEL_ALBUM_PROPERTY = "ALBUM-EIGENSCHAFT"
    MODEL_TRACK_PROPERTY = "TRACK-EIGENSCHAFT"
    MODEL_VIDEO_PROPERTY = "VIDEO-EIGENSCHAFT"
    MODEL_ARTIST_PROPERTY = "KÜNSTLER-EIGENSCHAFT"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-EIGENSCHAFT"

    MODEL_TITLE = 'Titel'
    MODEL_TRACK_NUMBER = 'Titelnummer'
    MODEL_VIDEO_NUMBER = 'Videonummer'
    MODEL_RELEASE_DATE = 'Veröffentlichungsdatum'
    MODEL_VERSION = 'Version'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Name'
    MODEL_TYPE = 'Typ'
