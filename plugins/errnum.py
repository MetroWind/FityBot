"""Let Fity tell you what a specific error number usually means."""

import os
import random

def cmdErrnum(bot, event, args):
    """Usage: errnum NUMBER
Let Fity tell you what error number `NUMBER' usually means.
    """
    if len(args) == 1:
        Error = None
        try:
            Error = os.strerror(int(args[0]))
        except ValueError:
            bot.reply(event, random.choice(["Huh??", "Yo kiddin', right?",
                                            "What are you talking about?",
                                            "You are speaking Martian now."]))
        else:
            bot.reply(event, "Error code %s means '%s'." % (args[0], Error))
    return
