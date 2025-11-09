"""
config/constants.py

Defines constants to be
used throughout the application
"""


from __future__ import annotations
import json

# Import fix
if __name__ != "__main__":
    import os
    import sys
    root_dir = os.getcwd()
    if os.name == "nt":
        sys.path.insert(1, root_dir+"\\src\\config")
    else:
        sys.path.insert(1, root_dir+"/src/config")

# pylint: disable=import-error, wrong-import-position
import settings



# Initialize character sets

# Note that some fairly rare cases are not represented using this system.


### ROMAJI
BASIC_ROMAJI_SYLLABLES = [
    'a', 'i', 'u', 'e', 'o',
    'ka', 'ki', 'ku', 'ke', 'ko',
    'sa', 'shi', 'su', 'se', 'so',
    'ta', 'chi', 'tsu', 'te', 'to',
    'na', 'ni', 'nu', 'ne', 'no',
    'ha', 'hi', 'fu', 'he', 'ho',
    'ma', 'mi', 'mu', 'me', 'mo',
    'ya', 'yu', 'yo',
    'ra', 'ri', 'ru', 're', 'ro',
    'wa', 'n'
]

DAKUTEN_ROMAJI_SYLLABLES = [
    'ga', 'gi', 'gu', 'ge', 'go',
    'za', 'ji', 'zu', 'ze', 'zo',
    'da', 'de', 'do',
    'ba', 'bi', 'bu', 'be', 'bo'
]

HANDAKUTEN_ROMAJI_SYLLABLES = [
    'pa', 'pi', 'pu', 'pe', 'po'
]


Y_COMBO_ROMAJI = []
for char in ['ky', 'sh', 'ch', 'ny', 'hy', 'my', 'ry', 'gy', 'j', 'by', 'py']:
    Y_COMBO_ROMAJI.extend([char+y_char for y_char in ['a', 'u', 'o']])





### HIRAGANA

BASIC_HIRAGANA_SYLLABLES = [
    'あ', 'い', 'う', 'え', 'お',
    'か', 'き', 'く', 'け', 'こ',
    'さ', 'し', 'す', 'せ', 'そ',
    'た', 'ち', 'つ', 'て', 'と',
    'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ひ', 'ふ', 'へ', 'ほ',
    'ま', 'み', 'む', 'め', 'も',
    'や', 'ゆ', 'よ',
    'ら', 'り', 'る', 'れ', 'ろ',
    'わ', 'ん'
]

DAKUTEN_HIRAGANA_SYLLABLES = [
    'が', 'ぎ', 'ぐ', 'げ', 'ご',
    'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
    'だ', 'で', 'ど',
    'ば', 'び', 'ぶ', 'べ', 'ぼ'
]

HANDAKUTEN_HIRAGANA_SYLLABLES = [
    'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'
]

SMALL_HIRAGANA = ['ゃ', 'ゅ', 'ょ', 'っ']

Y_COMBO_HIRAGANA = []
for char in 'きしちにひみりぎじびぴ':
    Y_COMBO_HIRAGANA.extend([char+y_char for y_char in ['ゃ', 'ゅ', 'ょ']])


### HIRAGANA-ROMAJI CONVERSION
ALL_HIRAGANA_COMPATIBLE_ROMAJI = []
ALL_HIRAGANA_COMPATIBLE_ROMAJI += BASIC_ROMAJI_SYLLABLES + DAKUTEN_ROMAJI_SYLLABLES
ALL_HIRAGANA_COMPATIBLE_ROMAJI += HANDAKUTEN_ROMAJI_SYLLABLES + Y_COMBO_ROMAJI

ALL_HIRAGANA = []
ALL_HIRAGANA += BASIC_HIRAGANA_SYLLABLES + DAKUTEN_HIRAGANA_SYLLABLES
ALL_HIRAGANA += HANDAKUTEN_HIRAGANA_SYLLABLES + Y_COMBO_HIRAGANA

