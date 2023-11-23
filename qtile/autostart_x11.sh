#!/bin/sh
#   ___ _____ ___ _     _____   ____  _             _    
#  / _ \_   _|_ _| |   | ____| / ___|| |_ __ _ _ __| |_  
# | | | || |  | || |   |  _|   \___ \| __/ _` | '__| __| 
# | |_| || |  | || |___| |___   ___) | || (_| | |  | |_  
#  \__\_\|_| |___|_____|_____| |____/ \__\__,_|_|   \__| 
#                                                        
#  
# by Stephan Raabe (2023) 
# ----------------------------------------------------- 

# My screen resolution
# xrandr --rate 120
# xrandr --output DP-3 --primary --mode 1920x1080 --output DP-4.1 --mode 1920x1080 --right-of DP-3 --output DP-0 --mode 2560x1440 --right-of DP-4.1 &

# For Virtual Machine 
# xrandr --output Virtual-1 --mode 1920x1080

# Set keyboard layout in config.py

# Load picom
picom &

# Load power manager
xfce4-power-manager &

# Load notification service
dunst &

# Keyboard switch language
setxkbmap -layout "us,ru"
setxkbmap -option "grp:alt_shift_toggle,grp_led:scroll"

# Launch polybar
~/dotfiles/qtile/scripts/x11/loadbar.sh
sleep 1
xrandr --output DP-3 --primary --mode 1920x1080 --output DP-4.1 --mode 1920x1080 --right-of DP-3 --output DP-0 --mode 2560x1440 --right-of DP-4.1 &

sleep 1
# 
# Setup Wallpaper and update colors
~/dotfiles/qtile/scripts/x11/wallpaper.sh init
