#!/usr/bin/env bash
if command -v nmcli >/dev/null 2>&1; then
    name=$(nmcli -t -f TYPE,STATE,CONNECTION device status |
        awk -F: '$2=="connected" && ($1=="wifi" || $1=="ethernet") {
            print $3; exit
        }')
    [ -n "$name" ] && printf 'NET %s\n' "$name"
fi
