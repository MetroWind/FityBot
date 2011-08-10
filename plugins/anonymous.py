"""Let Fity say what you tell him."""

def cmdSay(bot, event, args):
    """Usage: say TO STUFF
Let Fity say `STUFF'.  `TO' can be a channel or a nick."""
    bot.say(args[0], ' '.join(args[1:]))
    return
