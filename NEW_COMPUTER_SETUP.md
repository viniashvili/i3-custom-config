# i3 desktop: shortcuts and new-computer setup

This repository is a copy of an Ubuntu i3/X11 desktop configuration: keyboard shortcuts, window layout, Spacegray Polybar, Rofi launcher and power menu, scratchpad window picker, notifications, lock-screen images, wallpaper, and terminal appearance. It contains configuration files, not the operating system or installed programs.

The instructions below configure a new computer with explicit, saved settings. Run setup commands on the **new computer**. Replace example device/output names with its actual hardware. The repository's original copies remain a reference.

## All configured shortcuts

**Alt** is the main modifier (`$mod = Mod1`). **Super** is the Windows/logo key (`Mod4`). H/J/K/L mean left/down/up/right. These tables describe active bindings in `config/i3/config`, not default i3 shortcuts that might be absent here.

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

In **resize mode**, H/Left shrinks width, L/Right grows width, J/Down grows height, and K/Up shrinks height, using 10 px or 10 percentage-point steps. Enter, Escape, or Alt + R returns to normal mode. Letter bindings outside this mode require Alt.

There are **no active Alt + number workspace shortcuts** in the collected configuration. The `$ws1`–`$ws10` variables alone do not create bindings. To switch without adding bindings:

```sh
i3-msg 'workspace number 1'
i3-msg 'move container to workspace number 2'
```

The active Polybar has an application-launcher icon, focused window title, clickable hidden-window labels, date/time, and a power icon. Click a hidden-window label to restore it. Click power for lock/logout/reboot/shutdown/suspend/hibernate; availability depends on the target machine. Rofi menus accept typing, arrows and Enter; Escape dismisses them. The active theme does not display workspace buttons.

## Step 1 — Install the desktop programs

Use an Ubuntu installation with a working X11 graphics driver. Keep an existing desktop session available while setting this up. From a terminal on the new computer:

```sh
sudo apt update
sudo apt install i3-wm i3status polybar rofi dunst terminator feh flameshot \
  dex xss-lock network-manager network-manager-gnome pulseaudio-utils \
  x11-xserver-utils x11-xkb-utils xinput python3 fontconfig \
  fonts-noto-core fonts-noto-color-emoji fonts-dejavu-core fonts-dejavu-mono \
  fonts-symbola arc-theme papirus-icon-theme scrot imagemagick
```

Package availability varies by Ubuntu release; resolve any unavailable package before continuing. The custom lock additionally requires an **i3lock-color-compatible** binary at `/usr/bin/i3lock`. A stock `i3lock` package may not support the saved color/clock flags. Check the installed implementation:

```sh
/usr/bin/i3lock --help 2>&1 | less
command -v magick
```

Verify support for options such as `--force-clock`, `--time-color`, and `--ring-color`. The power-menu screenshot locker needs the `magick` command (ImageMagick 7); an installation providing only `convert` needs the saved `blur-lock` script adapted to that command.

Install **Symbols Nerd Font Mono** separately for Polybar glyphs and **Qogir/Qogir-dark** icons for the saved Rofi/Dunst paths. Font binaries and system icon themes are not in this repository. After installing fonts:

```sh
fc-cache -f
fc-list : family | sort -u | less
```

See `README.md` for optional legacy-helper dependencies. The active desktop does not need the archived i3blocks configuration.

## Step 2 — Back up the destination and copy the files

Open a terminal in this repository's root on the new computer. Create a backup before overwriting existing settings:

```sh
backup_dir="$HOME/i3-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
for item in .config/i3 .config/polybar .config/rofi .config/dunst \
  .config/gtk-3.0/settings.ini .config/terminator/config \
  .local/share/rofi/themes .screenlayout/monitors.sh .fehbg .Xresources \
  Pictures/Wallpapers/wallpaper.jpg; do
  if [ -e "$HOME/$item" ] || [ -L "$HOME/$item" ]; then
    cp -a --parents "$HOME/./$item" "$backup_dir/"
  fi
done

mkdir -p "$HOME/.config" "$HOME/.local/share/rofi/themes" \
  "$HOME/.screenlayout" "$HOME/Pictures/Wallpapers"
cp -a config/i3 config/polybar config/rofi config/dunst "$HOME/.config/"
cp -a local/share/rofi/themes/. "$HOME/.local/share/rofi/themes/"
cp -a screenlayout/monitors.sh "$HOME/.screenlayout/monitors.sh"
cp -a home/.fehbg home/.Xresources "$HOME/"
cp -a assets/wallpaper.jpg "$HOME/Pictures/Wallpapers/wallpaper.jpg"
```

