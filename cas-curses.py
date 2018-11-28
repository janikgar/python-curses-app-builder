#!/usr/bin/env python3

import curses
import time
import subprocess
from enum import IntEnum


class ColorEnum(IntEnum):
    WHITE_K = 1
    BLUE_K = 2

class ChoicePanel(object):
    def __init__(self, win, title="", color=0, choices=None):
        self.win = win
        self.title = title
        self.color = color
        self.choices = choices
        win.attron(curses.color_pair(self.color))
        win.border()

    def add_title(self, text):
        win_y, win_x = self.getmaxyx()
        self.addstr(1, int((win_x - len(text)) / 2), text)

    def use(self):
        self.win.add_title(self.title)
        if self.choices:
            for i in range(0, len(self.choices)):
                self.win.addstr(i + 2, 2, self.choices[i])
        return self.win

def add_center_text(win, text):
    win_y, win_x = win.getmaxyx()
    win.addstr(1, int((win_x - len(text)) / 2), text)

def get_cas_profiles():
    """
    CAS returns a tabulated list of profiles and their URLs. We decode the
    binary string, split it on whitespace, and then select every other element
    in the list (skipping the URLs).
    """
    cas_profiles = subprocess.run(["cas", "profiles"], stdout=subprocess.PIPE)
    profiles_string = cas_profiles.stdout.decode()
    profiles_list = profiles_string.split()
    profiles = profiles_list[0::2]
    return profiles

def main(stdscr):
    keypress = 0
    cas_profiles = get_cas_profiles()
    curses.init_pair(ColorEnum.BLUE_K, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(ColorEnum.WHITE_K, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while (keypress != ord('q')):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        status_bar = stdscr.subwin(6, width-3, 0, 0)
        # status_bar.attron(curses.color_pair(1))
        status_bar.box()
        status_bar.addstr(1, 1, " " * (width - 5))

        left_win = stdscr.subwin(height-6, int(width / 3), 6, 0)
        profile_screen = ChoicePanel(win=left_win, title="CAS PROFILES", color=ColorEnum.BLUE_K, choices=cas_profiles)

        # right_win = stdscr.subwin(height-6, int(width / 3))
        # right_win.border()

        keypress = stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
