#!/usr/bin/env python
# -*- coding: utf-8; -*-

import sys, os
import signal
import glob
import irc
import irc.client as irclib

IGNORE = ["BotFish", "ZFish"]
VERSION = "FityBot by Corsair"

def var2Str(var_name, value):
    return " = ".join([var_name, str(value)])

def event2Str(event):
    """return a string that pretty-print `event'.

    Arguments:
    - `event`: The event to convert.
    """
    return ", ".join([event.eventtype(), var2Str("source", event.source()),
                      var2Str("target", event.target()),
                      var2Str("args", event.arguments())])

class FityBot:
    """The bot."""
    def __init__(self, server="irc.oftc.net", port=6667):
        self.IRC = irclib.IRC()
        self.Connection = self.IRC.server()
        self.IRC.add_global_handler("all_events", self._dispatcher, -1)

        # Load plugins
        self.Plugins = glob.glob("./plugins/*.py")
        self.Plugins = [os.path.basename(path)[:-3] for path in self.Plugins]
        self.OnPubmsg = []
        self.OnPrivmsg = []
        self.OnJoin = []
        self.Cmds = {}
        import plugins
        self.PluginsMod = plugins
        for plugin in self.Plugins:
            self.logTerm("Loading %s..." % plugin)
            exec("import plugins." + plugin)
            try:
                exec(plugin + ".init(self)")
            except: pass
            # Public msg handler
            try:
                exec('self.OnPubmsg.append(plugins.%s.on_pubmsg)' % plugin)
            except:
                pass
            else:
                self.logTerm("  Added pubmsg handler.")
            # Private msg handler
            try:
                exec('self.OnPrivmsg.append(plugins.%s.on_privmsg)' % plugin)
            except:
                pass
            else:
                self.logTerm("  Added privmsg handler.")
            # Join handler
            try:
                exec('self.OnJoin.append(plugins.%s.on_join)' % plugin)
            except:
                pass
            else:
                self.logTerm("  Added join handler.")
            # Load cmds
            exec("Attrs = dir(plugins.%s)" % plugin)
            for attr in Attrs:
                if attr.startswith("cmd"):
                    Cmd = attr[3:].lower()
                    exec("self.Cmds[Cmd] = plugins.%s.%s" % (plugin, attr))
                    self.logTerm("  Added command " + Cmd)

        # Connection parameters
        self.Server = server
        self.Port = port
        self.Nick = "Fity"
        self.Passwd = None
        self.UserName = self.Nick.lower()
        self.IRCName = self.Nick.lower()
        self.LocalAddress = ""
        self.LocalPort = 0
        self.Channel = []

    def connect(self):
        self.logTerm("Connecting to %s..." %
                     ':'.join([self.Server, str(self.Port)]))
        self.Connection.connect(self.Server, self.Port, self.Nick, self.Passwd,
                                self.UserName, self.IRCName, self.LocalAddress,
                                self.LocalPort)

    def getSource(self, event):
        return irclib.nm_to_n(event.source())
    
    def getNick(self, event):
        Msg = event.arguments()[0]
        FirstSpace = Msg.find(' ')
        if FirstSpace != -1 and (Msg[FirstSpace - 1] == ':' or
                                 Msg[FirstSpace - 1] == ','):
            return Msg[:FirstSpace - 1]
        else:
            return None

    def getMsg(self, event):
        Nick = self.getNick(event)
        if Nick == None:
            return event.arguments()[0]
        else:
            return event.arguments()[0][len(Nick) + 2:].strip()

    def getCmd(self, event):
        Msg = self.getMsg(event)
        FirstSpace = Msg.find(' ')
        if FirstSpace == -1:
            if Msg in self.Cmds:
                return Msg
            else: return None
        else:
            Cmd = Msg[:FirstSpace]
            if Cmd in self.Cmds:
                return Cmd
            else:
                return None

    def getArgs(self, event):
        Cmd = self.getCmd(event)
        Msg = self.getMsg(event)
        if Cmd != None:
            return Msg[len(Cmd):].split()
        else:
            return None

    def logTerm(self, text):
        sys.stderr.write(text)
        sys.stderr.write('\n')
        return

    def _dispatcher(self, c, e):
        """[Internal]"""
        m = "_on_" + e.eventtype()
        if hasattr(self, m):
            getattr(self, m)(c, e)
        return

    def _on_privmsg(self, conn, event):
        Cmd = self.getCmd(event)
        if Cmd != None:
            self.logTerm("Executing command %s..." % Cmd)
            self.Cmds[Cmd](self, event, self.getArgs(event))
        else:
            for func in self.OnPrivmsg:
                func(self, event)
        return

    def _on_pubmsg(self, conn, event):
        Nick = self.getNick(event)
        if self.getSource(event) in IGNORE:
            return
        Cmd = self.getCmd(event)
        if Cmd != None and Nick == self.Nick:
            self.logTerm("Executing command %s..." % Cmd)
            self.Cmds[Cmd](self, event, self.getArgs(event))
        else:
            for func in self.OnPubmsg:
                func(self, event)
        return

    def _on_ctcp(self, conn, event):
        CtcpCMD = event.arguments()[0]
        if CtcpCMD == "VERSION":
            conn.ctcp_reply(self.getSource(event), "VERSION " + VERSION)
        return

    def _on_join(self, conn, event):
        for func in self.OnJoin:
            func(self, event)
        return

    def disconnect(self, msg):
        self.Connection.disconnect(msg)
        return

    def join(self, channel):
        """Join a channel."""
        self.logTerm("Joining in %s..." % channel)
        self.Connection.join(channel)
        self.Channel.append(channel)
        return

    def say(self, channel, text):
        """Send message to channel."""
        self.Connection.privmsg(channel, text.decode("utf-8"))
        return

    def msg(self, nick, text):
        """Send message to nick."""
        self.Connection.privmsg(nick, text.decode("utf-8"))
        return

    def replyChannel(self, event, reply):
        Nick = irclib.nm_to_n(event.source())
        Channel = event.target()
        if Nick != None:
            self.say(Channel, ": ".join([Nick, reply]))
        return

    def replyMsg(self, event, reply):
        self.msg(irclib.nm_to_n(event.source()), reply)
        return

    def reply(self, event, text):
        if event.eventtype() == "pubmsg":
            self.replyChannel(event, text)
        elif event.eventtype() == "privmsg":
            self.replyMsg(event, text)
        return

    def start(self):
        """Start the IRC client."""
        self.logTerm("Entering main loop...")
        self.IRC.process_forever()
        return

    def exit(self):
        self.logTerm("SIGINT received, exiting...")
        self.disconnect("Arhhh...")

def main():
    import optparse
    Parser = optparse.OptionParser()
    Parser.add_option("-s", "--server", dest="Server", default="irc.oftc.net",
                      help="Connect SERVER", metavar="SERVER")
    Parser.add_option("-p", "--port", dest="Port", default=6667,
                      help="Using port PORT", metavar="PORT")
    Parser.add_option("-c", "--channel", dest="Channels", default=[],
                      action="append", help="Join CHANNEL after connecting",
                      metavar="CHANNEL")
    (Options, Args) = Parser.parse_args()

    def botExit(signum, frame):
        Bot.exit()

    Bot = FityBot(Options.Server, Options.Port)
    signal.signal(signal.SIGINT, botExit)
    Bot.connect()
    for Cha in Options.Channels:
        Bot.join(Cha)
    Bot.start()
    return 0

if __name__ == "__main__":
    sys.exit(main())
