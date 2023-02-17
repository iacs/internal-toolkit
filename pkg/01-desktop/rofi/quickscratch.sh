#!/bin/bash
copy=$(xclip -o)
input=$(echo "" | rofi -dmenu -location 0 -theme-str 'listview {enabled:false;} window {width: 50%;}' -p "Enter note for scratchpad > " -filter $copy)

if [ "$input" ]
then
  jrnl sc "$input" && notify-send -u low "Added note" "$input" -a "Scratchpad"
else
  exit 1
fi
