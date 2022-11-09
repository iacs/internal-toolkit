#!/bin/bash

STUBFILE=$HOME/.greetme

FETCH=neofetch

determine_tod () {
  DATE=$( date +%H )
  if (( $DATE >=7 && $DATE < 12)); then
    TOD='morning'
  fi
  if (( $DATE >=12 && $DATE < 18)); then
    TOD='afternoon'
  fi
  if (( $DATE >=18 && $DATE < 24)); then
    TOD='night'
  fi
  if (( $DATE >=0 && $DATE < 7)); then
    TOD='late night'
  fi
}

if [[ -f "$STUBFILE" ]]; then
  determine_tod

  if command -v $FETCH &> /dev/null
  then
    $FETCH
  fi

  echo ""
  echo "Hello, $USER. Good $TOD."
  echo ""

  if command -v task &> /dev/null
  then
    echo "Here are your outstanding tasks as of today:"
    task next
  fi


  rm $STUBFILE
fi


