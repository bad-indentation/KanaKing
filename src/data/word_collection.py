"""
Word Collection.


This module is used to collect the vocabulary that will be used to quiz
users.

Words are collected from https://www.jisho.org using requests.

Please use this module responisbly. Do not overload Jisho with high rates
of requests; throttle the rate at which you send requests using time.sleep().
Jisho's robots.txt suggests 40 seconds in between requests
"""

# pylint: disable=import-error
# pylint: disable=wrong-import-position

from __future__ import annotations

import os
import sys
from time import sleep
from bs4 import BeautifulSoup
import requests
from better_profanity import profanity # used for detecting potentially offensive language

# Import fix for importing readings from src
root_dir = os.getcwd()
if os.name == "nt":
    sys.path.insert(1, root_dir+"\\src")
else:
    sys.path.insert(1, root_dir+"/src")

import readings
from errors import TransliterationError

from config.constants import (
    BASIC_HIRAGANA_SYLLABLES,
    DAKUTEN_HIRAGANA_SYLLABLES,
    HANDAKUTEN_HIRAGANA_SYLLABLES,
    ALL_SINGLE_CHAR_HIRAGANA,
    ALL_SINGLE_CHAR_KATAKANA,
    HIRAGANA_DIACRITIC_BINDER,
    KATAKANA_DIACRITIC_BINDER
)

HIRAGANA_MONOSYLLABLES = BASIC_HIRAGANA_SYLLABLES + DAKUTEN_HIRAGANA_SYLLABLES + HANDAKUTEN_HIRAGANA_SYLLABLES
HIRAGANA_WORDLIST = "./src/data/hiragana_wordlist.csv"
KATAKANA_WORDLIST = "./src/data/katakana_wordlist.csv"
REQUEST_DELAY = 40

def parse_wordlist(file: str) -> dict:
    """Parses a wordlist and creates a usable dictionary"""

    lexicon: dict = {}

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            # Grab a new line of word data
            word_data = line.split(",")
            word_data = [word.strip() for word in word_data]

            # Get data from word
            kana_word = word_data[0]
            meaning = word_data[1]

            if len(word_data) >= 4 and word_data[2] == "OVERRIDE_AUTO_READING":
                reading = word_data[3]
            else:
                try:
                    reading = readings.convert_h_to_r(word_data[0])
                except TransliterationError:
                    reading = readings.convert_k_to_r(word_data[0])

            lexicon.update({kana_word: [meaning, reading]})

    return lexicon



def search_char(url: str):
    """Looks for hiragana words in the given url"""
    headers = {"User-Agent":
               "KanaKing, an open-source Japanese learning project."}
    response = requests.get(url, timeout=100, headers=headers)

    reading_list = []
    meaning_list = []

    if response.status_code == 200:
        page = BeautifulSoup(response.text, features="html.parser")

        # Get all words
        words = page.find_all("div", class_="concept_light clearfix")

        for word in words:
            # Get text

            # Essentially, this takes the word, written with both
            # kanji, and the furigana and parses through the word.
            # If it comes across a kanji, it replaces it with the furigana


            # TODO: refactor/improve robustness

            # full word with kanji AND kana
            try:
                full_word = word.find("span", class_="text").text.strip()

                # All of the furigana on top of the kanji
                furigana_tags = word.find("span", class_="furigana")
                furigana = []
                for tag in furigana_tags:
                    furigana.append(str(tag.string))

                while "\n" in furigana:
                    furigana.remove('\n')
                while '' in furigana:
                    furigana.remove('')

                reading = ""
                furigana_iterator = -1
                for char in full_word:
                    if char in ALL_SINGLE_CHAR_HIRAGANA:
                        reading += char
                    else:
                        furigana_iterator += 1
                        try:
                            reading += furigana[furigana_iterator]
                        except IndexError:
                            break

                meaning = word.find("span", class_="meaning-meaning").string.strip()

                meaning = meaning.split(";")[0]

                if not (profanity.contains_profanity(reading) or profanity.contains_profanity(meaning)):
                    reading_list.append(reading)
                    meaning_list.append(meaning)
                    print(reading, meaning)

            except AttributeError:
                pass

    return reading_list, meaning_list


