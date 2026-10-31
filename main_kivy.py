import random

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

BG = (12 / 255, 14 / 255, 26 / 255, 1)
WHITE = (245 / 255, 245 / 255, 1, 1)
PURPLE = (145 / 255, 80 / 255, 240 / 255, 1)
BLUE = (55 / 255, 115 / 255, 220 / 255, 1)
GREEN = (35 / 255, 180 / 255, 110 / 255, 1)
RED = (215 / 255, 65 / 255, 75 / 255, 1)
GRAY = (150 / 255, 155 / 255, 175 / 255, 1)


class GameButton(Button):
    def __init__(self, fill=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = fill
        self.color = WHITE
        self.bold = True
        self.font_size = "18sp"


class NightFuryApp(App):
    def build(self):
        Window.clearcolor = BG
        self.state = "MENU"
        self.difficulty = "EASY"
        self.max_tries = 15
        self.tries = 15
        self.secret = ""
        self.guess = ""
        self.history = []
        self.message = "Choose your difficulty"
        self.root_box = BoxLayout(
            orientation="vertical", padding=dp(16), spacing=dp(8)
        )
        self.show_menu()
        return self.root_box

    def clear_screen(self):
        self.root_box.clear_widgets()

    def add_title(self):
        self.root_box.add_widget(Label(
            text="[b][color=9150F0]NIGHT FURY[/color][/b]",
            markup=True, font_size="30sp",
            size_hint_y=None, height=dp(48)
        ))
        self.root_box.add_widget(Label(
            text="SECRET CODE", color=WHITE, font_size="17sp",
            size_hint_y=None, height=dp(28)
        ))

    def show_menu(self):
        self.state = "MENU"
        self.clear_screen()
        self.add_title()
        self.root_box.add_widget(Widget())
        self.root_box.add_widget(Label(
            text="SELECT DIFFICULTY", color=WHITE, font_size="20sp",
            size_hint_y=None, height=dp(42)
        ))
        for level, color in (
            ("EASY", GREEN), ("MEDIUM", BLUE), ("HARD", RED)
        ):
            button = GameButton(
                text=level, background_color=color,
                size_hint_y=None, height=dp(58)
            )
            button.bind(
                on_release=lambda _button, value=level: self.start_game(value)
            )
            self.root_box.add_widget(button)
        self.root_box.add_widget(Widget())

    def start_game(self, level):
        self.difficulty = level
        self.max_tries = {"EASY": 15, "MEDIUM": 10, "HARD": 6}[level]
        self.tries = self.max_tries
        self.secret = "".join(random.sample("0123456789", 4))
        self.guess = ""
        self.history = []
        self.message = "Enter 4 different digits"
        self.show_game()

    def show_game(self):
        self.state = "GAME"
        self.clear_screen()
        self.add_title()

        self.attempt_label = Label(
            color=WHITE, font_size="17sp",
            size_hint_y=None, height=dp(30)
        )
        self.guess_label = Label(
            color=GREEN, font_size="30sp",
            size_hint_y=None, height=dp(48)
        )
        self.message_label = Label(
            color=WHITE, font_size="14sp",
            size_hint_y=None, height=dp(28)
        )
        self.root_box.add_widget(self.attempt_label)
        self.root_box.add_widget(Label(
            text="YOUR GUESS", color=GRAY,
            size_hint_y=None, height=dp(24)
        ))
        self.root_box.add_widget(self.guess_label)
        self.root_box.add_widget(self.message_label)

        self.history_label = Label(
            text="SCORE / HISTORY", color=WHITE,
            font_size="13sp", halign="center", valign="middle",
            size_hint_y=0.8
        )
        self.history_label.bind(
            size=lambda obj, value: setattr(obj, "text_size", value)
        )
        self.root_box.add_widget(self.history_label)

        keypad = GridLayout(
            cols=3, spacing=dp(7), size_hint_y=1.7
        )
        for number in range(1, 10):
            button = GameButton(text=str(number))
            button.bind(
                on_release=lambda _button, value=str(number): self.add_digit(value)
            )
            keypad.add_widget(button)

        zero = GameButton(text="0")
        zero.bind(on_release=lambda *_: self.add_digit("0"))
        keypad.add_widget(zero)

        clear = GameButton(text="CLEAR", background_color=RED)
        clear.bind(on_release=lambda *_: self.clear_guess())
        keypad.add_widget(clear)

        enter = GameButton(text="ENTER", background_color=GREEN)
        enter.bind(on_release=lambda *_: self.submit_guess())
        keypad.add_widget(enter)

        self.root_box.add_widget(keypad)
        self.refresh_game()

    def refresh_game(self):
        self.attempt_label.text = (
            f"{self.difficulty} | Attempts: {self.tries}/{self.max_tries}"
        )
        self.guess_label.text = self.guess + "_" * (4 - len(self.guess))
        self.message_label.text = self.message
        self.history_label.text = "\n".join(self.history[-4:]) or "SCORE / HISTORY"

    def add_digit(self, digit):
        if len(self.guess) < 4 and digit not in self.guess:
            self.guess += digit
            self.message = "Enter 4 different digits"
            self.refresh_game()

    def clear_guess(self):
        self.guess = ""
        self.message = "Enter 4 different digits"
        self.refresh_game()

    def submit_guess(self):
        if len(self.guess) != 4:
            self.message = "Enter exactly 4 digits"
            self.refresh_game()
            return

        bulls = sum(
            self.guess[index] == self.secret[index] for index in range(4)
        )
        cows = sum(digit in self.secret for digit in self.guess) - bulls
        self.history.append(
            f"{self.guess}  Bulls: {bulls}  Cows: {cows}"
        )
        self.tries -= 1

        if bulls == 4:
            self.show_result(True)
        elif self.tries <= 0:
            self.show_result(False)
        else:
            self.guess = ""
            self.message = "Try again!"
            self.refresh_game()

    def show_result(self, won):
        self.state = "WIN" if won else "LOSE"
        self.clear_screen()
        self.add_title()
        self.root_box.add_widget(Label(
            text="YOU WIN!" if won else "GAME OVER",
            color=GREEN if won else RED, font_size="30sp",
            size_hint_y=None, height=dp(70)
        ))
        self.root_box.add_widget(Label(
            text=f"Secret code: {self.secret}",
            color=WHITE, font_size="18sp"
        ))

        again = GameButton(
            text="PLAY AGAIN", background_color=GREEN,
            size_hint_y=None, height=dp(58)
        )
        again.bind(on_release=lambda *_: self.start_game(self.difficulty))
        menu = GameButton(
            text="MAIN MENU", background_color=BLUE,
            size_hint_y=None, height=dp(58)
        )
        menu.bind(on_release=lambda *_: self.show_menu())
        self.root_box.add_widget(again)
        self.root_box.add_widget(menu)


if __name__ == "__main__":
    NightFuryApp().run()
