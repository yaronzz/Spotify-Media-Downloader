#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   language.py
@Time    :   2020/08/19
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

from spotifyyy_dl.lang.english import LangEnglish
from spotifyyy_dl.lang.chinese import LangChinese
from spotifyyy_dl.lang.turkish import LangTurkish
from spotifyyy_dl.lang.italian import LangItalian
from spotifyyy_dl.lang.czech import LangCzech
from spotifyyy_dl.lang.arabic import LangArabic
from spotifyyy_dl.lang.russian import LangRussian
from spotifyyy_dl.lang.filipino import LangFilipino
from spotifyyy_dl.lang.croatian import LangCroatian
from spotifyyy_dl.lang.spanish import LangSpanish
from spotifyyy_dl.lang.portuguese import LangPortuguese
from spotifyyy_dl.lang.ukrainian import  LangUkrainian
from spotifyyy_dl.lang.vietnamese import LangVietnamese
from spotifyyy_dl.lang.french import LangFrench
from spotifyyy_dl.lang.german import LangGerman

LANG = None

def initLang(index):  # 初始化
    global LANG
    return setLang(index)

def setLang(index):
    global LANG
    if str(index) == '0':
        LANG = LangEnglish()
    elif str(index) == '1':
        LANG = LangChinese()
    elif str(index) == '2':
        LANG = LangTurkish()
    elif str(index) == '3':
        LANG = LangItalian()
    elif str(index) == '4':
        LANG = LangCzech()
    elif str(index) == '5':
        LANG = LangArabic()
    elif str(index) == '6':
        LANG = LangRussian()
    elif str(index) == '7':
        LANG = LangFilipino()
    elif str(index) == '8':
        LANG = LangCroatian()
    elif str(index) == '9':
        LANG = LangSpanish()
    elif str(index) == '10':
        LANG = LangPortuguese()
    elif str(index) == '11':
        LANG = LangUkrainian()
    elif str(index) == '12':
        LANG = LangVietnamese()
    elif str(index) == '13':
        LANG = LangFrench()
    elif str(index) == '14':
        LANG = LangGerman()
    else:
        LANG = LangEnglish()
    return LANG

def getLang():
    global LANG
    return LANG

def getLangName(index):
    if str(index) == '0':
        return "English"
    if str(index) == '1':
        return "中文"
    if str(index) == '2':
        return "Turkish"
    if str(index) == '3':
        return "Italian"
    if str(index) == '4':
        return "Czech"
    if str(index) == '5':
        return "Arabic"
    if str(index) == '6':
        return "Russian"
    if str(index) == '7':
        return "Filipino"
    if str(index) == '8':
        return "Croatian"
    if str(index) == '9':
        return "Spanish"
    if str(index) == '10':
        return "Portuguese"
    if str(index) == '11':
        return "Ukrainian"
    if str(index) == '12':
        return "Vietnamese"
    if str(index) == '13':
        return "French"
    if str(index) == '14':
        return "German"
    return ""

def getLangChoicePrint():
    array = []
    index = 0
    while True:
        name = getLangName(index)
        if name == "":
            break
        array.append('\'' + str(index) + '\'-' + name)
        index += 1
    return ','.join(array)
