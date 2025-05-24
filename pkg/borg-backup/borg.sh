#!/bin/bash

REPOSITORY=/mnt/seagate/stores/archives/hypernova-borg
PREFIX=hypernova
EXCL=~/bin/scripts/backups/excludes.txt
STATS=~/operational/logs/archive_stats.log
STATSPER=~/operational/logs/archive_stats-earlier.log
VENV=~/.virtualenvs/borg/bin
NOTIF=/home/iacus/.local/bin/ntfy
SND=/usr/share/sounds/freedesktop/stereo/message-new-instant.oga

# Enable venv
source $VENV/activate
export BORG_RELOCATED_REPO_ACCESS_IS_OK=yes
export BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes
export BORG_FILES_CACHE_SUFFIX=main
export BORG_FILES_CACHE_TTL=60

# Blinky
# curl "http://192.168.10.141:5000/pattern?pattern=backup"
#$NOTIF -t "Daily backup" send "Backup started"
notify-send -t 4000 Backup "Copia de seguridad iniciada" -a "Backup"

cp /etc/pkglist.txt ~/operational/logs/pkglist.txt

# # Backup
borg create --stats --verbose --exclude-caches --compression none      \
    --exclude-from $EXCL \
    $REPOSITORY::$PREFIX-{now:%Y-%m-%d.%H}      \
    ~/operational                \
    ~/repositories               \
    /mnt/internal/iacus/stores/heavy_repo          \
    /mnt/internal/iacus/bin/juegos/emuladores      \
    ~/bin/juegos/hdd/emuladores/ \
    ~/bin/juegos/if/             \
    ~/.config                    \
    ~/.local/etc                 \
    ~/.vim                       \
    ~/.task                      \
    ~/.task-project              \
    ~/.task-readlater            \
    ~/.timewarrior               \
    ~/.screenlayout              \
    ~/.themes                    \
    ~/.local/share/Rack2         \
    > $STATS 2>&1

# # Prune
borg prune -s -v --list                  \
    $REPOSITORY                          \
    --keep-daily=7                       \
    --keep-weekly=4                      \
    --keep-monthly=6                     \
    --keep-yearly=5                      \
    --glob-archives=$PREFIX* >> $STATS 2>&1

# Copy the log file so we can have a copy remain inside the backups too
cp $STATS $STATSPER

# Shutdown
# curl "http://192.168.10.141:5000/color?color=000000"
#$NOTIF -t "Daily backup" send "Backup complete"
notify-send -t 4000 Backup "Copia de seguridad finalizada" -a "Backup"
pw-play $SND

# date +"%Y-%m-%d (%H:%M:%S) - borg backup overriden" >> /cygdrive/d/data/logs/borg_stopped.log

