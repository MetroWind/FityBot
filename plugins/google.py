# -*- coding: utf-8; -*-
"""Let Fity google it for you."""

import urllib
import urllib2
import json

API_BASE = "http://ajax.googleapis.com/ajax/services/search/web"

def queryURL(query):
    return '?'.join([API_BASE, urllib.urlencode(query)])

def googleQuery(text):
    Url = queryURL({'v': "1.0", 'q': text})
    Req = urllib2.Request(Url)
    Opener = urllib2.build_opener()
    Data = json.loads(Opener.open(Req).read())
    return Data["responseData"]["results"]

def cmdGoogle(bot, event, args):
    """Do a google search
    """
    Results = googleQuery(' '.join(args))
    for entry in Results:
        bot.reply(event, entry["url"])
    return 0

def cmdLucky(bot, event, args):
    """Do a google lucky search
    """
    bot.reply(event, googleQuery(' '.join(args))[0]["url"])
    return 0
