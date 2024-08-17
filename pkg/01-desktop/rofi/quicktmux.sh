#!/bin/bash

input=$(echo "" | rofi -dmenu -location 0 -theme-str 'listview {enabled:false;} window {width: 50%;}' -p "Name of new tmux session >")

if [ "$input" ]
then
  kitty tmux new-session -A -s $input
else
  exit 1
fi
