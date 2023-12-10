#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/
# Icons: https://fontawesome.com/search?o=r&m=free

import os
import subprocess
import json
from pathlib import Path

from libqtile import hook
from libqtile import qtile
from libqtile import bar, layout
from libqtile.backend.wayland import InputConfig
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder
from libqtile.log_utils import logger

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

# --------------------------------------------------------
# General Variables
# --------------------------------------------------------

home = str(Path.home())
# core_name = "x11"
core_name = qtile.core.name
# wm_bar = "qtile"
if core_name == "x11":
    try:
        wm_bar = Path(home + "/.cache/.qtile_bar_x11.sh").read_text().replace("\n", "")
    except:
        wm_bar = "qtile"
elif qtile.core.name == "wayland":
    wm_bar = "qtile"

wmname = "QTILE"
monitors_order = ["DP-3", "DP-4.1", "DP-0"]
# Check for Desktop/Laptop (3 = Desktop)
platform = int(os.popen("cat /sys/class/dmi/id/chassis_type").read())

# --------------------------------------------------------
# Set default apps
# --------------------------------------------------------

terminal = "alacritty"
browser = "flatpak run ru.yandex.Browser"

# --------------------------------------------------------
# Groups
# --------------------------------------------------------


class ScreenGenInfo:
    def __init__(self, group_screen, groups):
        self.group_screen = group_screen
        self.groups = groups


class GroupGenInfo:
    def __init__(self, name, screen_affinity=None, spawn=None, matches=None):
        if matches is None:
            matches = []
        if spawn is None:
            spawn = []

        self.name = name
        self.screen_affinity = screen_affinity
        self.spawn = spawn
        self.matches = matches


screenGens = [
    ScreenGenInfo(
        group_screen=1,
        groups=[
            GroupGenInfo(
                name='  ',
                screen_affinity=0,
                spawn=[
                    'telegram-desktop', 'mattermost-desktop'
                ],
                matches=[
                    Match(wm_class='TelegramDesktop'),
                    Match(wm_class='Mattermost')
                ]
            )
        ]
    ),
    ScreenGenInfo(
        group_screen=2,
        groups=[
            GroupGenInfo(
                name='   ',
                screen_affinity=1,
                matches=[
                    Match(wm_class='jetbrains-pycharm-ce'),
                    Match(wm_class='steam')
                ]
            ),
            GroupGenInfo(
                name='   ',
                screen_affinity=1,
                matches=[
                    Match(wm_class='yaamp'),
                    Match(wm_class='Meld'),
                    Match(wm_class='Evolution'),
                    Match(wm_class='qBittorrent')
                ]
            )
        ]
    ),
    ScreenGenInfo(
        group_screen=3,
        groups=[
            GroupGenInfo(
                name='  ',
                screen_affinity=2,
                spawn=['flatpak run ru.yandex.Browser'],
                matches=[
                    Match(wm_class='Yandex-browser'),
                    Match(wm_class='gnome-text-editor')
                ]
            )
        ]
    ),
]

groups = []

for screen_index, screenGen in enumerate(screenGens):
    for groupIndex in range(len(screenGen.groups)):
        groupGen = screenGen.groups[groupIndex]
        groups.append(
            Group(
                name=groupGen.name,
                persist=True,
                layout='monadtall',
                screen_affinity=groupGen.screen_affinity,
                spawn=groupGen.spawn,
                matches=groupGen.matches
            )
        )

# --------------------------------------------------------
# Keybindings
# --------------------------------------------------------

mod = "mod4"  # SUPER KEY
shift = "shift"
ctrl = "control"

if core_name == "x11":
    logger.warning("Using keys with x11")
    keys = [
        # Focus
        Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
        Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
        Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
        Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
        Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),

        # Move
        Key([mod, shift], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([mod, shift], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([mod, shift], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, shift], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

        # Swap
        Key([mod, shift], "h", lazy.layout.swap_left()),
        Key([mod, shift], "l", lazy.layout.swap_right()),

        # Size
        Key([mod, ctrl], "Down", lazy.layout.shrink(), desc="Grow window to the left"),
        Key([mod, ctrl], "Up", lazy.layout.grow(), desc="Grow window to the right"),
        Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

        # Floating
        Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),

        # Split
        Key([mod, shift], "Return", lazy.layout.toggle_split(),
            desc="Toggle between split and unsplit sides of stack"),

        # Toggle Layouts
        Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

        # Full screen mode
        Key([mod], "f", lazy.window.toggle_fullscreen()),

        # System
        Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
        Key([mod, shift], "r", lazy.reload_config(),
            desc="Reload the config + reload polybar"),
        Key([mod, ctrl], "q", lazy.spawn(home + "/dotfiles/qtile/scripts/powermenu.sh"),
            desc="Open Power-menu"),
        Key([mod, shift], "s", lazy.spawn(home + "/dotfiles/qtile/scripts/x11/barswitcher.sh"),
            desc="Switch Status Bar"),

        # Apps
        Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        Key([mod, ctrl], "Return", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
        Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
        Key([mod, shift], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/x11/wallpaper.sh"),
            desc="Update Theme and Wallpaper"),
        Key([mod, ctrl], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/x11/wallpaper.sh select"),
            desc="Select Theme and Wallpaper"),
        Key([], "Print", lazy.spawn("flameshot gui"), desc="Take screenshot"),

        # Changing volume with the keyboard's scroll wheel
        Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),

        # Adjusting display brightness
        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q s +20%")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q s 20%-")),
    ]
