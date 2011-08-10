"""Usage: help [stuff]
Simply type "help" for detail."""

def replyMultiLine(bot, event, lines):
    for line in lines.strip().split('\n'):
        bot.reply(event, line)

def cmdHelp(bot, event, args):
    """Usage: help [STUFF]
Simply type "help" for detail."""

    if bot.getCmd(event) != "help":
        return

    Args = bot.getArgs(event)
    if not Args:                   # Just a "help"
        Doc = __doc__
        Cmds = "Available commands: " + ", ".join(bot.Cmds.keys())
        Plugins = "Running plugins: " + ", ".join(bot.Plugins)
        
        replyMultiLine(bot, event, '\n'.join([Doc, Cmds, Plugins]))
        return
    NeedHelp = Args[0]                       # The cmd or plugin that needs help

    Doc = ""

    if NeedHelp in bot.Cmds:
        Doc = bot.Cmds[NeedHelp].__doc__
    elif NeedHelp in bot.Plugins:
        Doc = getattr(bot.PluginsMod, NeedHelp).__doc__
    else:
        Doc = "What the hell is `%s' ?_?" % NeedHelp

    if Doc:
        replyMultiLine(bot, event, Doc)
    else:
        bot.reply(event, "`%s' has no doc available..." % NeedHelp)
