# Ubuntu i3 desktop configuration

Snapshot of this machine's existing Ubuntu/X11 i3 setup, collected on 2026-11-15. All 46 collected files are independent, unmodified copies; collecting them did not change the live desktop. Original permissions are preserved. No installer has been run.

For the complete shortcut reference, mouse sensitivity commands, and ordered setup steps, see [New computer setup](NEW_COMPUTER_SETUP.md).

## Contents

| Repository path | Restore destination | Purpose |
| --- | --- | --- |
| `config/i3/` | `~/.config/i3/` | Window manager, helpers, lock-screen image |
| `config/polybar/` | `~/.config/polybar/` | Active Spacegray theme, alternate theme, launcher, scratchpad/network helpers |
| `config/rofi/` | `~/.config/rofi/` | Application launcher and menu themes |
| `local/share/rofi/themes/` | `~/.local/share/rofi/themes/` | Referenced Arc theme |
| `config/dunst/` | `~/.config/dunst/` | Notification settings |
| `config/gtk-3.0/settings.ini` | `~/.config/gtk-3.0/settings.ini` | Optional GTK appearance |
| `config/terminator/config` | `~/.config/terminator/config` | Optional terminal appearance |
| `screenlayout/monitors.sh` | `~/.screenlayout/monitors.sh` | Machine-specific monitor arrangement |
| `home/.fehbg`, `home/.Xresources` | `~/.fehbg`, `~/.Xresources` | Wallpaper restore, cursor and DPI settings |
| `assets/wallpaper.jpg` | `~/Pictures/Wallpapers/wallpaper.jpg` | Referenced wallpaper |
| `archive/i3/i3blocks.conf` | Optional: `~/.config/i3/i3blocks.conf` | Legacy bar; inactive in current i3 config |

`collection-manifest.json` records each original path (relative to home), destination, SHA-256 checksum, and permission mode. `I3_CONFIG_COLLECTION_GUIDE.md` is the original collection brief; actual collected configs take precedence over its expectations.

Backups, logs, caches, font binaries, credentials, third-party Git clones, and unrelated home files were excluded. Optional GTK4, GTK2, LXAppearance, Flameshot and fontconfig settings were absent. Existing customized Dunst, GTK3 and Terminator settings were included. No symlinks were encountered among collected files.

## Current behavior

`config/polybar/launch.sh` explicitly loads `spacegray.ini`, bar `main`, on **DP-2 only**. `config.ini` is an alternate theme. The active bar shows the launcher, focused window title, hidden windows, date/time and power button; several other modules are defined but disabled.

| Shortcut | Action |
| --- | --- |
| Alt + Return | Terminator |
| Alt + D | Rofi apps on DP-2 |
| Alt + H/J/K/L | Focus left/down/up/right |
| Alt + Shift + H/J/K/L | Move window |
| Alt + Ctrl + H/J/K/L | Focus another monitor |
| Alt + Ctrl + Shift + H/J/K/L | Move window to another monitor |
| Alt + R | Resize mode (H/J/K/L or arrows; Escape exits) |
| Super + H | Hide window in scratchpad |
| Super + Shift + H | Select/restore a hidden window |
| Super + L | Custom image/clock lock screen |
| Super + Shift + S | Flameshot selection |
| Super + Space | Switch US/Georgian keyboard layout |

The custom `lock.sh` sets DPMS to turn displays off after 10 seconds of inactivity, restoring prior DPMS settings on exit. The power menu instead prefers `blur-lock`, which captures and blurs a screenshot. Suspend locking uses the separate `xss-lock -- i3lock --nofork` startup command. These behaviors are preserved as found.

## Dependencies

These names come from the collected configs and scripts; install matching packages for the target distribution. This snapshot does not install software or pin an Ubuntu release.

- Main desktop: i3/i3-msg, Polybar, Rofi, Dunst, Terminator, feh, Flameshot, dex, xss-lock, nm-applet, NetworkManager/nmcli, Python 3 (standard library only for scratchpad), Bash and standard shell tools.
- X11 tools: xrandr, xrdb, xset (typically `x11-xserver-utils`); setxkbmap (`x11-xkb-utils`); xinput.
- Audio: `pactl` (typically `pulseaudio-utils`) with a compatible PulseAudio/PipeWire server; systemd commands are used by the power menu.
- Custom lock: **i3lock-color-compatible `/usr/bin/i3lock`**, supporting the flags in `lock.sh`. The installed dpkg record says i3lock 2.16-1, which alone does not establish support for those custom flags. The power-menu `blur-lock` additionally needs `scrot`, ImageMagick's `magick`, and `shred`.
- Appearance: Noto Sans, DejaVu Sans Mono, Symbols Nerd Font Mono; alternate bar also names DejaVu Sans and Symbola. GTK uses Arc-Dark/Papirus-Dark/Adwaita; Rofi/Dunst name Qogir or Qogir-dark. Install themes/fonts separately; no font binaries or system icon trees were copied. Rofi power menus disable icons, but Dunst has absolute Qogir icon paths.
- Optional/legacy helpers: i3blocks, Perl, `mpstat` (sysstat), sensors (lm-sensors), acpi, iproute2, pavucontrol, brightnessctl, notify-send, powerprofilesctl, curl/jq (weather), and pacmd for the older PulseAudio switching branch. Legacy i3blocks launchers also name Firefox and Thunar. `keyhint` needs Yad and an EndeavourOS-specific library; it is not portable as collected.

