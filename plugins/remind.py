# -*- coding: utf-8; -*-
"""Tell someone something when he comes online."""

GET_REMIND = "好，下次我告诉他。"
Reminds = {"target": [["teller", "msg"]]}

def remind(bot, target, reminder, msg):
    bot.msg(target, "%s 让我告诉你 %s" % (reminder, msg))
    return

def on_pubmsg(bot, event):
    Nick = bot.getSource(event)
    if Nick in Reminds:
        for ele in Reminds[Nick]:
            remind(bot, Nick, ele[0], ele[1])
        del Reminds[Nick]
        bot.logTerm("Remind " + Nick)
    return

on_join = on_pubmsg

def cmdRemind(bot, event, args):
    """Usage: remind NICK STUFF
Let Fity say `STUFF' to `NICK' when `NICK' comes online next time."""
    Nick = bot.getSource(event)
    Target = args[0]
    Msg = ' '.join(args[1:])
    if not Target in Reminds:
        Reminds[Target] = [[Nick, Msg]]
    else:
        Reminds[Target].append([Nick, Msg])
    bot.reply(event, GET_REMIND)
    return
