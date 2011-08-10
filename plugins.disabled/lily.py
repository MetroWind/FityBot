# -*- coding: utf-8; -*-

"""Get Lily top ten!"""

import urllib2
import codecs

LILY_BASE = "http://bbs.nju.edu.cn/"

def getTop10Number(line):
    return int(line[26])

def getTop10Url(line):
    return LILY_BASE + line[line.find("bbstcon?board="):
                                line.find('.A">') + 2]

def getTop10Title(line):
    return line[line.find('.A">') + 4:]

def cmdTop10(bot, event, args):
    """Get titles of Lily top ten."""
    try:
        Number = int(args[0])
    except ValueError:
        bot.reply(event, "What were you thinking??!!  Trick me??")
        return 1
    if Number < 1 or Number > 10:
        bot.reply(event, "%d 大？你自己去看吧~~" % Number)
        return 1

    Html = urllib2.urlopen("http://bbs.nju.edu.cn/bbstop10")
    Lines = [line.strip() for line in Html.readlines()]
    Lines = filter(lambda s: s.startswith("<tr "), Lines)[1:]
    GBKDecoder = codecs.getdecoder("gbk")
    UniEncoder = codecs.getencoder("utf_8")
    Lines = [GBKDecoder(line)[0] for line in Lines]
    Lines = [UniEncoder(line)[0] for line in Lines]
    Line = Lines[int(args[0]) - 1]
    bot.reply(event, ' '.join([getTop10Title(Line), getTop10Url(Line)]))
    return 0
