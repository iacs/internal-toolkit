#!/bin/sh

REPOSITORY=/mnt/seagate/stores/archives/hypernova-borg
PREFIX=hypernova
STATS=~/operational/logs/compaction.log
VENV=~/.virtualenvs/borg/bin
SND=/usr/share/sounds/freedesktop/stereo/message-new-instant.oga

set -e

. $VENV/activate
export BORG_RELOCATED_REPO_ACCESS_IS_OK
export BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes

notify-send -t 4000 Compaction "Compactación iniciada" -a "Backup"
pw-play $SND

borg compact -v $REPOSITORY > $STATS 2>&1 || exit 1

#notify-send -t 4000 Backup "Backup compact finished" -a "Backup"
notify-send -t 4000 "Compactación finalizada" "$(head -1 $STATS)" -a "Backup"

exit 0
