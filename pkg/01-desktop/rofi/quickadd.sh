#!/bin/bash

input=$(echo "" | rofi -dmenu -location 0 -theme-str 'listview {enabled:false;} window {width: 50%;}' -p "Enter task name > ")

if [ "$input" ]
then
  task add +inbox "$input" && notify-send -u low "Added task" "$input" -a "Quicktask"
else
  exit 1
fi
