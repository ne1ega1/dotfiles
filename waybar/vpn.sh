#!/bin/bash

while true; do
    if pgrep -a openvpn$ > /dev/null; then
        echo '{"text": "🔒", "tooltip": "VPN активен", "class": "active"}'
    else
        echo '{}'
    fi
    sleep 10
done
