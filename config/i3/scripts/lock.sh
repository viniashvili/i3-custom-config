#!/usr/bin/env bash


# Save current DPMS settings
saved_dpms=$(xset q)

old_times=$(printf '%s\n' "$saved_dpms" |
    sed -nE 's/^[[:space:]]*Standby:[[:space:]]*([0-9]+)[[:space:]]+Suspend:[[:space:]]*([0-9]+)[[:space:]]+Off:[[:space:]]*([0-9]+).*/\1 \2 \3/p')

restore_dpms() {
    if [[ -n "$old_times" ]]; then
        xset dpms $old_times
    fi

    if [[ "$saved_dpms" == *"DPMS is Disabled"* ]]; then
        xset -dpms
    else
        xset +dpms
    fi
}

trap restore_dpms EXIT

# Turn off monitors after 10 seconds of inactivity
xset +dpms
xset dpms 0 0 10
xset s reset


/usr/bin/i3lock --nofork \
    --color="1e1e2eff" \
    --image="$HOME/.config/i3/lockscreen/blurred.png" \
    --fill \
    --force-clock \
    --indicator \
    --time-str="%H:%M" \
    --date-str="%d %B" \
    --time-color="ffffffff" \
    --date-color="ccccccff" \
    --inside-color="1e1e2ecc" \
    --ring-color="89b4faff" \
    --insidever-color="1e1e2ecc" \
    --ringver-color="a6e3a1ff" \
    --insidewrong-color="1e1e2ecc" \
    --ringwrong-color="f38ba8ff" \
    --keyhl-color="a6e3a1ff" \
    --bshl-color="f38ba8ff" \
    --radius=110 \
    --ring-width=8 \
    --time-size=36 \
    --date-size=16 \
    --time-pos="ix:iy-12" \
    --date-pos="ix:iy+28" \
    --verif-text="" \
    --wrong-text="" \
    --no-modkey-text
