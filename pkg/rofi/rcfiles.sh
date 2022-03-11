#!/usr/bin/env bash

source ~/.bashrc

RCDIR="$HOME/operational/scripts/rofi/rcfiles/"

pick="$(ls $RCDIR | rofi -dmenu -p "Select config file to edit")"
echo $pick

if [ "$pick" ]
then
    #$TERMINAL $EDITOR $RCDIR$pick
    kitty nvim $RCDIR$pick
else
    exit 1
fi
