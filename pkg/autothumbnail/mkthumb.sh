#!/bin/bash

# TODO Migrate to Python, parameterize

FONT=./CORESANSC-65BOLD.TTF
COLORA=LightCoral
COLORB=DarkSlateGray
OPACITY=0.8
BASEIMG=baseimg.png
START=1
END=5

# convert -size 280x720 gradient:$COLORA-$COLORB gradient.png
# convert -size 280x1080 gradient:red-blue gradient.png
    # -page +955+0 \( gradient.png -alpha set -background none -channel A -evaluate multiply $OPACITY +channel \) \

for i in $(seq -f "%02g" $START $END)
do

convert $BASEIMG \
    -page +955+0 \( -size 280x720 gradient:$COLORA-$COLORB -alpha set -background none -channel A -evaluate multiply $OPACITY +channel \) \
    -page +970+50 \( -stroke '#000C' -strokewidth 3 -fill white -font $FONT -pointsize 210 -gravity northwest label:$i \) \
    -layers flatten ${BASEIMG%.*}_$i.png

done
