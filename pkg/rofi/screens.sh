#!/usr/bin/env bash

LAYOUTDIR="$HOME/.screenlayout/"

pick="$(ls $LAYOUTDIR | rofi -dmenu -p "Change to saved layout")"

bash $LAYOUTDIR$pick
