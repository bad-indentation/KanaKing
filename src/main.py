"""
main.py

Controls the actual running of the application
"""

# pylint: disable=import-error
# pylint: disable=unused-import, wildcard-import
# pylint: disable=undefined-variable

from __future__ import annotations
import random
import time
from math import ceil
import tkinter as tk
from tkinter import messagebox

from config.settings import *
from graphic_utils import *
from data.word_collection import (get_potential_words,
                                  HIRAGANA_WORDLIST, KATAKANA_WORDLIST)
from data.userdata import (load_scores, HIRAGANA_DATA, KATAKANA_DATA,
                           update_data, reset_file, load_data)
from config.constants import (
    BG_CURRENT_COLOR,
    APP_FONT,
    LARGE_FONTSIZE,
    TEXT_CURRENT_COLOR,
    MENUBUTTON_COLOR,
    HIRAGANA_DIACRITIC_BINDER,
    KATAKANA_DIACRITIC_BINDER
)

INIT_WIN_WIDTH = 800
INIT_WIN_HEIGHT = 600



class Screen(tk.Frame):
    """
    Screen is a subclass of Frame that is
    used to pack in all of the widget of a
    given tab into the current window.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(highlightthickness=0, bd=0,
                         bg=BG_CURRENT_COLOR, *args, **kwargs)

        self.initialize_subwidgets()

    def initialize_subwidgets(self):
        """
        Initializes the subwidgets
        that will populate this screen.
        """

    def change_screen(self, new_screen: type[Screen]):
        """
        Switches the tab (for use in button commands
        and event bindings)
        """
        self.master.set_screen(new_screen(master=self.master))



class MainMenuScreen(Screen):
    """
    Screen for displaying the main menu options
    """

    def initialize_subwidgets(self):
        icon = Icon(master=self, scale=(0.25, 0.25))
        icon.pack(pady=20)

        welcome = BasicLabel(LARGE_FONTSIZE, master=self, text="Welcome to KanaKing!")
        welcome.pack(pady=70)

        self.study_button = MenuButton("Study", "べんきょうする", master=self,
                                       command=lambda: self.change_screen(StudyMenuScreen))
        self.study_button.pack()

        self.about_button = MenuButton("About", "じょうほう", master=self,
                                       command=lambda: self.change_screen(AboutScreen))
        self.about_button.pack()

        self.settings_button = MenuButton("Settings", "せってい", master=self,
                                       command=lambda: self.change_screen(SettingsScreen))
        self.settings_button.pack()

        self.stats_button = MenuButton("Stats", "とうけい", master=self,
                                       command=lambda: self.change_screen(StatsScreen))
        self.stats_button.pack()



class StudyMenuScreen(Screen):
    """
    Screen for the user to choose their options for
    the study session
    """

    def initialize_subwidgets(self):

        menu_title = BasicLabel(LARGE_FONTSIZE, master=self, text="New Study Session")
        menu_title.pack(pady=50)

        options_frm = tk.Frame(self, highlightthickness=0, bd=0, bg=BG_CURRENT_COLOR)
        options_frm.pack(pady=30)
        options_frm.columnconfigure(index=list(range(2)), minsize=300)
        options_frm.rowconfigure(index=list(range(2)), minsize=100)

        type_lbl = BasicLabel(MED_FONTSIZE, master=options_frm, text="Session Type")
        type_lbl.grid(row=0, column=0, sticky="WE")

        type_frm = tk.Frame(options_frm, highlightthickness=0, bd=0, bg=BG_CURRENT_COLOR)
        type_frm.grid(row=0, column=1, sticky="WE")

        type_radio_names = ["Hiragana", "Katakana", "Both"]
        self.type_radios = {}
        self.session_type = tk.StringVar(master=type_frm)

        for name in type_radio_names:
            new_radio = tk.Radiobutton(type_frm,
                                       bg=BG_CURRENT_COLOR, fg=TEXT_CURRENT_COLOR, text=name,
                                       value=name,
                                       bd=0, highlightthickness=0, indicatoron=True,
                                       selectcolor=MENUBUTTON_COLOR,
                                       variable=self.session_type)


            new_radio.pack(side="left", padx=5, fill="x")
            self.type_radios.update({name : new_radio})

        question_num_lbl = BasicLabel(MED_FONTSIZE, master=options_frm, text="# Questions")
        question_num_lbl.grid(row=1, column=0, sticky="WE")

        self.question_number = tk.Spinbox(options_frm, bg=BG_CURRENT_COLOR, fg=TEXT_CURRENT_COLOR,
                                          from_=1, to=200)

        # Set the value in the box
        self.question_number.delete(0, "end")
        self.question_number.insert(0, 25)

        self.question_number.grid(row=1, column=1, sticky="WE")

        navigation_frm = tk.Frame(self, highlightthickness=0, bd=0, bg=BG_CURRENT_COLOR)
        navigation_frm.pack(padx=20, pady=20, fill="x")

        exit_btn = BasicButton(master=navigation_frm, text="Back",
                               command=lambda: self.change_screen(MainMenuScreen))
        exit_btn.pack(side="left")

        start_button = MenuButton("Begin", "はじめる", master=navigation_frm,
                                  command=self.begin_session)
        start_button.pack(side="right")


    def begin_session(self):
        """
        Checks to ensure all fields are filled and
        then begins a study session.
        """

        # Are all fields filled?
        if self.session_type.get() not in ["Hiragana", "Katakana", "Both"]:
            messagebox.showerror("Invalid Entry", "Please select a session type before starting.")

        elif not self.question_number.get().isnumeric():
            messagebox.showerror("Invalid Entry", "Please enter a valid number of questions.")

        elif not 1 <= int(self.question_number.get()) <= 200:
            messagebox.showerror("Invalid Entry", "Your session must contain between 1 and 200 questions.")

        else:
            self.master.set_screen(SessionScreen(session_type=self.session_type.get(),
                                                 num_questions=self.question_number.get(),
                                                 master=self.master))



class SessionScreen(Screen):
    """Screen where the user begins practicing their kana"""
    def __init__(self, session_type: Literal["Hiragana", "Katakana", "Both"],
                 num_questions: int, *args, **kwargs):

        self.session_type: Literal["Hiragana", "Katakana", "Both"] = session_type
        self.num_questions = int(num_questions)
        self.questions_left = int(num_questions)
        self.answered_correct = 0 # counts number of questions user got right


        super().__init__(*args, **kwargs)

        self.begin_new_question()


    def initialize_subwidgets(self):

        self.prompt_lbl = BasicLabel(MED_FONTSIZE, master=self, text="")
        self.prompt_lbl.pack(pady=20)
        self.word_lbl = BasicLabel(LARGE_FONTSIZE, master=self, text="")
        self.word_lbl.pack()

        self.response_frm = tk.Frame(self, highlightthickness=0, bd=0, bg=BG_CURRENT_COLOR)
        self.response_frm.pack(pady=20)

        navigation_frm = tk.Frame(self, highlightthickness=0, bd=0, bg=BG_CURRENT_COLOR)
        navigation_frm.pack(padx=20, pady=20, fill="x")

        exit_btn = BasicButton(master=navigation_frm, text="Quit", command=self.quit_session)
        exit_btn.pack(side="left")

        self.start_button = MenuButton("Submit", "かいとうする", master=navigation_frm,
                                  command=self.submit_question)
        self.master.bind_all("<Return>", self.submit_question)
        self.start_button.pack(side="right")



    def begin_new_question(self):
        """
        Prompts the user with a new question
        """
        # Determine the question type
        if self.session_type == "Both":
            self.question_type = random.choice(["Hiragana", "Katakana"])

        else:
            self.question_type = self.session_type

        self.tranliteration_direction = random.choice(["from_kana", "from_romaji"])

        # Choose a character to test
        if self.question_type == "Hiragana":
            char_scores = load_scores(HIRAGANA_DATA)
        else:
            char_scores = load_scores(KATAKANA_DATA)

        options = []
        for char, score in char_scores.items():
            for _ in range(score):
                options.append(char)
        char_to_test = random.choice(options)


        # Choose a word to test
        if self.question_type == "Hiragana":
            possible_words = get_potential_words(char_to_test, HIRAGANA_WORDLIST)
        else:
            possible_words = get_potential_words(char_to_test, KATAKANA_WORDLIST)

        # `word_to_test` is organized as such:
        # [word, meaning, romaji]
        self.word_to_test = [random.choice(list(possible_words.keys()))]
        self.word_to_test.extend(possible_words[self.word_to_test[0]])


        # Update the graphics
        if self.tranliteration_direction == "from_kana":
            self.correct_answer = self.word_to_test[2]


            self.prompt_lbl.config(text="Transliterate the following word into Romaji:")
            self.word_lbl.config(text=f"{self.word_to_test[0]} - {self.word_to_test[1]}")

            self.entry_method = RomajiEntry(master=self.response_frm)
            self.entry_method.pack(pady=50)

        else:
            self.correct_answer = self.word_to_test[0]
            self.prompt_lbl.config(text="Transliterate the following word into Kana:")
            self.word_lbl.config(text=f"{self.word_to_test[2]} - {self.word_to_test[1]}")

            if self.question_type == "Hiragana":
                self.entry_method = HiraganaKeyboard(master=self.response_frm)
            else:
                self.entry_method = KatakanaKeyboard(master=self.response_frm)

            self.entry_method.pack()

        if CHEAT_MODE:
            self.cheat = BasicLabel(SMALL_FONTSIZE, text=f"Cheat: {self.correct_answer}",
                                    master=self.response_frm)
            self.cheat.pack()

        self.start_time = time.time()



    def submit_question(self, e=None):
        """Grades the user's response to a question"""

        # Check answer and light up text box accordingly

        my_answer = self.entry_method.get() if self.tranliteration_direction == "from_kana" else self.entry_method.text

        if my_answer: # empty string is a falsey
            if self.tranliteration_direction == "from_kana":
                correct = my_answer == self.correct_answer
                if correct:
                    self.entry_method.config(disabledforeground="green")
                    self.answered_correct += 1
                else:
                    self.entry_method.config(disabledforeground="red")

                self.entry_method.config(state="disabled")

            else:
                correct = my_answer == self.correct_answer
                if correct:
                    self.entry_method.text_entry.config(disabledforeground="green", state="disabled")
                    self.answered_correct += 1

                else:
                    self.entry_method.text_entry.config(disabledforeground="red", state="disabled")

                self.entry_method.menu_frame.destroy()
                self.entry_method.key_frame.destroy()
                self.entry_method.text_entry.unbind_all("<BackSpace>")

            # elapsed time per characters
            elapsed_time: int = min(ceil((time.time() - self.start_time) / len(my_answer)), 10)

            self.correct_lbl = BasicLabel(MED_FONTSIZE, text=f"Correct Answer: {self.correct_answer}",
                                        master=self.response_frm)
            self.correct_lbl.pack()

            # Updata data
            for char in self.word_to_test[0]:

                if self.question_type == "Hiragana":
                    if char in load_scores(HIRAGANA_DATA):
                        update_data(HIRAGANA_DATA, char, correct, elapsed_time)
                    elif char in HIRAGANA_DIACRITIC_BINDER:
                        update_data(HIRAGANA_DATA, HIRAGANA_DIACRITIC_BINDER[char], correct, elapsed_time)
                else:
                    if char in load_scores(KATAKANA_DATA):
                        update_data(KATAKANA_DATA, char, correct, elapsed_time)
                    elif char in KATAKANA_DIACRITIC_BINDER:
                        update_data(KATAKANA_DATA, KATAKANA_DIACRITIC_BINDER[char], correct, elapsed_time)


            self.questions_left -= 1

            # Repurpose "submit" button
            self.start_button.jp = "つづける"
            self.start_button.en = " Continue "
            if self.questions_left > 0:
                self.start_button.config(command=self.transition_to_next_question)
                self.master.bind_all("<Return>", self.transition_to_next_question)
            else:
                self.start_button.config(command=lambda: self.master.set_screen(FinishedScreen(self.answered_correct, self.num_questions)))
                self.master.bind_all("<Return>", lambda e=None: self.master.set_screen(FinishedScreen(self.answered_correct, self.num_questions)))


    def transition_to_next_question(self, e=None):
        """Clears up some extra widgets and initializes the next question"""
        for widget in self.response_frm.slaves():
            widget.destroy()
        # Re-repurpose "submit" button
        self.start_button.jp = "かいとうする"
        self.start_button.en = "   Submit   "
        self.start_button.config(command=self.submit_question)
        self.master.bind_all("<Return>", self.submit_question)
        self.begin_new_question()


    def quit_session(self):
        """Quits the sesson, but double-checks
        that's what the user wants."""
        response = messagebox.askyesno("Quit Session",
                                       "Are you sure you want to quit? All progress will be lost!")
        if response:
            self.master.set_screen(FinishedScreen(self.answered_correct, self.num_questions))