ALL_SINGLE_CHAR_HIRAGANA = BASIC_HIRAGANA_SYLLABLES + DAKUTEN_HIRAGANA_SYLLABLES
ALL_SINGLE_CHAR_HIRAGANA += HANDAKUTEN_HIRAGANA_SYLLABLES + SMALL_HIRAGANA

ROMAJI_TO_HIRAGANA: dict[str, str] = dict(zip(ALL_HIRAGANA_COMPATIBLE_ROMAJI, ALL_HIRAGANA))
HIRAGANA_TO_ROMAJI: dict[str, str] = dict(zip(ALL_HIRAGANA, ALL_HIRAGANA_COMPATIBLE_ROMAJI))


### KATAKANA

BASIC_KATAKANA_SYLLABLES = [
    'ア', 'イ', 'ウ', 'エ', 'オ',
    'カ', 'キ', 'ク', 'ケ', 'コ',
    'サ', 'シ', 'ス', 'セ', 'ソ',
    'タ', 'チ', 'ツ', 'テ', 'ト',
    'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
    'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
    'マ', 'ミ', 'ム', 'メ', 'モ',
    'ヤ', 'ユ', 'ヨ',
    'ラ', 'リ', 'ル', 'レ', 'ロ',
    'ワ', 'ン'
]

DAKUTEN_KATAKANA_SYLLABLES = [
    'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
    'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
    'ダ', 'デ', 'ド',
    'バ', 'ビ', 'ブ', 'ベ', 'ボ'
]

HANDAKUTEN_KATAKANA_SYLLABLES = [
    'パ', 'ピ', 'プ', 'ペ', 'ポ',
]


SMALL_KATAKANA = ['ャ', 'ュ', 'ョ', 'ッ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ']

Y_COMBO_KATAKANA = []
for char in "キシチニヒミリギジビピ":
    Y_COMBO_KATAKANA.extend([char+y_char for y_char in ['ャ', 'ュ', 'ョ']])

# This constant is under the KATAKANA section
# because these combos are really only present in
# Katakana transliterations
SPECIAL_COMBO_ROMAJI = ["wi", "we", "wo",
                        "va", "vi", "vu", "ve", "vo",
                        "she", "je",
                        "fa", "fi", "fe", "fo",
                        "ti", "tu", "di", "du", "che"]

SPECIAL_COMBO_KATAKANA = ["ウィ",  "ウェ", 'ウォ',
                          "ヴァ", "ヴィ", "ヴ", "ヴェ", "ヴォ",
                          "ジェ", "ジェ",
                          "ファ", "フィ", "フェ", "フォ",
                          "ティ", "トゥ", "ディ", "ドゥ", "チェ"]

ALL_KATAKANA_COMPATIBLE_ROMAJI = []
ALL_KATAKANA_COMPATIBLE_ROMAJI += ALL_HIRAGANA_COMPATIBLE_ROMAJI + SPECIAL_COMBO_ROMAJI

ALL_KATAKANA = []
ALL_KATAKANA += BASIC_KATAKANA_SYLLABLES + DAKUTEN_KATAKANA_SYLLABLES
ALL_KATAKANA += HANDAKUTEN_KATAKANA_SYLLABLES + Y_COMBO_KATAKANA + SPECIAL_COMBO_KATAKANA

ALL_SINGLE_CHAR_KATAKANA = BASIC_KATAKANA_SYLLABLES + DAKUTEN_KATAKANA_SYLLABLES
ALL_SINGLE_CHAR_KATAKANA += HANDAKUTEN_KATAKANA_SYLLABLES + SMALL_KATAKANA + ["ー"]

ROMAJI_TO_KATAKANA: dict[str, str] = dict(zip(ALL_KATAKANA_COMPATIBLE_ROMAJI, ALL_KATAKANA))
KATAKANA_TO_ROMAJI: dict[str, str] = dict(zip(ALL_KATAKANA, ALL_KATAKANA_COMPATIBLE_ROMAJI))





### STYLING

with open("./src/config/styling.json", 'r', encoding="utf-8") as f:
    ALL_STYLES: dict = json.load(f)


