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
	
	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)
	
	def on_pubmsg(self, c, e):
		if e.arguments[0] == self.config["command-string"]:
			c.notice(e.source.nick, generate_sentence())
