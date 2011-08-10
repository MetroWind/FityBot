#!/usr/bin/env python2

import sys,os
import signal
import threading
import time
import fitybot

Channels = {"irc.oftc.net": ["#arch-cn", "#njulug"],}
Servers = Channels.keys()

Bots = []

def main():
    global Bots
    def botExit(signum, frame):
        for Bot in Bots:
            Bot.exit()
        sys.exit(0)

    signal.signal(signal.SIGINT, botExit)

    Threads = []
    for Server in Servers:
        Bot = fitybot.FityBot(Server)
        Bot.connect()
        for Channel in Channels[Server]:
            Bot.join(Channel)
        Thread = threading.Thread(target=Bot.start)
        Thread.start()
        Threads.append(Thread)
        Bots.append(Bot)

    while True:
        time.sleep(10)

    return 0

if __name__ == "__main__":
    sys.exit(main())
