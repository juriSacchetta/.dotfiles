#!/bin/sh
swayidle -w timeout 300 'systemctl --user start lock.service' timeout 450 'hyprctl dispatch dpms off' resume 'hyprctl dispatch dpms on' timeout 600 'systemctl suspend'
