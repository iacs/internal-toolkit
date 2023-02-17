#!/bin/bash

REPOSITORY=/mnt/seagate/stores/archives/supernova-borg
PREFIX=supernova
DATEFILE=/tmp/deg_$(date --rfc-3339=date).txt
STATS=~/operational/logs/degradation_stats.log
VENV=~/.virtualenvs/borg/bin

# Enable venv
source $VENV/activate
export BORG_RELOCATED_REPO_ACCESS_IS_OK=yes
export BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes

echo "ran $(date)" > $DATEFILE

notify-send -t 4000 Backup "Degradando repositorio anterior" -a "Backup"

# # Backup
borg create --stats --verbose --exclude-caches --compression none      \
    $REPOSITORY::$PREFIX-{now:%Y-%m-%d.%H}-deg      \
    $DATEFILE > $STATS 2>&1

# # Prune
borg prune -s -v --list                  \
    $REPOSITORY                          \
    --keep-daily=7                       \
    --keep-weekly=4                      \
    --keep-monthly=6                     \
    --keep-yearly=5                      \
    --glob-archives=$PREFIX* >> $STATS 2>&1


notify-send -t 4000 Backup "Degradación finalizada" -a "Backup"
