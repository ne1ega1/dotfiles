#!/bin/bash

nwg-menu \
  -s "menu-start.css" \
  -va "top" \
  -ha "left" \
  -fm "yazi" \
  -cmd-lock "hyprlocklock" \
  -cmd-logout "hyprctl dispatch exit" \
  -cmd-restart "systemctl -i reboot" \
  -cmd-shutdown "systemctl -i poweroff" \
  -d \
  # -height 800 \
  # -width 400 \
  -isl 32 \
  -iss 16 \
  -lang "en" \
  -padding 2 \
  -mb 100 \
  -ml 10 \
  -mr 10 \
  -mt 100 \
  -o "jumanji" \
  -term "kitty" \
  -wm "hyprland" \
  -v
