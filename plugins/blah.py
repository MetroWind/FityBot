# -*- coding: utf-8; -*-
"""Enables Fity to say silly stuff.  Just say silly stuff to Fity."""

import random

BLAHFILE = "/home/corsair/.supybot/data/blah.txt"

def on_pubmsg(bot, event):
    if bot.getNick(event) == bot.Nick:
        BlahFile = open(BLAHFILE, 'r')
        Blahs = [line.strip() for line in BlahFile.readlines()]
        BlahFile.close()
        if len(Blahs) == 0:
            bot.reply(event, "I don't know any blah!")
            return
        tokens = bot.getMsg(event)
        GoodBlahs = filter(lambda x : x.find(tokens) != -1, Blahs)
        if len(GoodBlahs) == 0:
            bot.reply(event, random.choice(Blahs))
        else:
            bot.reply(event, random.choice(GoodBlahs))
    return

def on_privmsg(bot, event):
    BlahFile = open(BLAHFILE, 'r')
    Blahs = [line.strip() for line in BlahFile.readlines()]
    BlahFile.close()
    if len(Blahs) == 0:
        bot.reply(event, "I don't know any blah!")
        return
    tokens = bot.getMsg(event)
    GoodBlahs = filter(lambda x : x.find(tokens) != -1, Blahs)
    if len(GoodBlahs) == 0:
        bot.reply(event, random.choice(Blahs))
    else:
        bot.reply(event, random.choice(GoodBlahs))
    return
