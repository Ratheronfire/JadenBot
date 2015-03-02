__author__ = 'David'

import logging
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from jadenbot import generate_sentence, load_config

class JadenBot(irc.bot.SingleServerIRCBot):
    config = dict()

    def __init__(self, channel, nickname, server, config, port=6667):
        irc.client.ServerConnection.buffer_class = irc.buffer.LenientDecodingLineBuffer

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)

        self.channel = channel
        self.config = config

        global jaden_log
        jaden_log = logging.getLogger("jaden")
        logging.basicConfig(filename="jaden.log", level=logging.DEBUG)

        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG)

        logging.getLogger('jaden').addHandler(console_log)

        jaden_log.info("Joining " + channel + " on " + server + ":" + str(port) + " as " + nickname)

    def print_sentence(self, c, e):
        jaden_log.info("Read command " + self.config["command-string"] + " from " + e.source.nick)

        sentence = generate_sentence()
            
        jaden_log.info(sentence)
        c.privmsg(self.channel, sentence)

    def reload_config(self):
        global config

        config = load_config()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        user = e.source.nick

        msg = e.arguments[0]

        if msg == self.config["command-string"]:
            self.print_sentence(c, e)
        elif msg == "!reload":
            self.reload_config()
        elif msg.lower() == "jadenbot die":
            jaden_log.info("Read exit command from " + user)
            if user.lower() in self.config["bot-ops"]:
                jaden_log.info("Exiting now.")
                self.die()
            else:
                jaden_log.warning(user + " is not authorized to kill bot.")
                c.privmsg(self.channel, "JadenBot never dies")
    
    def on_privmsg(self, c, e):
        msg = e.arguments[0]
        msg_words = msg.split()
        command = msg_words[0]

        user = e.source.nick

        if user.lower() in self.config["bot-ops"]:
            jaden_log.info("Authorized user " + user + " issued private command " + msg)
            if command == "!say":
                c.privmsg(self.channel, msg.replace("!say ", ""))
            elif command == "!reload":
                self.reload_config()
            elif command == "!jaden":
                self.print_sentence(c, e)
            elif command == "!quit":
                jaden_log.info("Exiting now.")
                self.die()
            else:
                jaden_log.debug("Unrecognized command.")
                c.privmsg(user, "Unrecognized command.")
        else:
            jaden_log.warning("Unauthorized user " + user + " issued private command " + msg)
