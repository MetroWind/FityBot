# -*- coding: utf-8; -*-
"""Greet people every time they come online."""
import random

GREETINGS = {"SteamedFish": ["今天潜水吧，别老当水王了。", "Hi~~  吃了么？", "来肯德基看我吧。", "水水更健康~~"],
             "nico65": ["又来调戏 bot 了^^"]}

def on_join(bot, event):
    Nick = bot.getSource(event)
    if Nick in GREETINGS:
        bot.replyChannel(event, random.choice(GREETINGS[Nick]))
        bot.logTerm("Hello to " + Nick)
    return
