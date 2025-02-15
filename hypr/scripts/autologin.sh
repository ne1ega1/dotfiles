#!/bin/bash

FILE=/etc/systemd/system/getty.target.wants/getty@tty1.service

sed -i "s|ExecStart=-/sbin/agetty -o '-- \\u' --noreset --noclear - ${TERM}|ExecStart=-/sbin/agetty -o '-p -f -- \\u' --noclear --autologin jumanji %I $TERM|g" "$FILE"

echo "Автологин включен"