elif qtile.core.name == "wayland":
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


def focus_group(qtile, screen, group):
    qtile.focus_screen(screen)
    qtile.groups_map[group].cmd_toscreen()


for screen_index, screenGen in enumerate(screenGens):
    groupKeys = []
    for groupIndex in range(len(screenGen.groups)):
        group = "{screen}:{group}".format(screen=screenGen.group_screen, group=groupIndex + 1)
        groupKeys.extend([
            Key([mod], "{group}".format(group=groupIndex + 1), lazy.function(focus_group, screen_index, group)),
            Key([mod, shift], "{group}".format(group=groupIndex + 1), lazy.window.togroup(group)),
        ])
    keys.append(KeyChord([mod], "{screen}".format(screen=screenGen.group_screen), groupKeys))

dgroups_key_binder = simple_key_binder(mod)

# --------------------------------------------------------
# Pywal Colors
# --------------------------------------------------------

colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
Color0 = (colordict['colors']['color0'])
Color1 = (colordict['colors']['color1'])
Color2 = (colordict['colors']['color2'])
Color3 = (colordict['colors']['color3'])
Color4 = (colordict['colors']['color4'])
Color5 = (colordict['colors']['color5'])
Color6 = (colordict['colors']['color6'])
Color7 = (colordict['colors']['color7'])
Color8 = (colordict['colors']['color8'])
Color9 = (colordict['colors']['color9'])
Color10 = (colordict['colors']['color10'])
Color11 = (colordict['colors']['color11'])
Color12 = (colordict['colors']['color12'])
Color13 = (colordict['colors']['color13'])
Color14 = (colordict['colors']['color14'])
Color15 = (colordict['colors']['color15'])

# --------------------------------------------------------
# Setup Layout Theme
# --------------------------------------------------------

layout_theme = {
    "border_width": 3,
    "margin": 15,
    "border_focus": Color2,
    "border_normal": "FFFFFF",
    "single_border_width": 3
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating()
]

# --------------------------------------------------------
# Setup Widget Defaults
# --------------------------------------------------------

widget_defaults = dict(
    font="Fira Sans SemiBold",
    fontsize=14,
    padding=3
)
extension_defaults = widget_defaults.copy()

# --------------------------------------------------------
# Decorations
# https://qtile-extras.readthedocs.io/en/stable/manual/how_to/decorations.html
# --------------------------------------------------------

