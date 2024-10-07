#!/usr/bin/env sh

killall -q waybar
while pgrep -x waybar >/dev/null; do sleep 1; done
# monitors_count=$(hyprctl monitors | grep -c "Monitor")

# if [ "$monitors_count" -le 1 ]; then
# 	waybar -c ~/.config/waybar/notebook_config &
# else
# 	waybar -c ~/.config/waybar/config.jsonc &
# fi

waybar

pkill swaync
swaync &
