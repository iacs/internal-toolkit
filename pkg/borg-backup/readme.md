Template for a periodic backup script using borg, ran by cron.
Sends notifications via notify-send on start and finish

Currently, must copy the script and configure the following env parameters:

    REPOSITORY
    PREFIX
    EXCL
    STATS
    VENV

In order for the notifications to show when ran by cron, it needs the following format:

    0 16 * * * XDG_RUNTIME_DIR=/run/user/$(id -u) /path_to/backup.sh
