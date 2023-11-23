"""Неиспользуемые части конфига"""

import os
import re
import socket
import subprocess
import psutil
import json
from libqtile import hook
from libqtile import qtile
from typing import List
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight, TextBox
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from pathlib import Path
from libqtile.log_utils import logger
from libqtile.backend.wayland import InputConfig

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

home = str(Path.home())
core_name = "x11"
wm_bar = "qtile"

try:
    wm_bar = Path(home + "/.cache/.qtile_bar_x11.sh").read_text().replace("\n", "")
except:
    wm_bar = "qtile"

mod = "mod4"  # SUPER KEY
shift = "shift"

if qtile.core.name == "wayland":
    logger.warning("Using keys with wayland")

    keys = [

        # Focus
        Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
        Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
        Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
        Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
        Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),

        # Move
        Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

        # Swap
        Key([mod, "shift"], "h", lazy.layout.swap_left()),
        Key([mod, "shift"], "l", lazy.layout.swap_right()),

        Key([mod], "Print", lazy.spawn(home + "/dotfiles/qtile/scripts/wayland/screenshot.sh")),

        # Size
        Key([mod, "control"], "Down", lazy.layout.shrink(), desc="Grow window to the left"),
        Key([mod, "control"], "Up", lazy.layout.grow(), desc="Grow window to the right"),
        Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

        # Floating
        Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),

        # Split
        Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
            desc="Toggle between split and unsplit sides of stack"),

        # Toggle Layouts
        Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

        # Fullscreen
        Key([mod], "f", lazy.window.toggle_fullscreen()),

        # System
        Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
        Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
        Key([mod, "control"], "q", lazy.spawn(home + "/dotfiles/qtile/scripts/powermenu.sh"), desc="Open Powermenu"),

        # Apps
        Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        Key([mod, "control"], "Return", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
        Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
        Key([mod, "shift"], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/wayland/wallpaper.sh"),
            desc="Update Theme and Wallpaper"),
        Key([mod, "control"], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/wayland/wallpaper.sh select"),
            desc="Select Theme and Wallpaper"),

        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q s +20%")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q s 20%-"))
    ]

groups = [
    Group(
        name="chats",
        label='  ',
        layout='monadtall',
        position=1,
        screen_affinity=0,
        matches=[
            Match(wm_class='TelegramDesktop'),
            Match(wm_class='Mattermost')
        ]
    ),
    Group(
        name="coding",
        label="  ",
        layout='monadtall',
        position=2,
        screen_affinity=1,
        matches=[
            Match(wm_class='jetbrains-pycharm-ce'),
            Match(wm_class='Evolution'),
            Match(wm_class='steam')
        ]
    ),
    Group(
        name="other",
        label="  ",
        layout='monadtall',
        position=3,
        screen_affinity=1,
        matches=[
            Match(wm_class='yaamp'),
            Match(wm_class='Meld'),
            Match(wm_class='qBittorrent')
        ]
    ),
    Group(
        name="browser",
        label="  ",
        layout='monadtall',
        position=4,
        screen_affinity=2,
        matches=[
            Match(wm_class='Yandex-browser'),
            Match(wm_class='gnome-text-editor')
        ]
    )
]

keys.extend(
    [
        Key([mod, "shift"], '1', lazy.window.togroup("")),
        Key([mod, "shift"], '2', lazy.window.togroup("")),
        Key([mod, "shift"], '3', lazy.window.togroup(""))
    ]
)

dgroups_key_binder = simple_key_binder(mod)

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

groups.append(ScratchPad("", [
    DropDown("yaamp", "chromium --app=https://chat.openai.com", x=0.3, y=0.1, width=0.40, height=0.4,
             on_focus_lost_hide=False),
    DropDown("mousepad", "mousepad", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False),
    DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False),
    DropDown("scrcpy", "scrcpy -d", x=0.8, y=0.05, width=0.15, height=0.6, on_focus_lost_hide=False)
]))

keys.extend([
    Key([mod], 'F10', lazy.group["6"].dropdown_toggle("yaamp")),
    Key([mod], 'F11', lazy.group["6"].dropdown_toggle("mousepad")),
    Key([mod], 'F12', lazy.group["6"].dropdown_toggle("terminal")),
    Key([mod], 'F9', lazy.group["6"].dropdown_toggle("scrcpy"))
])

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# Keyboard layout
wl_input_rules = {
    "type:keyboard": InputConfig(kb_layout="us"),
}

keyboard = widget.KeyboardLayout(configured_keyboards=['us', 'ru', 'us intl', 'gr'])
keys.extend([
    Key([mod, ], "i", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),
])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

# Widgets qtile

widgets = [
    widget.DF(
        **decor_right,
        padding=10,
        background=Color8 + ".4",
        visible_on_warn=False,
        format="{p} {uf}{m} ({r:.0f}%)"
    ),
    widget.Bluetooth(
        **decor_right,
        background=Color2 + ".4",
        padding=10,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("blueman-manager")},
    ),
    widget.Wlan(
        **decor_right,
        background=Color2 + ".4",
        padding=10,
        format='{essid} {percent:2.0%}',
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("alacritty -e nmtui")},
    ),
    widget.TextBox(
        **decor_right,
        background=Color10 + ".4",
        padding=5,
        text=" ",
        fontsize=16,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + "/dotfiles/scripts/cliphist.sh")},
    ),
]

# Show wi-fi/bluetooth
# show_wlan = True
# show_wlan = False
# show_bluetooth = True
# show_bluetooth = False

# Hide Modules if not on laptop
#if (show_wlan == False):
#    del widget_list[12:13]
#
#if (show_bluetooth == False):
#    del widget_list[11:12]
#
#if (core_name == "x11"):
#    del widget_list[12:13]
