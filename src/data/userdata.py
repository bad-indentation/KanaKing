"""
user_data.py

Controls the information the
application stores about the user,
such as their progress on kana.
"""

from __future__ import annotations
from typing import Literal
import os
import sys
# Import fix for importing readings from src
root_dir = os.getcwd()
if os.name == "nt":
    sys.path.insert(1, root_dir+"\\src")
else:
    sys.path.insert(1, root_dir+"/src")

from config.constants import BASIC_HIRAGANA_SYLLABLES, BASIC_KATAKANA_SYLLABLES


HIRAGANA_DATA = "./src/data/hiragana_userdata.csv"
KATAKANA_DATA = "./src/data/katakana_userdata.csv"


def reset_file(file: str, kana_type: Literal["hiragana", "katakana"]):
    """
    Resets the current file to an empty list of
    the characters.
    """

    # Safety net to avoid overriding wordlist files 
    with open(file, "r", encoding="utf-8") as f:
        if len(f.readlines()) > 50:
            raise ValueError(f"Are you sure {file} is the file you want to overwrite?!")


    with open(file, "w", encoding="utf-8") as f:
        if kana_type == "hiragana":
            for syllable in BASIC_HIRAGANA_SYLLABLES:
                f.write(syllable+"\n")
        else:
            for syllable in BASIC_KATAKANA_SYLLABLES:
                f.write(syllable+"\n")


def load_scores(file: str):
    """
    Loads the data from the file in the following format:\n\n
    ```
    {
    \tcharacter: points
    \tcharacter: points
    \tcharacter: points
    \t...
    }
    ```
    Note that the number of "points" a character has is 200 times
    (1 - the user's accurary) plus the average number of seconds
    they spent on each question
    """

    data = {}

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip()) == 1:
                data.update({line[0]:3})
            else:
                char_data = [value.strip() for value in line.strip().split(",")]

                # Data for each character is organized as follows:
                # char, number of incorrect tries, total seconds, total # of tries

                char_data = [int(value) if value.isnumeric() else value for value in char_data]

                score = round((char_data[1] / char_data[3])*200 + (char_data[2] / char_data[3]))

                data.update({line[0]:score})

    return data



def load_data(file: str):
    """
     Loads the data from the file in the following format:\n\n
    ```
    {
    \tcharacter: [number of incorrect tries, total seconds, total num. of tries]
    \tcharacter: [number of incorrect tries, total seconds, total num. of tries]
    \tcharacter: [number of incorrect tries, total seconds, total num. of tries]
    \t...
    }
    ```
    """

    data = {}

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip()) == 1:
                data.update({line[0]:[0, 0, 0]})
            else:
                char_data = [value.strip() for value in line.strip().split(",")]

                # Data for each character is organized as follows:
                # char, number of incorrect tries, total seconds, total # of tries

                char_data = [int(value) if value.isnumeric() else value for value in char_data]

                data.update({line[0]:char_data[1:]})

    return data

def update_data(file: str, char: str, correct: bool, seconds: int):
    """
    Updates the accuracy and time for the given character into the given
    file.
    """
    data = load_data(file)

    char_data = data[char] 

    if not correct:
        char_data[0] += 1

    char_data[1] += seconds
    char_data[2] += 1

    with open(file, "w", encoding="utf-8") as f:
        for entry in data:
            if data[entry] == [0, 0, 0]:
                f.write(entry+"\n")
            else:
                f.write(f"{entry}, {', '.join([str(i) for i in data[entry]])}\n")


# reset_file(HIRAGANA_DATA, "hiragana")
# reset_file(KATAKANA_DATA, "katakana")
