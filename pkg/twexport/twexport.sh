#!/bin/bash

WN=$(date +%Y-W%V)
FILENAME=$WN.json
TIMEW_BIN=/usr/local/bin/timew
DIR=/mnt/d/operational/documents/tw_reports

$TIMEW_BIN export :week > $DIR/$FILENAME