def search_katakana(url: str):
    """Looks for hiragana words in the given url"""
    headers = {"User-Agent":
               "KanaKing, an open-source Japanese learning project."}
    response = requests.get(url, timeout=100, headers=headers)

    reading_list = []
    meaning_list = []

    if response.status_code == 200:

        page = BeautifulSoup(response.text, features="html.parser")

        # Get all words
        words = page.find_all("div", class_="concept_light clearfix")

        for word in words:
            # Get text

            # Essentially, this takes the word, written with both
            # kanji, and the furigana and parses through the word.
            # If it comes across a kanji, it replaces it with the furigana


            # I wrote this code without really knowing what I was doing;
            # I know it's terrible.
            try:
                # full word with kanji AND kana
                full_word = word.find("span", class_="text").text.strip()


                reading = full_word

                meaning = word.find("span", class_="meaning-meaning").string.strip()

                meaning = meaning.split(";")[0]
                print("got a response")
                if not (profanity.contains_profanity(reading) or profanity.contains_profanity(meaning)):
                    reading_list.append(reading)
                    meaning_list.append(meaning)

                    print(reading, meaning)

            except AttributeError:

                print("oops")

    return reading_list, meaning_list





def add_word(file: str, word: str, meaning):
    """Adds a word to the lexicon"""
    with open(file, "a", encoding="utf-8") as f:
        f.write(f"{word}, {meaning}\n")



def get_hiragana():
    """
    Attempts to find new hiragana words to add to the list.
    Checks against duplicates.
    """

    lexicon = list(parse_wordlist(HIRAGANA_WORDLIST).keys())

    for char in HIRAGANA_MONOSYLLABLES:
        urls = [f"https://jisho.org/search/%23jlpt-n{l}%20{char}" for l in range(4, 6)]

        for url in urls:
            sleep(REQUEST_DELAY)
            reading_list, meaning_list = search_char(url)

            for reading, meaning in zip(reading_list, meaning_list):
                try:
                    # Check if the word can be transliterated
                    readings.convert_h_to_r(reading)
                    if reading not in lexicon:
                        lexicon.append(reading)
                        add_word(HIRAGANA_WORDLIST, reading, meaning)


                except (TransliterationError, IndexError):
                    pass


def get_katakana():
    """
    Attempts to find new hiragana words to add to the list.
    Checks against duplicates.
    """
    lexicon = list(parse_wordlist(KATAKANA_WORDLIST).keys())


    for char in ALL_SINGLE_CHAR_KATAKANA:
        sleep(REQUEST_DELAY)
        urls = [f"https://jisho.org/search/%23common%20{char}%20%23words?page={p}"
                for p in range(1,2)]

        for url in urls:
            reading_list, meaning_list = search_katakana(url)

            for reading, meaning in zip(reading_list, meaning_list):
                try:
                    # Check if the word can be transliterated
                    readings.convert_k_to_r(reading)
                    if reading not in lexicon:
                        lexicon.append(reading)
                        add_word(KATAKANA_WORDLIST, reading, meaning)


                except (TransliterationError, IndexError):
                    pass


def get_potential_words(char: str, file: str):
    """
    Finds all of the words containing that
    character in the given file.
    """
    if char in ALL_SINGLE_CHAR_HIRAGANA:
        diacritic_binder = HIRAGANA_DIACRITIC_BINDER
    else:
        diacritic_binder = KATAKANA_DIACRITIC_BINDER


    lexicon = parse_wordlist(file)

    valid_words: dict = {}



    for word in lexicon:
        valid = False
        for kana in word:
            if diacritic_binder.get(kana, kana) == char:
                valid = True

        if valid:
            valid_words.update({word : lexicon[word]})

    return valid_words
