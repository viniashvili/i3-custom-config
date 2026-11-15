# Ubuntu i3 desktop

Ubuntu/X11 i3 configuration with shortcuts, Spacegray Polybar, Rofi menus, scratchpad, Dunst, wallpapers, lock screen and Terminator settings.

## 1. Install programs

Run on the new Ubuntu computer before logging into i3; package names depend on the Ubuntu release.

```sh
sudo apt update
sudo apt install git i3-wm i3status i3lock xterm polybar rofi dunst terminator \
  feh flameshot dex xss-lock network-manager network-manager-gnome \
  pulseaudio-utils x11-xserver-utils x11-xkb-utils xserver-xorg-input-libinput \
  xinput python3 fontconfig \
  fonts-noto-core fonts-noto-color-emoji fonts-dejavu-core fonts-dejavu-mono \
  fonts-symbola arc-theme papirus-icon-theme scrot imagemagick
```

Install Symbols Nerd Font Mono and Qogir/Qogir-dark icons separately for matching glyphs and appearance.

```sh
fc-cache -f
fc-list : family | sort -u
```

The custom lock requires [i3lock-color](https://github.com/Raymo111/i3lock-color) flags at `/usr/bin/i3lock`; the screenshot locker requires ImageMagick's `magick` command.

```sh
/usr/bin/i3lock --help 2>&1 | less
command -v magick
```

## 2. Copy configuration

Run from this repository's root; these commands overwrite matching destination files.

```sh
mkdir -p "$HOME/.config" "$HOME/.local/share/rofi/themes" \
  "$HOME/.screenlayout" "$HOME/Pictures/Wallpapers" \
  "$HOME/.config/gtk-3.0" "$HOME/.config/terminator"
cp -a config/i3 config/polybar config/rofi config/dunst "$HOME/.config/"
cp -a config/gtk-3.0/settings.ini "$HOME/.config/gtk-3.0/settings.ini"
cp -a config/terminator/config "$HOME/.config/terminator/config"
cp -a local/share/rofi/themes/. "$HOME/.local/share/rofi/themes/"
cp -a screenlayout/monitors.sh "$HOME/.screenlayout/monitors.sh"
cp -a home/.fehbg home/.Xresources "$HOME/"
cp -a assets/wallpaper.jpg "$HOME/Pictures/Wallpapers/wallpaper.jpg"
chmod +x "$HOME/.fehbg" "$HOME/.screenlayout/monitors.sh" \
  "$HOME/.config/polybar/launch.sh" "$HOME/.config/polybar/network.sh" \
  "$HOME/.config/i3/scripts/lock.sh" "$HOME/.config/i3/scripts/blur-lock" \
  "$HOME/.config/i3/scripts/mouse-settings.sh" "$HOME/.config/i3/scripts/powermenu"
```

Replace the original username in installed paths.

```sh
python3 - <<'PYTHON'
from pathlib import Path
home = Path.home()
for name in ['.fehbg', '.config/polybar/config.ini', '.config/polybar/spacegray.ini']:
    path = home / name
    path.write_text(path.read_text().replace('/home/vano-iniashvili', str(home)))
PYTHON
```

## 3. Configure monitors

Run in an X11 session and use the reported output names, resolutions and rates.

```sh
xrandr --query
nano "$HOME/.screenlayout/monitors.sh"
```

Single-monitor example for the contents of `~/.screenlayout/monitors.sh`:

```sh
#!/bin/sh
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --pos 0x0 --rotate normal
```

Two-monitor example:

```sh
#!/bin/sh
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --pos 0x0 --rotate normal \
  --output DP-1 --mode 1920x1080 --rate 60 --pos 1920x0 --rotate normal
```

Save the same output names in all three locations.

| File | Set |
| --- | --- |
| `~/.screenlayout/monitors.sh` | Outputs, positions, modes, refresh rates |
| `~/.config/polybar/launch.sh` | `MONITOR="HDMI-1"` (chosen bar display) |
| `~/.config/i3/config` | Rofi `-monitor HDMI-1` and `workspace N output NAME` lines |

Original layout: HDMI-1-0 top-left, DVI-D-1-0 top-right, DP-2 bottom-left, HDMI-3 bottom-right; all 1080p, DP-2 at 60 Hz, others 74.97 Hz, right-column X position 1925.

## 4. Configure mouse

Choose the actual mouse interface and inspect its properties.

```sh
xinput list
mouse_name='YOUR EXACT MOUSE DEVICE NAME'
xinput list-props "$mouse_name"
xinput set-prop "$mouse_name" 'libinput Accel Speed' -0.5
xinput set-prop "$mouse_name" 'libinput Natural Scrolling Enabled' 0
# Adaptive acceleration (three-value property)
xinput set-prop "$mouse_name" 'libinput Accel Profile Enabled' 1 0 0
# Flat acceleration instead
# xinput set-prop "$mouse_name" 'libinput Accel Profile Enabled' 0 1 0
```

Speed ranges from -1 (slow) to 1 (fast); scrolling uses 0 (normal)/1 (natural); older two-value profiles use `1 0` (adaptive)/`0 1` (flat).

Save the chosen device name, speed, supported profile and scrolling values in the startup script.

```sh
nano "$HOME/.config/i3/scripts/mouse-settings.sh"
sh "$HOME/.config/i3/scripts/mouse-settings.sh"
```

## 5. Configure keyboard and appearance

Edit the installed files to save settings for this computer.

| Setting | File / original value |
| --- | --- |
| Keyboard | `~/.config/i3/config`: `us,ge`, `grp:win_space_toggle` |
| Modifier | `~/.config/i3/config`: `set $mod Mod1` (Alt) |
| Window font/borders/gaps | `~/.config/i3/config`: Noto Sans 10, borders 1, inner gaps 6, outer gaps 3 |
| DPI/cursor | `~/.Xresources`: DPI 84, cursor Adwaita 24 |
| Bar | `~/.config/polybar/spacegray.ini`: fonts, colors, height 20, modules |
| Rofi | `~/.config/rofi/config.rasi`, `~/.local/share/rofi/themes/` |
| Power menu | `~/.config/rofi/powermenu.rasi`: northeast, offsets -10/28 px |
| Notifications | `~/.config/dunst/dunstrc`: font, colors, Qogir icon paths |
| GTK | `~/.config/gtk-3.0/settings.ini`: Arc-Dark/Papirus-Dark; keep one `gtk-font-name` entry |
| Terminal | `~/.config/terminator/config` |
| Wallpaper | `~/Pictures/Wallpapers/wallpaper.jpg`, `~/.fehbg` |
| Custom lock | `~/.config/i3/scripts/lock.sh`, `~/.config/i3/lockscreen/blurred.png`; inactivity 10 seconds |

Apply settings in the current X11 session.

```sh
setxkbmap -layout 'us,ge' -option 'grp:win_space_toggle'
xrdb -merge "$HOME/.Xresources"
sh "$HOME/.screenlayout/monitors.sh"
sh "$HOME/.fehbg"
```

## 6. First login and keyboard

Copy the configuration before the first i3 login to skip its Enter/Esc configuration wizard.

```sh
i3 -C -c "$HOME/.config/i3/config"
```

**Log out → select your user → session/gear menu → i3 → log in**; repeat a full logout/login after changing startup commands.

Open a terminal with **Alt + Enter** or the launcher with **Alt + D**; if the wizard appears, return to your previous desktop and check `~/.config/i3/config`.

Physical keyboard support comes from `xserver-xorg-input-libinput`; for a clickable [on-screen keyboard](https://packages.ubuntu.com/onboard), install Onboard before switching sessions and add its startup line after copying the config.

```sh
sudo apt install onboard
printf '\nexec --no-startup-id onboard\n' >> "$HOME/.config/i3/config"
```

Onboard opens after i3 starts; it does not replace the login screen's own accessibility keyboard.

## Shortcuts

Alt is `$mod`; Super is the Windows/logo key; H/J/K/L mean left/down/up/right.

| Shortcut | Action |
| --- | --- |
| Alt + Enter | Open Terminator |
| Alt + D | Open Rofi application launcher |
| Alt + Shift + Q | Close focused window |
| Alt + H/J/K/L | Focus window left/down/up/right |
| Alt + arrow key | Focus window in that direction |
| Alt + semicolon | Focus right |
| Alt + Shift + H/J/K/L | Move window left/down/up/right |
| Alt + Shift + arrow key | Move window in that direction |
| Alt + Shift + semicolon | Move window right |
| Alt + Ctrl + H/J/K/L | Focus monitor left/down/up/right |
| Alt + Ctrl + Shift + H/J/K/L | Move focused window to another monitor |
| Alt + V | Set vertical split for subsequent windows |
| Alt + slash | Toggle split orientation |
| Alt + F | Toggle fullscreen |
| Alt + S or Alt + comma | Stacked layout |
| Alt + W | Tabbed layout |
| Alt + E | Toggle split layout |
| Alt + Shift + Space | Toggle focused window floating/tiling |
| Alt + Space | Switch focus between floating and tiling windows |
| Alt + A | Focus parent container |
| Alt + minus | Shrink width, configured as 50 px or 5 percentage points |
| Alt + equals | Grow width, configured as 50 px or 5 percentage points |
| Alt + R | Enter resize mode (see below) |
| Alt + Shift + C | Reload config; also relaunches Polybar via `exec_always` |
| Alt + Shift + R | Restart i3 in place |
| Alt + Shift + E | Show confirmation to exit i3/logout |
| Super + H | Hide focused window in scratchpad |
| Super + Shift + H | Open hidden-window picker; choose a window and press Enter |
| Super + L | Run custom lock screen |
| Super + Shift + S | Select screenshot region using Flameshot |
| Super + Space | Switch US/Georgian keyboard layout |
| Volume up/down keys | Change default output volume by 10% |
| Speaker mute key | Toggle default output mute |
| Microphone mute key | Toggle default microphone mute |
| Alt + left mouse drag | Move floating windows; drag tiling windows to rearrange |
| Alt + right mouse drag | Resize floating windows |

Resize mode: H/Left shrinks width, L/Right grows width, J/Down grows height, K/Up shrinks height (10 px or 10 percentage points); Enter/Esc/Alt + R exits.

Polybar: click the launcher, a hidden-window label to restore it, or the power icon; Rofi uses typing/arrows/Enter/Esc.

## Workspace keys (optional)

Number shortcuts are absent by default; append these to `~/.config/i3/config` for Alt + 1–4 switching and Alt + Shift + 1–4 moving windows.

```i3
bindsym $mod+1 workspace number 1
bindsym $mod+2 workspace number 2
bindsym $mod+3 workspace number 3
bindsym $mod+4 workspace number 4
bindsym $mod+Shift+1 move container to workspace number 1
bindsym $mod+Shift+2 move container to workspace number 2
bindsym $mod+Shift+3 move container to workspace number 3
bindsym $mod+Shift+4 move container to workspace number 4
```

## Useful commands

Run inside i3 after saving edits.

```sh
i3-msg reload
"$HOME/.config/polybar/launch.sh"
tail -n 50 "$HOME/.config/polybar/polybar.log"
i3-msg 'workspace number 1'
i3-msg 'move container to workspace number 2'
python3 "$HOME/.config/polybar/scratchpad.py" menu
"$HOME/.config/i3/scripts/powermenu"
pactl set-sink-volume @DEFAULT_SINK@ 50%
pactl set-sink-mute @DEFAULT_SINK@ toggle
```

Power-menu locking uses `blur-lock`; to match Super + L, prefer `"${HOME}/.config/i3/scripts/lock.sh"` in `LOCK_SCRIPTS` inside `~/.config/i3/scripts/powermenu`; suspend uses `xss-lock -- i3lock --nofork`.

## Optional legacy helpers

Install only when using the archived i3blocks configuration or extra helper scripts.

```sh
sudo apt install i3blocks sysstat lm-sensors acpi pavucontrol brightnessctl \
  libnotify-bin power-profiles-daemon curl jq yad perl iproute2
```

`keyhint` requires an EndeavourOS library; use `keyhint-2` for Rofi instead; keep weather credentials outside Git and leave `import-gsettings` unused to preserve GNOME preferences.

## Collection and credits

`collection-manifest.json` records original paths, permissions and SHA-256 hashes for 46 copied files; `archive/` contains inactive i3blocks settings.

Preserve upstream licenses/notices and verify image-sharing rights: [EndeavourOS](https://github.com/endeavouros-team/endeavouros-i3wm-setup), [audio switcher](https://gist.github.com/kbravh/1117a974f89cc53664e55823a55ac320), [volume/brightness](https://gitlab.com/Nmoleo/i3-volume-brightness-indicator), [i3blocks-contrib](https://github.com/vivien/i3blocks-contrib).

Reference: [i3 manual](https://i3wm.org/docs/userguide.html), [libinput properties](https://cgit.freedesktop.org/xorg/driver/xf86-input-libinput/tree/man/libinput.man).
