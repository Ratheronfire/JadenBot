__author__ = 'David'

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from jadenbot import generate_sentence

class JadenBot(irc.bot.SingleServerIRCBot):
    config = dict()

    def __init__(self, channel, nickname, server, config, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.config = config

        print "Joining " + channel + " on " + server + ":" + str(port) + " as " + nickname

    def print_sentence(self, c, e):
        print "Read command " + self.config["command-string"] + " from " + e.source.nick

        sentence = generate_sentence()
            
        print(sentence)
        c.privmsg(self.channel, sentence)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        user = e.source.nick

        if msg == self.config["command-string"]:
            self.print_sentence(c, e)
        elif msg.lower() == "jadenbot die":
            print "Read exit command from " + user
            if user.lower() in self.config["bot-ops"]:
                print "Exiting now."
                self.die()
            else:
                print user.nick + " is not authorized to kill bot."
                c.privmsg(self.channel, "JadenBot never dies")
    
    def on_privmsg(self, c, e):
        msg = e.arguments[0]
        msg_words = msg.split()
        user = e.source.nick

        if user.lower() in self.config["bot-ops"]:
            print "Authorized user " + user + " issued private command " + msg
            if msg_words[0] == "!say":
                c.privmsg(self.channel, msg.replace("!say ", ""))
            elif msg_words[0] == "!jaden":
                self.print_sentence(c, e)
            elif msg_words[0] == "!quit":
                print "Exiting now."
                self.die()
            else:
                print "Unrecognized command."
                c.privmsg(user, "Unrecognized command.")
        else:
            print "Unauthorized user " + user + " issued private command " + msg