Locally reported versions at collection: i3 4.25.1, Polybar 3.7.2, Rofi 2.0.0, Dunst 1.12.2, feh 3.11.2, Terminator 2.1.5. These describe the source machine, not a tested minimum-version matrix.

## Adapt before restoring

Edit repository copies for your target machine before copying them into place:

1. Replace `/home/vano-iniashvili` in `home/.fehbg`, `config/polybar/config.ini`, and `config/polybar/spacegray.ini` with your home path or appropriate shell expansion. Original paths remain here for fidelity.
2. Update output names and modes in `screenlayout/monitors.sh`, i3 workspace assignments/Rofi monitor, and the Polybar launcher's `MONITOR`. The script uses HDMI-1-0 at 0x0, DVI-D-1-0 at 1925x0, DP-2 at 0x1080, HDMI-3 at 1925x1080. All are 1920x1080; DP-2 is 60 Hz, the others 74.97 Hz. DP-1/HDMI-2 are disabled. No output is marked primary by this script. GPU identities in the original guide were not independently verified.
3. Adjust the exact Xiaomi mouse device name and libinput values in `mouse-settings.sh`, keyboard layout in i3, and DPI (84)/cursor size (24) in `.Xresources`.
4. Install required fonts and themes or edit their names/paths. The optional `keyhint` references `/usr/share/endeavouros/scripts/eos-script-lib-yad`, which was not copied. Its `keyhint-2` sibling uses Rofi instead.
5. Keep weather credentials outside Git. `openweather` contains placeholders and reads `~/.config/openweather/config` or environment variables; that private configuration was not collected.

`import-gsettings` is retained among the helpers but is not called by the current i3 configuration. It changes GNOME interface preferences when run; leave it unused to preserve GNOME settings.

## Restore manually

First back up any existing destination files outside this repository. Review the target-specific edits above. From the repository root, copy only the components you intend to restore; the following commands overwrite matching destination files and do not delete unrelated files:

```sh
mkdir -p "$HOME/.config" "$HOME/.local/share/rofi/themes" \
  "$HOME/.screenlayout" "$HOME/Pictures/Wallpapers"
cp -a config/i3 config/polybar config/rofi config/dunst "$HOME/.config/"
cp -a local/share/rofi/themes/. "$HOME/.local/share/rofi/themes/"
cp -a screenlayout/monitors.sh "$HOME/.screenlayout/monitors.sh"
cp -a home/.fehbg home/.Xresources "$HOME/"
cp -a assets/wallpaper.jpg "$HOME/Pictures/Wallpapers/wallpaper.jpg"
```

Optionally copy GTK3 and Terminator settings to the destinations in the table. Leave `archive/` inactive unless intentionally restoring i3blocks. Check the installed i3 syntax with `i3 -C -c "$HOME/.config/i3/config"`. Log into the i3 X11 session to apply startup commands; an i3 reload does not rerun all `exec` lines. GNOME can remain available as a separate login session.

## Review and Git

Every copied file was compared byte-for-byte and by mode against its source. A text review found no embedded credentials; absolute home paths and upstream author credits remain. This collection was not activated or tested as a fresh desktop installation.

The scripts/themes retain upstream notices, including EndeavourOS sources and GPL notices. See [EndeavourOS i3 setup](https://github.com/endeavouros-team/endeavouros-i3wm-setup), [audio-device-switch](https://gist.github.com/kbravh/1117a974f89cc53664e55823a55ac320), [volume/brightness indicator](https://gitlab.com/Nmoleo/i3-volume-brightness-indicator), and [i3blocks-contrib](https://github.com/vivien/i3blocks-contrib). Wallpaper and lock-image provenance is not recorded; confirm redistribution rights before publishing them. No blanket license has been assigned to third-party content.

When ready, initialize Git here if needed, inspect `git status --short` and `git diff --cached`, then make the first commit. The collection process has not initialized, staged, committed, or pushed a repository.
