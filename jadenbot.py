__author__ = 'David'
# test
import json
import os
import traceback
import sys
from wordnik import *
from urllib2 import HTTPError

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

def main():
	load_config()

	global parts_of_speech
	parts_of_speech = config["parts-of-speech"]

	for part in parts_of_speech:
		word = get_word(part)
		if word is not None:
			print part, word

if __name__ == "__main__":
	main()
