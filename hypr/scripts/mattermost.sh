#!/usr/bin/env sh

pkill -f mattermost-desktop
sleep 10
mattermost-desktop --enable-features=UseOzonePlatform --ozone-platform=wayland