To also match terminal and GTK appearance (overwrites those saved settings):

```sh
mkdir -p "$HOME/.config/terminator" "$HOME/.config/gtk-3.0"
cp -a config/terminator/config "$HOME/.config/terminator/config"
cp -a config/gtk-3.0/settings.ini "$HOME/.config/gtk-3.0/settings.ini"
```

The remaining steps edit these **installed copies under your home directory** on the new computer. Leave `archive/` inactive.

## Step 3 — Replace the old home-directory paths

From the repository root, run this once after copying:

```sh
python3 - <<'PY'
from pathlib import Path
home = Path.home()
for relative in ['.fehbg', '.config/polybar/config.ini', '.config/polybar/spacegray.ini']:
    path = home / relative
    path.write_text(path.read_text().replace('/home/vano-iniashvili', str(home)))
PY
```

This saves your actual home path in wallpaper and power-menu commands.

## Step 4 — Save the new computer's monitor arrangement

In an X11 session, inspect output names and supported refresh rates:

```sh
xrandr --query
```

Edit `~/.screenlayout/monitors.sh` with one fixed command matching the target hardware. For example, a **single** monitor called `HDMI-1`:

```sh
#!/bin/sh
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --pos 0x0 --rotate normal
```

Two monitors, with `DP-1` to the right of `HDMI-1`:

```sh
#!/bin/sh
xrandr --output HDMI-1 --mode 1920x1080 --rate 60 --pos 0x0 --rotate normal \
       --output DP-1 --mode 1920x1080 --rate 60 --pos 1920x0 --rotate normal
```

Use only modes/rates reported by `xrandr`. Remove references to absent outputs. The original arrangement is four 1080p monitors: HDMI-1-0 top-left, DVI-D-1-0 top-right, DP-2 bottom-left, HDMI-3 bottom-right; right-hand X positions are 1925, leaving a 5-pixel gap.

Set these three places consistently:

| File | What to set |
| --- | --- |
| `~/.screenlayout/monitors.sh` | Output names, resolution, rate, position |
| `~/.config/polybar/launch.sh` | `MONITOR="HDMI-1"` (example: chosen bar display) |
| `~/.config/i3/config` | Rofi's `-monitor HDMI-1` and `workspace N output NAME` lines |

For a single monitor, replace the original four workspace assignment lines with `workspace 1 output HDMI-1`, or remove explicit assignments. For several monitors, assign each desired workspace to a real output. These lines select where a workspace opens; they do not add shortcuts or guarantee every workspace is already open.

Apply the layout after saving:

```sh
sh "$HOME/.screenlayout/monitors.sh"
```

## Step 5 — Save mouse sensitivity and scrolling

List input devices and inspect the actual mouse, avoiding its keyboard/consumer-control interfaces:

```sh
xinput list
mouse_name='YOUR EXACT MOUSE DEVICE NAME'
xinput list-props "$mouse_name"
```

Try a speed; libinput uses **-1 to 1** (slower to faster), with `0` the default. The original setting is `-0.5`:

```sh
xinput set-prop "$mouse_name" 'libinput Accel Speed' -0.5
xinput set-prop "$mouse_name" 'libinput Natural Scrolling Enabled' 0
```

Use `1` for natural/reversed scrolling. If the mouse exposes `libinput Accel Profile Enabled`, inspect how many values it has and which profiles are available. For the three-value property (adaptive, flat, custom):

```sh
# Adaptive acceleration: original behavior
xinput set-prop "$mouse_name" 'libinput Accel Profile Enabled' 1 0 0
# Or flat acceleration
xinput set-prop "$mouse_name" 'libinput Accel Profile Enabled' 0 1 0
```

For an older two-value property, use `1 0` or `0 1`. Set only supported properties/profiles. These commands change the current session. To persist them, edit **`~/.config/i3/scripts/mouse-settings.sh`**: replace the Xiaomi device name and save your chosen speed, profile and scrolling values there. i3 already runs that script at login. Reapply it after editing:

```sh
sh "$HOME/.config/i3/scripts/mouse-settings.sh"
```

A different mouse's hardware DPI can make the same `-0.5` feel different. No DPI-changing utility is included.

## Step 6 — Save keyboard, size, wallpaper and UI choices

