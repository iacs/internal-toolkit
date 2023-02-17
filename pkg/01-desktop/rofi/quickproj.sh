#!/bin/bash

input=$(echo "" | rofi -dmenu -location 0 -theme-str 'listview {enabled:false;} window {width: 50%;}' -p "Enter task for $WIP_PROJ > ")
echo $input
if [ "$input" ]
then
  task add +inbox project:$WIP_PROJ "$input" && notify-send -u low "Added to $WIP_PROJ:" "$input" -a "Quicktask"
else
  exit 1
fi
