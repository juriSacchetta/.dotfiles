#!/bin/sh
swayidle -w timeout 300 'systemctl --user start lock.service' timeout 600 'systemctl suspend'
