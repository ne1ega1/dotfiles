## Run fastfetch as welcome message

#function fish_greeting
#    fastfetch
#end

## Set values
fish_add_path /home/jumanji/.spicetify

# Format man pages
set -x MANROFFOPT "-c"
set -x MANPAGER "sh -c 'col -bx | bat -l man -p'"

# Set settings for https://github.com/franciscolourenco/done
set -U __done_min_cmd_duration 10000
set -U __done_notification_urgency_level low

# Plasma
#set -gx GBM_BACKEND nvidia-drm
#set -gx __GLX_VENDOR_LIBRARY_NAME nvidia
#set -gx __GL_VRR_ALLOWED 1
#set -gx __GL_THREADED_OPTIMIZATIONS 0
#set -gx nvidia_anti_flicker true
#set -gx QT_QPA_PLATFORMTHEME qt5ct
#set -gx QT_AUTO_SCREEN_SCALE_FACTOR 1
#set -gx QT_WAYLAND_DISABLE_WINDOWDECORATION 1
#set -gx ELECTRON_OZONE_PLATFORM_HINT wayland
#set -gx ANKI_WAYLAND 1
#set -gx OBSIDIAN_USE_WAYLAND 1
#set -gx MOZ_ENABLE_WAYLAND 1
#set -gx WLR_NO_HARDWARE_CURSORS 1
#set -gx WLR_RENDERER_ALLOW_SOFTWARE 1
#set -gx WLR_DRM_NO_ATOMIC 1

## Enable Wayland support for different applications
if [ "$XDG_SESSION_TYPE" = "wayland" ]
    set -gx WAYLAND 1
    set -gx QT_QPA_PLATFORM 'wayland;xcb'
    set -gx GDK_BACKEND 'wayland,x11'
    set -gx MOZ_DBUS_REMOTE 1
    set -gx MOZ_ENABLE_WAYLAND 1
    set -gx _JAVA_AWT_WM_NONREPARENTING 1
    set -gx BEMENU_BACKEND wayland
    set -gx CLUTTER_BACKEND wayland
    set -gx ECORE_EVAS_ENGINE wayland_egl
    set -gx ELM_ENGINE wayland_egl
end

## Environment setup
# Apply .profile: use this to put fish compatible .profile stuff in
if test -f ~/.fish_profile
  source ~/.fish_profile
end

# Add ~/.local/bin to PATH
if test -d ~/.local/bin
    if not contains -- ~/.local/bin $PATH
        set -p PATH ~/.local/bin
    end
end

# Add depot_tools to PATH
if test -d ~/Applications/depot_tools
    if not contains -- ~/Applications/depot_tools $PATH
        set -p PATH ~/Applications/depot_tools
    end
end

## Functions
# Functions needed for !! and !$ https://github.com/oh-my-fish/plugin-bang-bang
function __history_previous_command
  switch (commandline -t)
  case "!"
    commandline -t $history[1]; commandline -f repaint
  case "*"
    commandline -i !
  end
end

function __history_previous_command_arguments
  switch (commandline -t)
  case "!"
    commandline -t ""
    commandline -f history-token-search-backward
  case "*"
    commandline -i '$'
  end
end

if [ "$fish_key_bindings" = fish_vi_key_bindings ];
  bind -Minsert ! __history_previous_command
  bind -Minsert '$' __history_previous_command_arguments
else
  bind ! __history_previous_command
  bind '$' __history_previous_command_arguments
end

# Fish command history
function history
    builtin history --show-time='%F %T '
end

function backup --argument filename
    cp $filename $filename.bak
end

# Copy DIR1 DIR2
function copy
    set count (count $argv | tr -d \n)
    if test "$count" = 2; and test -d "$argv[1]"
        set from (echo $argv[1] | trim-right /)
        set to (echo $argv[2])
        command cp -r $from $to
    else
        command cp $argv
    end
end


##### Useful aliases

# Replace ls with eza
alias ls='eza -al --color=always --group-directories-first --icons' # preferred listing
alias la='eza -a --color=always --group-directories-first --icons'  # all files and dirs
alias ll='eza -l --color=always --group-directories-first --icons'  # long format
alias lt='eza -aT --color=always --group-directories-first --icons' # tree listing
alias l.="eza -a | grep -e '^\.'"                                     # show only dotfiles

# Common use
alias unset='set --erase'
alias grubup="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias fixpacman="sudo rm /var/lib/pacman/db.lck"
alias tarnow='tar -acf '
alias untar='tar -zxvf '
alias wget='wget -c '
alias psmem='ps auxf | sort -nr -k 4'
alias psmem10='ps auxf | sort -nr -k 4 | head -10'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ......='cd ../../../../..'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias hw='hwinfo --short'                                   # Hardware Info
alias big="expac -H M '%m\t%n' | sort -h | nl"              # Sort installed packages according to size in MB
alias gitpkg='pacman -Q | grep -i "\-git" | wc -l'          # List amount of -git packages

# Get fastest mirrors
alias mirror="sudo cachyos-rate-mirrors"

# Help people new to Arch
alias apt='man pacman'
alias apt-get='man pacman'
alias please='sudo'
alias tb='nc termbin.com 9999'

# Cleanup orphaned packages
alias cleanup='sudo pacman -Rns (pacman -Qtdq)'

# Get the error messages from journalctl
alias jctl="journalctl -p 3 -xb"

# Recent installed packages
alias rip="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -200 | nl"

### Custom

alias gd='cd ~/Downloads'
alias gc='cd ~/.config'

# Work
alias lg='lazygit'
alias gl='git pull'
alias gb='git checkout'
alias d='sudo systemctl start docker.socket'
alias b='cd ~/etlsrc && make build/airflow && make build/crawlers && make build/parsers/base && make build/normalizers/base'
alias n='cd ~/etlsrc && make build/xporters/couchdb && make build/operators'
alias r='cd ~/etlsrc && make down && make clean && make up'
alias f='b && n && make up'

# VPN
alias m='sudo ip route add default via 10.31.0.1 dev tun0 metric 200 && sudo ip route del default dev tun0'
alias pt='sudo tailscale up --login-server https://hs.ptsecurity.com --accept-routes'
alias pt_off='tailscale down'
alias wg_on='sudo wg-quick up dimon_wg'
alias wg_off='sudo wg-quick down dimon_wg'

# Other
alias pixel='scrcpy --render-driver=software --window-height=1240 --window-title="Pixel 7" -e'

#cat ~/.cache/wal/sequences

[ "$(tty)" = /dev/tty1 ] && exec Hyprland

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH

function y
	set tmp (mktemp -t "yazi-cwd.XXXXXX")
	yazi $argv --cwd-file="$tmp"
	if set cwd (command cat -- "$tmp"); and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
		builtin cd -- "$cwd"
	end
	rm -f -- "$tmp"
end
