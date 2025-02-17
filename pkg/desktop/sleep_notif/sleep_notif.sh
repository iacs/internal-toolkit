#!/bin/bash

set -e

for p in {0..100}
do
  notify-send -u critical --icon preferences-desktop-screensaver -a WARN -h "string:x-dunst-stack-tag:proglock" -h "int:value:${p}" "Sleep" "Screen will be locked in one minute"
  sleep 0.6
done
