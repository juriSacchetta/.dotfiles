#!/bin/bash

# Check if exactly one argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi

# Access the first argument (in this case, it's $1)
arg=$1
echo $1
playerctl $arg
case $arg in
    "previous")
       ;;
    "play-pause")
      avizo-client --image-path="play-pause.png" --bar-bg-color=#848486
        ;;
    "next")
      playerctl next
        ;;
    *)
        echo "It's something else."
        ;;
esac

