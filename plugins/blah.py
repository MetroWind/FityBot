# -*- coding: utf-8; -*-
"""Enables Fity to say silly stuff.  Just say silly stuff to Fity."""

import random

BLAHFILE = "blah.txt"

def on_pubmsg(bot, event):
    if bot.getNick(event) == bot.Nick:
        with open(BLAHFILE, 'r') as BlahFile:
            Blahs = [line.strip() for line in BlahFile]

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
    with open(BLAHFILE, 'r') as BlahFile:
        Blahs = [line.strip() for line in BlahFile]

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

def cmdAddBlah(bot, event, args):
    """Teach Fity to say something.  Usage: addblah SOMETHING.
    """
    NewBlah = ' '.join(args)
    if NewBlah:
        with open(BLAHFILE, 'a') as BlahFile:
            BlahFile.write(NewBlah)
            BlahFile.write('\n')
    return
