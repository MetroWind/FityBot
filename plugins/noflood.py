# -*- coding: utf-8; -*-
"""Warn someone when he is flooding."""

import time
import random

THRESHOLD_TIME = 2.0
THRESHOLD_MSG = 8

REPLY=["我要被淹死了！", "小心 op 来 T 你！！", "我靠... 灌水啊..."]

LastNick = ""
AlreadySaid = 0
FirstTime = 0

class CFloodData:
    def __init__(self, nick):
        self.FirstTime = time.time()
        self.AlreadySaid = 1;
        self.Nick = nick
    def __str__(self):
        return "%s's first time was %f, AlreadySaid %d msgs." % \
               (self.Nick, self.FirstTime, self.AlreadySaid)
    def said(self):
        Now = time.time()
        if Now - self.FirstTime <= THRESHOLD_TIME:
            if self.AlreadySaid == THRESHOLD_MSG - 1:
                self.AlreadySaid = 1
                self.FirstTime = Now
                return True             # It's a flood
            else:
                self.AlreadySaid += 1
        else:                           # reset everything
            self.AlreadySaid = 1
            self.FirstTime = Now
        return False                    # nothing happens

Chatters = {}

def antiFlood(bot, event):
    bot.reply(event, random.choice(REPLY))
    return

def on_pubmsg(bot, event):
    Nick = bot.getSource(event)
    if Nick in Chatters:
        if Chatters[Nick].said():
            antiFlood(bot, event)
            bot.logTerm(Nick + " flooded.")
    else:
        Chatters[Nick] = CFloodData(Nick)
