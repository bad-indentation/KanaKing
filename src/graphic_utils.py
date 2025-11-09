"""
graphic_utils.py

A module which contains the
styling for the graphics of the
program. Custom styles
are subclasses of tkinter widgets.
"""

# pylint: disable=all

from __future__ import annotations
from typing import Literal
import tkinter as tk
from PIL import Image, ImageTk
from config.constants import *



class BasicButton(tk.Button):
    """Basic styled button."""


    def __init__(self, hover_effect=True, *args, **kwargs):

        super().__init__(*args, **kwargs, font=(APP_FONT, MED_FONTSIZE))



        if hover_effect:
            self.bind("<Enter>", self.on_hover)
            self.bind("<Leave>", self.on_exit_hover)

        # Padding
        self.padx = 5
        self.pady = 5


    def on_hover(self, e=None):
        """
        Button grows slightly on hover
        """

        self.config(font=(APP_FONT, round(MED_FONTSIZE*1.1)))


    def on_exit_hover(self, e=None):
        """
        Button returns to original size when
        user stops hovering
        """
        self.config(font=(APP_FONT, MED_FONTSIZE))


    def pack(self, *args, **kwargs):
        """
        Modified packing function
        """
        super().pack(padx=self.padx, pady=self.pady, *args, **kwargs)



class MenuButton(BasicButton):
    """
    Specialized button with additional
    effects. When user hovers over button,
    text is converted from Japanese to English.
    Automatically colored according to constant
    values.
    """

    def __init__(self, en: str, jp: str, *args, **kwargs):
        super().__init__(hover_effect=True, bg=MENUBUTTON_COLOR, fg=TEXT_CURRENT_COLOR,
                         text=jp, activebackground=MENUBUTTON_COLOR,
                         activeforeground=TEXT_CURRENT_COLOR,
                         *args, **kwargs)


        # An effect where the text changes from Japanese to English
        self.jp = jp
        self.en = en

        while len(self.en) < len(self.jp)*2.2:
            self.en = " " + self.en + " "

    def on_hover(self, e=None):
        super().on_hover(e)
        self.config(text=self.en)

    def on_exit_hover(self, e=None):
        super().on_exit_hover(e)
        self.config(text=self.jp)



class KeyboardButton(BasicButton):
    """
    Button used to represent keys when typing
    Kana.
    """

    def __init__(self, char: str, *args, **kwargs):
        super().__init__(False, bg=BG_CURRENT_COLOR, fg=TEXT_CURRENT_COLOR,
                         activebackground=TEXT_CURRENT_COLOR, activeforeground=BG_CURRENT_COLOR,
                         text=char,
                         *args, **kwargs)
        self.char = char

        # Overriding some parent attributes
        self.padx = 0
        self.pady = 0
        self.config(font=(APP_FONT, SMALL_FONTSIZE))



