swayidle -w timeout 120 'swaylock' \
            resume 'hyprctl dispatch dpms on' \
            timeout 240 'systemctl suspend' \
            before-sleep 'swaylock' \
            lock 'swaylock' &
