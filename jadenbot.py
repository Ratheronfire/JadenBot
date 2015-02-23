__author__ = 'David'

import requests
import json
import os

config = dict()

def load_config():
    if os.access("config.json", os.F_OK):
        with open("config.json", "r", encoding="utf8") as config_file:
            config = json.load(config_file)

    return config

def send_get_request(url):
    response_json = dict()

    try:
        response_json = requests.get(url).json()
    except Exception as e:
        print("Error trying to send GET request for {0}\n Error {1} - {2}".format(url, type(e), e.args))

    return response_json

def get_word(partOfSpeech, minLength, maxLength):
    url = config["base-url"] + "randomWord?hasDictionaryDef=false&includePartOfSpeech=" + partOfSpeech + \
                               "&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1" \
                               "&MinLength=" + str(minLength) + "&maxLength=" + str(maxLength) + "&api_key=" + config["api-key"]

    response = send_get_request(url)

    return response["word"]


def main():
    global config
    config = load_config()
    print(get_word("noun", 5, -1))


if __name__ == "__main__":
    main()