| Setting | Installed file and edit |
| --- | --- |
| Keyboard languages | In `~/.config/i3/config`, keep/change `setxkbmap -layout "us,ge" -option "grp:win_space_toggle"` |
| Main modifier | Keep `set $mod Mod1` for documented Alt shortcuts; explicit `Mod4` shortcuts remain Super |
| UI scale/cursor | `~/.Xresources`: original `Xft.dpi: 84`, `Xcursor.size: 24`, `Xcursor.theme: Adwaita` |
| Window font/borders/gaps | `~/.config/i3/config`: Noto Sans 10, 1 px borders, inner gap 6, outer gap 3; font line occurs twice |
| Bar fonts/height/colors/modules | `~/.config/polybar/spacegray.ini`; current height 20 |
| Launcher theme | `~/.config/rofi/config.rasi` and `~/.local/share/rofi/themes/arc_dark_transparent_colors.rasi` |
| Power-menu placement | Final `window` block in `~/.config/rofi/powermenu.rasi`; currently northeast, offsets -10/28 px |
| Notifications | `~/.config/dunst/dunstrc`; replace Qogir icon paths if using another icon theme |
| GTK theme/icons | `~/.config/gtk-3.0/settings.ini`; Arc-Dark/Papirus-Dark |
| Terminal colors | `~/.config/terminator/config` |
| Desktop image | Replace `~/Pictures/Wallpapers/wallpaper.jpg` or edit `~/.fehbg` |
| Lock-screen image/timing | `~/.config/i3/lockscreen/blurred.png` and `~/.config/i3/scripts/lock.sh`; DPMS inactivity is 10 seconds |

Apply keyboard/DPI/wallpaper changes in the current X11 session:

```sh
setxkbmap -layout 'us,ge' -option 'grp:win_space_toggle'
xrdb -merge "$HOME/.Xresources"
sh "$HOME/.fehbg"
```

Some applications need reopening to pick up DPI/font changes. The GTK file contains two `gtk-font-name` entries; keep one chosen value if adjusting it. Do not run the saved `import-gsettings` helper unless you also intend to change GNOME interface preferences.

## Step 7 — Add workspace keys if you want them

This is an optional addition to the original configuration. Add to `~/.config/i3/config`:

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

Then Alt + 1–4 switches workspaces and Alt + Shift + 1–4 sends windows there. Extend the pattern if needed.

## Step 8 — Validate, log into i3, and check the result

```sh
i3 -C -c "$HOME/.config/i3/config"
```

Resolve any reported configuration errors, then log out and choose **i3** in the login screen's session selector. Complete a fresh login after changing startup commands: reload does not rerun ordinary `exec` lines, and an in-place i3 restart does not replace a fresh login for those commands.

Check Alt + Enter, Alt + D, monitor focus/movement, Super + Space, screenshot selection, and scratchpad hide/restore. Test Super + L once the custom lock implementation is installed. The power menu uses the separate screenshot-based `blur-lock`; suspend uses plain `i3lock` via xss-lock. To use the custom image/clock lock from the power menu, change its `LOCK_SCRIPTS` list in `~/.config/i3/scripts/powermenu` to prefer `"${HOME}/.config/i3/scripts/lock.sh"`.

Useful commands while tuning:

```sh
i3-msg reload
"$HOME/.config/polybar/launch.sh"
tail -n 50 "$HOME/.config/polybar/polybar.log"
python3 "$HOME/.config/polybar/scratchpad.py" menu
"$HOME/.config/i3/scripts/powermenu"
pactl set-sink-volume @DEFAULT_SINK@ 50%
pactl set-sink-mute @DEFAULT_SINK@ toggle
```

If copied executable bits were lost during transfer, restore only the launch scripts you need:

```sh
chmod +x "$HOME/.fehbg" "$HOME/.screenlayout/monitors.sh" \
  "$HOME/.config/polybar/launch.sh" "$HOME/.config/polybar/network.sh" \
  "$HOME/.config/i3/scripts/lock.sh" "$HOME/.config/i3/scripts/blur-lock" \
  "$HOME/.config/i3/scripts/mouse-settings.sh" "$HOME/.config/i3/scripts/powermenu"
```

The saved files now hold the target computer's static settings. Optional weather credentials belong outside the repository in `~/.config/openweather/config` or environment variables.

## References

Shortcut meanings, resize, workspace assignment and startup/reload behavior follow the [i3 User's Guide](https://i3wm.org/docs/userguide.html). Mouse property ranges and acceleration-profile ordering are documented in the [X.org libinput driver manual](https://cgit.freedesktop.org/xorg/driver/xf86-input-libinput/tree/man/libinput.man).