class KatakanaKeyboard(tk.Frame):
    """
    A custom widget designed for easy
    Katakana entry

    Yes, I could have made a keyboard parent class,
    but I'm too lazy for that.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(bg=BG_CURRENT_COLOR, *args, **kwargs)

        self.text = ""
        self.mode: Literal["normal", "dakuten", "handakuten", "small"] = "normal"


        self.initialize_subwidgets()



    def initialize_subwidgets(self):
        """
        Creates all of the necessary subwidgets for
        the keyboard
        """
        self.text_entry = tk.Label(self, bg=BG_CURRENT_OPPOSITE_COLOR,
                              fg=TEXT_CURRENT_OPPOSITE_COLOR, font=(APP_FONT, MED_FONTSIZE),
                              text=self.text)

        self.text_entry.pack(side="top")

        self.menu_frame = tk.Frame(self, bg=BG_CURRENT_COLOR,)
        self.menu_frame.pack(side="top", pady=5)

        normal_mode_btn = self._create_change_mode_button('ハ', master=self.menu_frame)
        normal_mode_btn.bind("<Button-1>", lambda e: self.change_mode("normal"))

        dakuten_mode_btn = self._create_change_mode_button('バ', master=self.menu_frame)
        dakuten_mode_btn.bind("<Button-1>", lambda e: self.change_mode("dakuten"))

        handakuten_mode_btn = self._create_change_mode_button('パ', master=self.menu_frame)
        handakuten_mode_btn.bind("<Button-1>", lambda e: self.change_mode("handakuten"))

        small_mode_btn = self._create_change_mode_button('小', master=self.menu_frame)
        small_mode_btn.bind("<Button-1>", lambda e: self.change_mode("small"))

        clear_btn = self._create_change_mode_button("Ｘ", master=self.menu_frame)
        clear_btn.bind("<Button-1>", lambda e: self.clear())

        self.key_frame = tk.Frame(self, bg=BG_CURRENT_COLOR,)
        self.key_frame.pack(side="top", pady=5)

        self.initialize_keyboard()


    def _create_change_mode_button(self, text: str, master: tk.Misc) -> KeyboardButton:
        """
        Method for creating buttons which look similar to keyboard
        buttons but are used to switch between keyboard modes (i.e.
        normal, dakuten, handakuten, small)
        """
        mode_button = KeyboardButton(text, master=master)
        mode_button.config(bg=MENUBUTTON_COLOR)
        mode_button.pack(side="left")

        return mode_button

    def initialize_keyboard(self):
        """
        Adds in the keyboard keys
        """
        self.keyboard_keys: list[KeyboardButton] = []

        match self.mode:
            case "normal":
                keyboard_chars = KATAKANA_BASIC_KEYBOARD
            case "dakuten":
                keyboard_chars = KATAKANA_DAKUTEN_KEYBOARD
            case "handakuten":
                keyboard_chars = KATAKANA_HANDAKUTEN_KEYBOARD
            case "small":
                keyboard_chars = KATAKANA_SMALL_KEYBOARD

        for c, col in enumerate(keyboard_chars):
            for r, char in enumerate(col):
                if char != "*":
                    key = KeyboardButton(char, master=self.key_frame)

                    key.bind("<Button-1>", lambda e, ch=char: self.add_character(ch))

                    key.grid(row=r, column=10-c)
                    self.keyboard_keys.append(key)

        self.bind_all("<BackSpace>", self.clear)


    def add_character(self, character: str):
        """Adds a character to the text field"""
        self.text += character
        self.text_entry.config(text=self.text)

    def clear(self, e=None):
        """Clears the text field"""
        self.text = self.text[:-1]
        self.text_entry.config(text=self.text)


    def change_mode(self, mode: Literal["normal", "dakuten", "handakuten", "small"]):
        """Changes the mode of the keyboard"""
        self.mode = mode
        [key.destroy() for key in self.keyboard_keys]
        self.initialize_keyboard()



    def pack(self, *args, **kwargs):
        """Custom pack settings for this widget"""
        super().pack(padx=5, pady=5, *args, **kwargs)



class HiraganaKeyboard(tk.Frame):
    """
    A custom widget designed for easy
    Hiragana entry
    """

    def __init__(self, *args, **kwargs):

        super().__init__(bg=BG_CURRENT_COLOR, *args, **kwargs)

        self.text = ""
        self.mode: Literal["normal", "dakuten", "handakuten", "small"] = "normal"


        self.initialize_subwidgets()



    def initialize_subwidgets(self):
        """
        Creates all of the necessary subwidgets for
        the keyboard
        """
        self.text_entry = tk.Label(self, bg=BG_CURRENT_OPPOSITE_COLOR,
                              fg=TEXT_CURRENT_OPPOSITE_COLOR, font=(APP_FONT, MED_FONTSIZE),
                              text=self.text)

        self.text_entry.pack(side="top")

        self.menu_frame = tk.Frame(self, bg=BG_CURRENT_COLOR,)
        self.menu_frame.pack(side="top", pady=5)

        normal_mode_btn = self._create_change_mode_button('は', master=self.menu_frame)
        normal_mode_btn.bind("<Button-1>", lambda e: self.change_mode("normal"))

        dakuten_mode_btn = self._create_change_mode_button('ば', master=self.menu_frame)
        dakuten_mode_btn.bind("<Button-1>", lambda e: self.change_mode("dakuten"))

        handakuten_mode_btn = self._create_change_mode_button('ぱ', master=self.menu_frame)
        handakuten_mode_btn.bind("<Button-1>", lambda e: self.change_mode("handakuten"))

        small_mode_btn = self._create_change_mode_button('小', master=self.menu_frame)
        small_mode_btn.bind("<Button-1>", lambda e: self.change_mode("small"))

        clear_btn = self._create_change_mode_button("Ｘ", master=self.menu_frame)
        clear_btn.bind("<Button-1>", lambda e: self.clear())

        self.key_frame = tk.Frame(self, bg=BG_CURRENT_COLOR,)
        self.key_frame.pack(side="top", pady=5)

        self.initialize_keyboard()


    def _create_change_mode_button(self, text: str, master: tk.Misc) -> KeyboardButton:
        """
        Method for creating buttons which look similar to keyboard
        buttons but are used to switch between keyboard modes (i.e.
        normal, dakuten, handakuten, small)
        """
        mode_button = KeyboardButton(text, master=master)
        mode_button.config(bg=MENUBUTTON_COLOR)
        mode_button.pack(side="left")

        return mode_button

    def initialize_keyboard(self):
        """
        Adds in the keyboard keys
        """
        self.keyboard_keys: list[KeyboardButton] = []

        match self.mode:
            case "normal":
                keyboard_chars = HIRAGANA_BASIC_KEYBOARD
            case "dakuten":
                keyboard_chars = HIRAGANA_DAKUTEN_KEYBOARD
            case "handakuten":
                keyboard_chars = HIRAGANA_HANDAKUTEN_KEYBOARD
            case "small":
                keyboard_chars = HIRAGANA_SMALL_KEYBOARD

        for c, col in enumerate(keyboard_chars):
            for r, char in enumerate(col):
                if char != "*":
                    key = KeyboardButton(char, master=self.key_frame)

                    # Small lambda bug fix by ChatGPT; without the ch=char,
                    # the program was only able to output one letter no matter what
                    # key was pressed
                    key.bind("<Button-1>", lambda e, ch=char: self.add_character(ch))

                    key.grid(row=r, column=10-c)
                    self.keyboard_keys.append(key)

        self.bind_all("<BackSpace>", self.clear)


    def add_character(self, character: str):
        """Adds a character to the text field"""
        self.text += character
        self.text_entry.config(text=self.text)

    def clear(self, e=None):
        """Clears the text field"""
        self.text = self.text[:-1]
        self.text_entry.config(text=self.text)


    def change_mode(self, mode: Literal["normal", "dakuten", "handakuten", "small"]):
        """Changes the mode of the keyboard"""
        self.mode = mode
        [key.destroy() for key in self.keyboard_keys]
        self.initialize_keyboard()



    def pack(self, *args, **kwargs):
        """Custom pack settings for this widget"""
        super().pack(padx=5, pady=5, *args, **kwargs)



class RomajiEntry(tk.Entry):
    """
    Styled entry graphic
    """
    def __init__(self, *args, **kwargs):
        super().__init__(bg=BG_CURRENT_OPPOSITE_COLOR, fg=TEXT_CURRENT_OPPOSITE_COLOR,
                         font=(APP_FONT, MED_FONTSIZE, "italic"),
                         *args, **kwargs)

        self.bind("<KeyRelease>", self.check_for_invalid)
        self.text_var = tk.StringVar(self)
        self.config(textvariable=self.text_var)



    def check_for_invalid(self, e=None):
        """
        Looks for invalid characters in the
        user's entry (that is, any punctuation)
        """
        new_string = ""
        for char in self.get():
            if char.isalpha():
                new_string += char.lower()

        self.text_var.set(new_string)



class Icon(tk.Canvas):
    """
    Used to display the icon image
    """
    def __init__(self, scale: tuple=(1, 1), *args, **kwargs):
        self.icon = Image.open("src/icon.png")
        icon_width = int(self.icon.width*scale[0])
        icon_height = int(self.icon.height*scale[1])
        self.icon = self.icon.resize((icon_width, icon_height),
                                     Image.Resampling.LANCZOS)
        self.icon = ImageTk.PhotoImage(self.icon)

        super().__init__(bg=BG_CURRENT_COLOR, width=self.icon.width(), height=self.icon.height(), bd=0,
                         highlightthickness=0,
                         *args, **kwargs)
        self.create_image(0, 0, image=self.icon, anchor=tk.NW)



class BasicLabel(tk.Label):
    """
    Custom label style
    """
    def __init__(self, fontsize: int, *args, **kwargs):
        super().__init__(bg=BG_CURRENT_COLOR, font=(APP_FONT, fontsize),
                         fg=TEXT_CURRENT_COLOR, *args, **kwargs)


def graphics_test():
    """Packs all of the styles widgets onto a screen for testing"""
    root = tk.Tk()
    root.geometry("500x500")
    root.config(bg=BG_CURRENT_COLOR)

    entry = Icon(scale=(0.5, 0.5), master=root)
    entry.pack()

    root.mainloop()



if __name__ == "__main__":
    graphics_test()
