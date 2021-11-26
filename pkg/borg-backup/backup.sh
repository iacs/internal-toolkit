#!/bin/bash

REPOSITORY=~/stores/reponame
PREFIX=archivename
EXCL=~/path_to/excludes.txt
STATS=~/path_to/archive_stats.log
VENV=~/.python-venv/borg

source $VENV/bin/activate
# export BORG_RELOCATED_REPO_ACCESS_IS_OK
export BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes

notify-send -u low -t 4000 Backup "File backup has started"

# Backup
borg create --stats --verbose --compression none  \
    $REPOSITORY::$PREFIX-{now:%Y-%m-%d.%H}  \
    ~/.config           \
    ~/operational       \
    ~/repositories      \
    ~/stores/archive    \
    ~/templates         \
    --exclude-from $EXCL > $STATS 2>&1


# Prune
borg prune -s -v --list     \
    $REPOSITORY             \
    --keep-daily=7          \
    --keep-weekly=4         \
    --keep-monthly=6        \
    --keep-yearly=5         \
    --prefix=$PREFIX >> $STATS 2>&1

notify-send -u low -t 4000 Backup "File backup finished"
