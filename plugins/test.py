# -*- coding: utf-8; -*-

def cmdTest(bot, event, args):
    """Only Corsair gets to use this one!!!  Hia hia hia~~"""
    print "Source:", event.source()
    print "Target:", event.target()
    print "Command:", bot.getCmd(event)
    print "Arguments:", bot.getArgs(event)
#     bot.reply(event, "Args: " + ' '.join(args))
    return