class FinishedScreen(Screen):
    """
    Screen where the user is directed after they have completed
    their session
    """

    def __init__(self, correct: int, total: int):
        self.correct = correct
        self.total = total
        super().__init__()


    def initialize_subwidgets(self):
        done = BasicLabel(LARGE_FONTSIZE, text="All Done!", master=self)
        done.pack(pady=50)

        done = BasicLabel(MED_FONTSIZE, text=f"You got {self.correct} / {self.total} questions correct.",
                          master=self)
        done.pack(pady=50)

        main_menu_button = MenuButton("Menu", "メニュー", master=self,
                                      command=lambda: self.change_screen(MainMenuScreen))
        main_menu_button.pack()



class AboutScreen(Screen):
    """
    Screen where the user can learn more about the project
    """
    def initialize_subwidgets(self):

        title = BasicLabel(LARGE_FONTSIZE, text="About", master=self)
        title.pack(side="top", fill="x")

        content_frame = tk.Frame(self, bg=BG_CURRENT_COLOR, bd=0, highlightthickness=0)
        content_frame.pack(side="top", fill="both", padx=10)



        self.content = """

Basic Use\n
---------\n\n

KanaKing is designed to be simple and intuitive to use. You may be surprised\n
at first to see that most of the buttons are labeled in Japanese, but this\n
is simply a stylistic choice - you can see their English translation by\n
hovering over them with a mouse. To begin a new study session, click on\n
"Study" ("べんきょうする") to begin a new study session. You will be directed\n
to a new page, where you can choose your session type (Hiragana, Katakana, or\n
Both) and the number of questions in your session (anywhere between 1 and\n
200). Once you begin your session, you will be presented with two types of\n
questions: Kana to Romaji, and Romaji to Kana. For the Kana to Romaji\n
exercises, simply select the text box and enter the romaji equivalent of the\n
kana provided. For the Romaji to Kana exercises, a digital kana keyboard will\n
be displayed. Simply click on the characters you want to add to the word. To\n
delete a character or to type a character with a diacritic, use the orange\n
buttons on the navigation bar at the top of the keyboard. When you are finished\n
entering your response, click "Submit" at the bottom right of the screen. After\n
completing all of the questions in the session, your score will be displayed.\n\n

If you would like to see your progress on your kana and what characters you're\n
struggling with, you can navigate to the "Stats" page, which shows you your five\n
best Hiragana and Katakana and your five worst Hiragana and Katakana.\n\n

If you need to see the answer to a question BEFORE submitting your response (such\n
as for debugging purposes), you can enable "Cheat Mode" in Settings.\n\n

About\n
-----\n\n

KanaKing (or かなキング) is a free, open-source piece of software dedicated to\n
helping learners master Japanese's syllabary alphabets. It was created by a\n
developer who is an amateur programmer and Japanese learner using Python,\n
TKinter, and several rolls of duct tape.\n\n
KanaKing aims to reinforce the user's kana reading abilities by giving them\n
examples of real Japanese words and asking them to convert from Japanese\n
script to Romaji. While this association with Romaji may not be ideal long-\n
term, the repeated examples and reading exercises should help learners to\n
build confidence in their reading. It is recommended that users say the words\n
out loud as they use the software. Future versions may include text-to-speech\n
exercises.\n\n
KanaKing is a unique piece of software because it tracks your proficiency for\n
each character. Your speed and accuracy are tracked for every word you are\n
shown. If you respond to a word slowly or incorrectly, the score for all of\n
the characters in that word will go up; if you respond quickly and\n
accurately, the score for that word will go down. Characters with the highest\n
scores will appear more often.\n\n
KanaKing does not claim to teach you Japanese, or even Kana. The purpose of this\n
software is to reinforce what you have already learned. If you don't know any\n
Kana yet, you should probably make use of a different resource before\n
practicing with KanaKing.
"""

        scrollbar = tk.Scrollbar(content_frame, bg=BG_CURRENT_OPPOSITE_COLOR)
        scrollbar.pack(side="right", fill="y")

        text_label = tk.Listbox(content_frame, bg=BG_CURRENT_COLOR, font=(APP_FONT, SMALL_FONTSIZE), bd=0,
                                fg=TEXT_CURRENT_COLOR, highlightthickness=0, height=18,
                                 yscrollcommand=scrollbar.set, width=100)
        for line in self.content.split("\n"):
            text_label.insert("end", line)


        scrollbar.config( command = text_label.yview )

        text_label.pack(side="right", fill="both")

        back_button = BasicButton(master=self, text="Back", command=lambda: self.change_screen(MainMenuScreen))
        back_button.pack()



