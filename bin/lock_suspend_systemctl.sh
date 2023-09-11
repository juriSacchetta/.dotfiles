#!/bin/sh
#This scrit is based on systemctl, that arise some concurrent problem
swayidle -w timeout 120 'systemctl --user start lock.service'\
            timeout 180 'hyprctl dispatch dpms off'\
            resume 'hyprctl dispatch dpms on'\
            timeout 240 'systemctl suspend'\
            resume 'hyprctl dispatch dpms on'\
            before-sleep 'systemctl --user start lock.service'
