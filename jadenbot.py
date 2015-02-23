__author__ = 'David'

import json
import os
import traceback
import sys
import re
from wordnik import *
from urllib2 import HTTPError
from random import choice

def load_config():
	if os.access("config.json", os.F_OK):
		with open("config.json", "r") as config_file:
			config = json.load(config_file)
	
	return config

def init_api():
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

	for word in words:
		word = re.sub("\[|\]", "", word)
		if word in config["parts-of-speech"]:
			word = get_word(word)
			word = word.capitalize()
		
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