class SettingsScreen(Screen):
    """
    A screen on which the user can select different settings
    for the software.
    """
    def __init__(self, *args, **kwargs):
        self.darkmode = tk.BooleanVar(value=DARK_MODE)
        self.cheatmode = tk.BooleanVar(value=CHEAT_MODE)
        super().__init__(*args, **kwargs)

    def initialize_subwidgets(self):
        title = BasicLabel(LARGE_FONTSIZE, text="Settings", master=self)
        title.pack(pady=20)

        settings_frm = tk.Frame(self, bd=0, highlightthickness=0, bg=BG_CURRENT_COLOR)
        settings_frm.pack(pady=20)
        settings_frm.rowconfigure(list(range(0, 2)), minsize=100, pad=20)
        settings_frm.columnconfigure(list(range(0, 1)), minsize=150)

        labels = ["Dark Mode", "Cheat Mode", "Reset User Data?"]
        for r, label in enumerate(labels):
            new_label = BasicLabel(MED_FONTSIZE, text=label, master=settings_frm)
            new_label.grid(row=r, column=0, sticky="W", padx=20)

        self.buttons = [
            tk.Checkbutton(settings_frm, highlightcolor=MENUBUTTON_COLOR, font=(APP_FONT, MED_FONTSIZE),
                           fg=TEXT_CURRENT_COLOR, bg=BG_CURRENT_COLOR, selectcolor=MENUBUTTON_COLOR,
                           variable=self.darkmode),
            tk.Checkbutton(settings_frm, highlightcolor=MENUBUTTON_COLOR, font=(APP_FONT, MED_FONTSIZE),
                           fg=TEXT_CURRENT_COLOR, bg=BG_CURRENT_COLOR, selectcolor=MENUBUTTON_COLOR,
                           variable=self.cheatmode),
            BasicButton(text="Reset", master=settings_frm, command=self.reset)
        ]

        for r, button in enumerate(self.buttons):
            button.grid(row=r, column=1, sticky="W", padx=20)

        navigation_frm = tk.Frame(self, bd=0, highlightthickness=0, bg=BG_CURRENT_COLOR)
        navigation_frm.pack(pady=20)

        back_button = BasicButton(master=navigation_frm, text="Back",
                                  command=lambda: self.change_screen(MainMenuScreen))
        back_button.pack(side="left")

        submit_button = BasicButton(master=navigation_frm, text="Update Settings",
                                    command=self.update_settings)
        submit_button.pack(side="right")


    def reset(self):
        """Resets all user data."""
        areyousure = messagebox.askokcancel("Reset User Data",
                                            "Are you sure? All kana data will be lost.")

        if areyousure:
            reset_file(HIRAGANA_DATA, "hiragana")
            reset_file(KATAKANA_DATA, "katakana")
            messagebox.showinfo("Data reset", "All kana data successfully reset.")


    def update_settings(self):
        """
        Changes the user settings according to what
        checkboxes were ticked
        """
        change_settings(self.darkmode.get(), self.cheatmode.get())
        messagebox.showinfo("Settings Updated",
                            "Please restart KanaKing for the settings to take effect.")