decor_left = {
    "decorations": [
        PowerLineDecoration(
            # path="arrow_left"
            path="rounded_left"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

decor_right = {
    "decorations": [
        PowerLineDecoration(
            # path="arrow_right"
            path="rounded_right"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

decor_group = {
    "decorations": [
        RectDecoration(
            colour=Color1 + ".4",
            radius=10,
            filled=True,
            padding_y=4,
            group=True
        )
    ],
    "padding": 10
}

# --------------------------------------------------------
# Widgets
# --------------------------------------------------------

widget_list = [
    widget.TextBox(
        **decor_group,
        group_id=1,
        background="#000000.3",
        text='App',
        foreground='ffffff',
        fontsize=16,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("rofi -show drun")}
    ),
    widget.Spacer(length=10),
    widget.GroupBox(
        **decor_group,
        group_id=2,
        toggle=True,
        center_aligned=True,
        background="#000000.3",
        highlight_method='text',
        disable_drag=True,
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=Color12 + ".4",
        block_highlight_text_color='ffffff',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff',
        inactive='#444444'
    ),
    widget.Spacer(length=10),
    widget.WidgetBox(
        **decor_group,
        close_button_location='right',
        text_closed="  ",
        text_open='x',
        fontsize=16,
        background="#000000.3",
        widgets=[
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text=" ",
                fontsize=16,
                mouse_callbacks={
                    "Button1": lambda: lazy.cmd_spawn("/home/ddryupin/Documents/Yaamp-0.0.1.AppImage")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("nautilus")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("flatpak run ru.yandex.Browser")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("snap run pycharm-community")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("telegram")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("mattermost-desktop")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("gnome-text-editor")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("meld")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("evolution")}
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                fontsize=16,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("steam-runtime")}
            ),
        ]
    ),
    widget.Spacer(length=10),
    widget.WindowName(
        **decor_left,
        max_chars=50,
        background="#000000.3",
        colour="#000000.3",
        width=350,
        font_size=16
    ),
    widget.Spacer(),
    widget.OpenWeather(
        **decor_group,
        location='Gubkin',
        format='{location_city} {main_temp} {icon}',
        background="#000000.3",
        update_interval=600
    ),
    widget.Spacer(length=10),
    widget.CPU(
        **decor_group,
        background="#000000.3",
        format='  {load_percent}%',
    ),
    widget.Memory(
        **decor_group,
        background="#000000.3",
        measure_mem='G',
        format="  {MemPercent: .0f}%"
    ),
    widget.Spacer(length=10),
    widget.ThermalSensor(
        **decor_group,
        background="#000000.3",
        tag_sensor="CPU",
        format='🌡 {temp:.0f}{unit}',
        foreground_alert="#FF0000",
        threshold=70,
        update_interval=1
    ),
    widget.ThermalSensor(
        **decor_group,
        background="#000000.3",
        tag_sensor="GPU",
        format='🌡 {temp:.0f}{unit}',
        foreground_alert="#FF0000",
        threshold=70,
        update_interval=1
    ),
    widget.Spacer(length=10),
    widget.Volume(
        **decor_group,
        background="#000000.3",
        step=5,
        fmt='{}',
        emoji=False,
        emoji_list=['🔇', '🔈', '🔉', '🔊']
    ),
    widget.WidgetBox(
        **decor_group,
        close_button_location='left',
        text_closed="  ",
        text_open='x',
        fontsize=16,
        background="#000000.3",
        widgets=[
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text="",
                foreground="000000.6",
                fontsize=16,
                mouse_callbacks={
                    "Button1": lambda: qtile.cmd_spawn(
                        "pactl set-default-sink alsa_output.usb-1532_Razer_Barracuda_X_R002000000-01.analog-stereo"
                    )
                }
            ),
            widget.TextBox(
                **decor_group,
                background="#000000.3",
                text=" ",
                foreground="000000.6",
                fontsize=16,
                mouse_callbacks={
                    "Button1": lambda: qtile.cmd_spawn(
                        "pactl set-default-sink alsa_output.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__sink"
                    )
                }
            ),
        ]
    ),
    widget.Spacer(length=10),
    widget.Clock(
        **decor_group,
        background="#000000.3",
        format="   %H:%M | %A %d %B",
    ),
    widget.Spacer(length=10),
    widget.Systray(
        **decor_right,
        icon_size=16,
        background="#000000.3"
    ),
    widget.TextBox(
        **decor_right,
        background="#000000.3",
        text=" ",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + "/dotfiles/qtile/scripts/powermenu.sh")},
    ),
]

# --------------------------------------------------------
# Screens
# --------------------------------------------------------

if wm_bar == "qtile":
    screens = [
        Screen(
            wallpaper_mode='fill'
        ),
        Screen(
            top=bar.Bar(
                widget_list,
                30,
                padding=20,
                opacity=1,
                border_width=[0, 0, 0, 0],
                margin=[0, 0, 0, 0],
                background="#000000.3"
            ),
            wallpaper_mode='fill'
        ),
        Screen(
            wallpaper_mode='fill'
        )
    ]
else:
    screens = [Screen(top=bar.Gap(size=28))]
    if (core_name == "x11"):
        screens = [Screen(top=bar.Gap(size=28))]
    else:
        screens = [Screen(top=bar.Gap(size=0))]


# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# --------------------------------------------------------
# Define floating layouts
# --------------------------------------------------------

floating_layout = layout.Floating(
    border_width=3,
    border_focus=Color2,
    border_normal="FFFFFF",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# --------------------------------------------------------
# General Setup
# --------------------------------------------------------

dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = False
wl_input_rules = None

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# --------------------------------------------------------
# Set wayland properties
# --------------------------------------------------------

# Keyboard layout
wl_input_rules = {
    "type:keyboard": InputConfig(kb_layout="us"),
}

# --------------------------------------------------------
# Hooks
# --------------------------------------------------------


# HOOK startups
@hook.subscribe.startup_once
def autostart():
    for i in range(3):
        wallpaper_cmd = f"feh --bg-fill $(cat ~/.cache/wal/wal) --no-fehbg --screen {i}"
        subprocess.Popen(wallpaper_cmd, shell=True)
    if qtile.core.name == "x11":
        autostartscript = "~/.config/qtile/autostart_x11.sh"
        subprocess.Popen(['setxkbmap', "us"])
    elif qtile.core.name == "wayland":
        autostartscript = "~/.config/qtile/autostart_wayland.sh"

    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])


# HOOK prioritize monitors
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    # Получите новый порядок мониторов
    new_order = [screen.name for screen in qtile.conn.pseudoscreens]

    # Установите порядок мониторов
    qtile.screens = [qtile.screens[new_order.index(monitor)] for monitor in monitors_order]