# Text
TEXT_PROPERTIES: dict = ALL_STYLES["text_properties"]
APP_FONT: str = TEXT_PROPERTIES["font"]
SMALL_FONTSIZE: int = TEXT_PROPERTIES["small_fontsize"]
MED_FONTSIZE: int = TEXT_PROPERTIES["med_fontsize"]
LARGE_FONTSIZE: int = TEXT_PROPERTIES["large_fontsize"]
TEXT_DARKMODE_COLOR: str = TEXT_PROPERTIES["darkmode_color"]
TEXT_LIGHTMODE_COLOR: str = TEXT_PROPERTIES["lightmode_color"]
TEXT_CURRENT_COLOR = TEXT_DARKMODE_COLOR if settings.DARK_MODE else TEXT_LIGHTMODE_COLOR
TEXT_CURRENT_OPPOSITE_COLOR = TEXT_LIGHTMODE_COLOR if settings.DARK_MODE else TEXT_DARKMODE_COLOR


# Background
BG_PROPERTIES: dict = ALL_STYLES["bg"]
BG_LIGHTMODE: str = BG_PROPERTIES["lightmode"]
BG_DARKMODE: str = BG_PROPERTIES["darkmode"]
BG_CURRENT_COLOR = BG_DARKMODE if settings.DARK_MODE else BG_LIGHTMODE
BG_CURRENT_OPPOSITE_COLOR = BG_LIGHTMODE if settings.DARK_MODE else BG_DARKMODE

# Buttons
BUTTON_PROPERTIES: dict = ALL_STYLES["button_properties"]
MENUBUTTON_COLOR: str = BUTTON_PROPERTIES["menubutton_color"]
KEYBOARD_BUTTON_COLOR = BG_CURRENT_COLOR




