"""
test/test_readings

Ensures that readings.py
properly converts kana to roumanji
and vice versa

Will not work unless you are in the outer
KanaKing directory.
"""
# pylint: disable=unused-import

from __future__ import annotations
import sys
import os
import pytest

root_dir = os.getcwd()
if os.name == "nt":
    sys.path.insert(1, root_dir+"\\src")
else:
    sys.path.insert(1, root_dir+"/src")



# pylint: disable=wrong-import-position
from src import readings



class TestHiragana:
    """
    Tests the ability of the readings module
    to make transliterations to and from
    hiragana and romaji
    """
    def test_hiragana_to_romaji(self):
        """
        Tests the ability of the readings module
        to convert between hiragana and romanized
        Japanese
        """

        # Basic cases
        assert readings.convert_h_to_r("いいえ") == "iie"
        assert readings.convert_h_to_r("かさ") == "kasa"
        assert readings.convert_h_to_r("ください") == "kudasai"
        assert readings.convert_h_to_r("おはよう") == "ohayou"

        # Y-combo words
        assert readings.convert_h_to_r("びょういん") == "byouin"
        assert readings.convert_h_to_r("しょく") == "shoku"
        assert readings.convert_h_to_r("しゃしん") == "shashin"
        assert readings.convert_h_to_r("じゃないです") == "janaidesu"
        assert readings.convert_h_to_r("おちゃ") == "ocha"
        assert readings.convert_h_to_r("りゅうがくせい") == "ryuugakusei"

        # Doubled syllables
        assert readings.convert_h_to_r("かっこいい") == "kakkoii"
        assert readings.convert_h_to_r("じゃなかったです") == "janakattadesu"
        assert readings.convert_h_to_r("いらっしゃいませ") == "irasshaimase"



    def test_romaji_to_hiragana(self):
        """
        Tests the ability of the readings module
        to convert between romanized Japanese (romaji)
        and hiragana
        """
        # Basic cases
        assert readings.convert_r_to_h("iie") == "いいえ"
        assert readings.convert_r_to_h("kasa") == "かさ"
        assert readings.convert_r_to_h("kudasai") == "ください"
        assert readings.convert_r_to_h("ohayou") == "おはよう"

        # Y-combo words
        assert readings.convert_r_to_h("byouin") == "びょういん"
        assert readings.convert_r_to_h("shoku") == "しょく"
        assert readings.convert_r_to_h("shashin") == "しゃしん"
        assert readings.convert_r_to_h("janaidesu") == "じゃないです"
        assert readings.convert_r_to_h("ocha") == "おちゃ"
        assert readings.convert_r_to_h("ryuugakusei") == "りゅうがくせい"

        # Doubled syllables
        assert readings.convert_r_to_h("kakkoii") == "かっこいい"
        assert readings.convert_r_to_h("janakattadesu") == "じゃなかったです"
        assert readings.convert_r_to_h("irasshaimase") == "いらっしゃいませ"



class TestKatakana:
    """
    Tests the ability of the readings module
    to make transliterations to and from
    katakana and romaji
    """

    def test_katakana_to_romaji(self):
        """
        Tests the ability of the readings module
        to convert between katakana
        and romanized Japanese (romaji)
        """
        # Basic cases
        assert readings.convert_k_to_r("カメ") == "kame"
        assert readings.convert_k_to_r("バナナ") ==  "banana"
        assert readings.convert_k_to_r("ペン") == "pen"

        # Y-combo words
        assert readings.convert_k_to_r("キュウリ") == "kyuuri"
        assert readings.convert_k_to_r("ジョギング") ==  "jogingu"
        assert readings.convert_k_to_r("ジャスミン") == "jasumin"

        # Long vowels
        assert readings.convert_k_to_r("コーヒー") == "koohii"
        assert readings.convert_k_to_r("ミーティング") == "miitingu"
        assert readings.convert_k_to_r("セーター") == "seetaa"

        # Doubled syllables
        assert readings.convert_k_to_r("スッポン") == "suppon"
        assert readings.convert_k_to_r("クッキー") ==  "kukkii"
        assert readings.convert_k_to_r("パッケージ") == "pakkeeji"

        # Special Combinations
        assert readings.convert_k_to_r("ヴァイオリン") == "vaiorin"
        assert readings.convert_k_to_r("ファンタジー") == "fantajii"
        assert readings.convert_k_to_r("チェス") == "chesu"
        assert readings.convert_k_to_r("ティーン") == "tiin"
        assert readings.convert_k_to_r("サーフィン") == "saafin"


    def test_romaji_to_katakana(self):
        """
        Tests the ability of the readings module
        to convert between romanized Japanese (romaji)
        and katakana
        """
        # Basic cases
        assert readings.convert_r_to_k("kame") == "カメ"
        assert readings.convert_r_to_k("banana") ==  "バナナ"
        assert readings.convert_r_to_k("pen") == "ペン"

        # Y-combo words
        assert readings.convert_r_to_k("jogingu") ==  "ジョギング"
        assert readings.convert_r_to_k("jasumin") == "ジャスミン"

        # Long vowels
        assert readings.convert_r_to_k("koohii") == "コーヒー"
        assert readings.convert_r_to_k("miitingu") == "ミーティング"
        assert readings.convert_r_to_k("seetaa") == "セーター"

        # Doubled syllables
        assert readings.convert_r_to_k("suppon") == "スッポン"
        assert readings.convert_r_to_k("kukkii") ==  "クッキー"
        assert readings.convert_r_to_k("pakkeeji") == "パッケージ"

        # Special Combinations
        assert readings.convert_r_to_k("vaiorin") == "ヴァイオリン"
        assert readings.convert_r_to_k("fantajii") == "ファンタジー"
        assert readings.convert_r_to_k("chesu") == "チェス"
        assert readings.convert_r_to_k("tiin") == "ティーン"
        assert readings.convert_r_to_k("saafin") == "サーフィン"

