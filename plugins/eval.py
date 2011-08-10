"""Evaluate a python expression."""

def cmdEval(bot, event, args):
    """Usage: eval CODE"""
    try:
        Result = eval(' '.join(args))
    except:
        bot.reply(event, "Do you really know what you are doing??")
    else:
        bot.reply(event, str(Result))
    return