class StatsScreen(Screen):
    """
    Screen where the user can view statistics about
    their strongest and weakest kana
    """
    def initialize_subwidgets(self):

        title = BasicLabel(LARGE_FONTSIZE, text="Your Stats", master=self)
        title.pack(pady=20)

        sorted_hiragana = load_scores(HIRAGANA_DATA)
        sorted_hiragana = sorted(sorted_hiragana, key=sorted_hiragana.get)

        sorted_katakana = load_scores(KATAKANA_DATA)
        sorted_katakana = sorted(sorted_katakana, key=sorted_katakana.get)

        strongest_lbl = BasicLabel(MED_FONTSIZE, text="Strongest Kana", master=self)
        strongest_lbl.pack(pady=10)

        strong_hiragana = BasicLabel(SMALL_FONTSIZE, text="\t".join(sorted_hiragana[:5]), master=self)
        strong_hiragana.pack(pady=10)

        strong_katakana = BasicLabel(SMALL_FONTSIZE, text="\t".join(sorted_katakana[:5]), master=self)
        strong_katakana.pack(pady=10)

        weakest_lbl = BasicLabel(MED_FONTSIZE, text="Weakest Kana", master=self)
        weakest_lbl.pack(pady=10)

        weak_hiragana = BasicLabel(SMALL_FONTSIZE, text="\t".join(sorted_hiragana[-5:]), master=self)
        weak_hiragana.pack(pady=10)

        weak_katakana = BasicLabel(SMALL_FONTSIZE, text="\t".join(sorted_katakana[-5:]), master=self)
        weak_katakana.pack(pady=10)

        accuracy_fraction = [0, 0]
        all_data = load_data(HIRAGANA_DATA)
        all_data.update(load_data(KATAKANA_DATA))
        for data in all_data.values():
            accuracy_fraction[0] += data[0]
            accuracy_fraction[1] += data[2]

        accuracy = 0 if accuracy_fraction[1] == 0 else 1 - (accuracy_fraction[0] / accuracy_fraction[1])

        accuracy_lbl = BasicLabel(MED_FONTSIZE, text=f"Overall Accuracy: {accuracy:.2%}", master=self)
        accuracy_lbl.pack(pady=10)

        back_button = BasicButton(master=self, text="Back",
                                  command=lambda: self.change_screen(MainMenuScreen))
        back_button.pack()


class App(tk.Tk):
    """
    Main window where all subwidgets are placed
    """
    def __init__(self, screenName = None, baseName = None,
                 className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.config(bg=BG_CURRENT_COLOR)

        center = ((self.winfo_screenwidth() - INIT_WIN_WIDTH)//2,
                  (self.winfo_screenheight() - INIT_WIN_HEIGHT)//2)

        self.geometry(f"{INIT_WIN_WIDTH}x{INIT_WIN_HEIGHT}+{center[0]}+{center[1]}")
        self.title("KanaKing")


    def set_screen(self, new_screen: Screen):
        """
        Destroys everything on the screen and replaces
        it with the next screen that needs to be in place
        """
        for widget in self.slaves():
            widget.destroy()

        new_screen.pack()




def main():
    """
    Main process of the program
    """
    root = App()

    root.set_screen(MainMenuScreen(master=root))

    root.mainloop()


if __name__ == "__main__":
    main()
