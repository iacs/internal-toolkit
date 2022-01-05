#!/bin/bash

WN=$(date +%Y-W%V)
FILENAME=$WN.json
TIMEW_BIN=/usr/local/bin/timew
DIR=$1

$TIMEW_BIN export :week > $DIR/$FILENAME