### KANA KEYBOARD SETUP
HIRAGANA_BASIC_KEYBOARD = [
    ['あ', 'い', 'う', 'え', 'お'],
    ['か', 'き', 'く', 'け', 'こ'],
    ['さ', 'し', 'す', 'せ', 'そ'],
    ['た', 'ち', 'つ', 'て', 'と'],
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['は', 'ひ', 'ふ', 'へ', 'ほ'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['や', '*', 'ゆ', '*', 'よ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['わ', '*', '*', '*', 'ん']
]


HIRAGANA_DAKUTEN_KEYBOARD = [
    ['*', '*', '*', '*', '*'], # vowel
    ['が', 'ぎ', 'ぐ', 'げ', 'ご'], # k
    ['ざ', 'じ', 'ず', 'ぜ', 'ぞ',], # s
    ['だ', 'ぢ', 'づ', 'で', 'ど'], # t
    ['*', '*', '*', '*', '*'], # n
    ['ば', 'び', 'ぶ', 'べ', 'ぼ'], # h
    ['*', '*', '*', '*', '*'], # m
    ['*', '*', '*', '*', '*'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]

HIRAGANA_HANDAKUTEN_KEYBOARD = [
    ['*', '*', '*', '*', '*'], # vowel
    ['*', '*', '*', '*', '*'], # k
    ['*', '*', '*', '*', '*'], # s
    ['*', '*', '*', '*', '*'], # t
    ['*', '*', '*', '*', '*'], # n
    ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'], # h
    ['*', '*', '*', '*', '*'], # m
    ['*', '*', '*', '*', '*'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]

HIRAGANA_SMALL_KEYBOARD = [
    ['*', '*', '*', '*', '*'], # vowel
    ['*', '*', '*', '*', '*'], # k
    ['*', '*', '*', '*', '*'], # s
    ['*', '*', 'っ', '*', '*'], # t
    ['*', '*', '*', '*', '*'], # n
    ['*', '*', '*', '*', '*'], # h
    ['*', '*', '*', '*', '*'], # m
    ['ゃ', '*', 'ゅ', '*', 'ょ'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]



KATAKANA_BASIC_KEYBOARD = [
    ['ア', 'イ', 'ウ', 'エ', 'オ'],
    ['カ', 'キ', 'ク', 'ケ', 'コ'],
    ['サ', 'シ', 'ス', 'セ', 'ソ'],
    ['タ', 'チ', 'ツ', 'テ', 'ト'],
    ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'],
    ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'],
    ['マ', 'ミ', 'ム', 'メ', 'モ'],
    ['ヤ', '*', 'ユ', '*', 'ヨ'],
    ['ラ', 'リ', 'ル', 'レ', 'ロ'],
    ['ワ', '*', 'ー', '*', 'ン']
]


KATAKANA_SMALL_KEYBOARD = [
    ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ'], # vowel
    ['*', '*', '*', '*', '*'], # k
    ['*', '*', '*', '*', '*'], # s
    ['*', '*', 'ッ', '*', '*'], # t
    ['*', '*', '*', '*', '*'], # n
    ['*', '*', '*', '*', '*'], # h
    ['*', '*', '*', '*', '*'], # m
    ['ャ', '*', 'ュ', '*', 'ョ'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]

KATAKANA_DAKUTEN_KEYBOARD = [
    ['*', '*', 'ヴ', '*', '*'], # vowel
    ['ガ', 'ギ', 'グ', 'ゲ', 'ゴ'], # k
    ['ザ', 'ジ', 'ズ', 'ゼ', 'ゾ'], # s
    ['ダ', 'ヂ', 'ヅ', 'デ', 'ド'], # t
    ['*', '*', '*', '*', '*'], # n
    ['バ', 'ビ', 'ブ', 'ベ', 'ボ'], # h
    ['*', '*', '*', '*', '*'], # m
    ['*', '*', '*', '*', '*'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]

KATAKANA_HANDAKUTEN_KEYBOARD = [
    ['*', '*', '*', '*', '*'], # vowel
    ['*', '*', '*', '*', '*'], # k
    ['*', '*', '*', '*', '*'], # s
    ['*', '*', '*', '*', '*'], # t
    ['*', '*', '*', '*', '*'], # n
    ['パ', 'ピ', 'プ', 'ペ', 'ポ'], # h
    ['*', '*', '*', '*', '*'], # m
    ['*', '*', '*', '*', '*'], # y
    ['*', '*', '*', '*', '*'], # r
    ['*', '*', '*', '*', '*'] # w
]



### DAKUTEN TO BASIC BINDING

# basically, we're indicating here that diacritics are
# really just variations of a main character

HIRAGANA_DIACRITIC_BINDER = {
    "が" : "か",
    "ぎ" : "き",
    "ぐ" : "く",
    "げ" : "け",
    "ご" : "こ",
    "ざ" : "さ",
    "じ" : "し",
    "ず" : "す",
    "ぜ" : "せ",
    "ぞ" : "そ",
    "だ" : "た",
    "で" : "て",
    "ど" : "と",
    "ば" : "は",
    "び" : "ひ",
    "ぶ" : "ふ",
    "べ" : "へ",
    "ぼ" : "ほ",
    "ぱ" : "は",
    "ぴ" : "ひ",
    "ぷ" : "ふ",
    "ぺ" : "へ",
    "ぽ" : "ほ",
}

KATAKANA_DIACRITIC_BINDER = {
    "ガ" : "カ",
    "ギ" : "キ",
    "グ" : "ク",
    "ゲ" : "ケ",
    "ゴ" : "コ",
    "ザ" : "サ",
    "ジ" : "シ",
    "ズ" : "ス",
    "ゼ" : "セ",
    "ゾ" : "ソ",
    "ダ" : "タ",
    "デ" : "テ",
    "ド" : "ト",
    "バ" : "ハ",
    "ビ" : "ヒ",
    "ブ" : "フ",
    "ベ" : "ヘ",
    "ボ" : "ホ",
    "パ" : "ハ",
    "ピ" : "ヒ",
    "プ" : "フ",
    "ペ" : "ヘ",
    "ポ" : "ホ",
    "ヴ" : "ウ",
}
