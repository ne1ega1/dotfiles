#!/usr/bin/env sh
HYPRGAMEMODE=$(hyprctl getoption animations:enabled | sed -n '1p' | awk '{print $2}')

# Waybar performance
# FILE="$HOME/.config/waybar/style.css"
#
# sed -i 's/\/\* \(.*animation:.*\) \*\//\1/g' $FILE
# sed -i 's/\/\* \(.*transition:.*\) \*\//\1/g' $FILE
# if [ $HYPRGAMEMODE = 1 ]; then
#   sed -i 's/^\(.*animation:.*\)$/\/\* \1 \*\//g' $FILE
#   sed -i 's/^\(.*transition:.*\)$/\/\* \1 \*\//g' $FILE
# fi
# killall waybar
# waybar >/dev/null 2>&1 &

# Hyprland performance
if [ $HYPRGAMEMODE = 1 ]; then
  hyprctl --batch "\
        keyword animations:enabled 0;\
        keyword decoration:drop_shadow 0;\
        keyword decoration:blur:enabled 0;\
        keyword general:gaps_in 0;\
        keyword general:gaps_out 0;\
        keyword general:border_size 1;\
        keyword decoration:rounding 0;\
        dispatch dpms on DP-5;\
        dispatch dpms off eDP-1;\
        dispatch dpms off DP-4"
  exit
else
  hyprctl --batch "\
        dispatch dpms on eDP-1;\
        dispatch dpms on DP-4;\
        keyword monitor eDP-1,preferred,auto-right,1;\
        keyword monitor DP-4,1920x1080@120,0x0,1"
  hyprctl reload
fi
