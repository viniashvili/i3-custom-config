#!/usr/bin/env bash

pkill -x polybar 2>/dev/null || true
sleep 1

# Detect primary monitor
MONITOR="DP-2"

# If no primary is designated, use the first monitor

# Launch Polybar only on that monitor
MONITOR="$MONITOR" polybar \
    --config="$HOME/.config/polybar/spacegray.ini" \
    main >> "$HOME/.config/polybar/polybar.log" 2>&1 &
