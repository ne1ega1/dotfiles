#!/bin/bash
#    _                      _                 _  
#   | |__  _   _ _ __  _ __| | __ _ _ __   __| | 
#   | '_ \| | | | '_ \| '__| |/ _` | '_ \ / _` | 
#  _| | | | |_| | |_) | |  | | (_| | | | | (_| | 
# (_)_| |_|\__, | .__/|_|  |_|\__,_|_| |_|\__,_| 
#          |___/|_|                              
#  
# ----------------------------------------------------- 
# Overwrite hyprland configuration with hyprctl
# Individual scripts and settings possible
# Copy this file into your home directory
# ----------------------------------------------------- 

# ----------------------------------------------------- 
# Keyboard Layout
# -----------------------------------------------------
# hyprctl keyword input:kb_layout de # to de
hyprctl keyword input:kb_layout us # to us

# ----------------------------------------------------- 
# Monitor Setup
# See https://wiki.hyprland.org/Configuring/Monitors/
# ----------------------------------------------------- 
hyprctl keyword monitor eDP-1,1920x1080,0x0,1 monitor DP-4,1920x1080@120,1920x0,1 monitor DP-1,2560x1440,3840x0,1
# hyprctl keyword monitor ,preferred,auto,1

notify-send ".hyprland.sh exists" "hyprctl commands executed"
