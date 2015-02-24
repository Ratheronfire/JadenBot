__author__ = 'David'

import json
import os
import traceback
import sys
import re
from wordnik import *
from urllib2 import HTTPError
from random import choice

default_config = { "api-key": "", "parts-of-speech": 
	[ "noun", "adjective", "verb", "adverb", "interjection", "pronoun",
	"preposition", "abbreviation", "affix", "article", "auxiliary-verb",
	"conjunction", "definite-article", "family-name", "given-name",
	"idiom", "imperative", "noun-plural", "noun-posessive",
	"past-participle", "phrasal-prefix", "proper-noun",
	"proper-noun-plural", "proper-noun-posessive", "suffix",
	"verb-intransitive", "verb-transitive" ],
	"base-url": "http://api.wordnik.com/v4",
	"min-length": 5, "max-length": 9,
	"min-corpus-count": 5000, "max-corpus-count": -1,
	"sentences":
	[ "How Can [noun] Be [adjective] If Our [noun] Aren't [adjective] ?" ]
}

def prompt_for_api_key():
	print "You must add your own API key from http://developer.wordnik.com" \
	      "under the field 'api-key' to use this program."
	exit(0)

def initialize_config():
	with open("config.json", "w") as config_file:
		json.dump(default_config, config_file, indent=2)

def load_config():
	if os.access("config.json", os.F_OK):
		with open("config.json", "r") as config_file:
			config = json.load(config_file)
	else:
		print "No config file found.  Generating default file in config.json"
		initialize_config()
		prompt_for_api_key()
	
	return config

def init_api():
	if config["api-key"] == "":
		prompt_for_api_key()
	
	return swagger.ApiClient(config["api-key"], config["base-url"])

def get_word(partOfSpeech):
	try:
		response = wordsApi.getRandomWord(includePartOfSpeech=partOfSpeech, \
			minLength=config["min-length"], \
			maxLength=config["max-length"], \
			minCorpusCount=config["min-corpus-count"], \
			maxCorpusCount=config["max-corpus-count"])

		if response is not None:
			return response.word
	except HTTPError:
		print "Error finding word of type " + partOfSpeech
		traceback.print_exc(file=sys.stderr)

	return None

config = load_config()
parts_of_speech = config["parts-of-speech"]
api = init_api()
wordsApi = WordsApi.WordsApi(api)

def generate_sentence():
	words = choice(config["sentences"]).split(' ')
	sentence = ""

	for source_word in words:
		source_word = re.sub("\[|\]", "", source_word)
		if source_word in config["parts-of-speech"]:
			word = get_word(source_word)
			word = word.capitalize()
		else:
			word = source_word
		
		if word in "?!.":
			sentence = sentence.rstrip()
			sentence += word
		else:
			sentence += word + " "
	
	return sentence

def main():
	load_config()

	global parts_of_speech
	parts_of_speech = config["parts-of-speech"]

	print generate_sentence()

if __name__ == "__main__":
	main()
