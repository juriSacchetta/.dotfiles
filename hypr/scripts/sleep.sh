swayidle -w timeout 120 'wr-swaylock' \
            timeout 150 'hyprctl dispatch dpms off' \
            timeout 240 'systemctl suspend' \
            resume 'hyprctl dispatch dpms on' \
            before-sleep 'wr-swaylock' &
