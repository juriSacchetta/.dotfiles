swayidle -w timeout 120 'swaylock' \
            timeout 180 'hyprctl dispatch dpms off' \
            resume 'hyprctl dispatch dpms on' \
            timeout 240 'systemctl suspend' \
            resume 'hyprctl dispatch dpms on' \
            before-sleep 'swaylock' &
