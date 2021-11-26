#/bin/bash

# Polybar conditional script that checks Taskwarrior if there are overdue tasks

OVERDUES=$(task +OVERDUE count)

if [ "$OVERDUES" = "0" ]; then
    exit 1
else
    exit 0
fi
