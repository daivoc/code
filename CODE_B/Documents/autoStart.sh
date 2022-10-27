#!/bin/sh -e

# Create a file /etc/systemd/system/autoStart.service:
    [Unit]
    Description=ITS autoStart script
    [Service]
    ExecStart=/home/pi/autoStart.sh
    [Install]
    WantedBy=multi-user.target

# And script /path/to/autoStart.sh (don't forget to chmod +x it)
# Enable your service
    $ sudo systemctl enable autoStart


su pi -c 'cd /home/pi/MONITOR/ && /usr/bin/python run_IMS.pyc > /tmp/run_IMS.txt' &

# 우분투 18.04에서 rc.local 사용이 종료됨
# 대신 /etc/systemd/system/ 사용
# https://askubuntu.com/questions/1151080/how-do-i-run-a-script-as-sudo-at-boot-time-on-ubuntu-18-04-server

# ITS Auto start

# su pi -c 'cd /home/pi/common/ && /usr/bin/python systemConfig.pyc > /tmp/run_systemConfig.txt'
# su pi -c 'cd /home/pi/common/ && /usr/bin/python resetIP.pyc > /tmp/run_resetIP.txt' &

# su pi -c 'cd /home/pi/common/ && /usr/bin/python run_table.pyc > /tmp/run_table.txt' &
# su pi -c 'cd /home/pi/GPWIO/ && /usr/bin/python GPWIO.pyc > /tmp/run_GPWIO.txt' &
# su pi -c 'cd /home/pi/CAM/ && /usr/bin/python run_CAM.pyc > /tmp/run_CAM.txt' &
# su pi -c 'cd /home/pi/MONITOR/ && /usr/bin/python run_IMS.pyc > /tmp/run_IMS.txt' &
# su pi -c 'cd /home/pi/GPIO/ && /usr/bin/python run_GPIO.pyc > /tmp/run_GPIO.txt' &
# su pi -c 'cd /home/pi/optex_BSS/ && /usr/bin/python run_optex.pyc > /tmp/run_optexBSS.txt' &
# su pi -c 'cd /home/pi/optex_RLS_R/ && /usr/bin/python run_optex.pyc > /tmp/run_optexRLS_R.txt' &
# su pi -c 'cd /home/pi/optex_BSS_R/ && /usr/bin/python run_optex.pyc > /tmp/run_optexBSS_R.txt' &
# su pi -c 'cd /home/pi/optex_RLS/ && /usr/bin/python run_optex.pyc > /tmp/run_optexRLS.txt' &
# su pi -c 'cd /home/pi/optex_PARKING/ && /usr/bin/python run_optex.pyc > /tmp/run_optexPARKING.txt' &
# su pi -c 'cd /home/pi/optex_SPEED/ && /usr/bin/python run_optex.pyc > /tmp/run_optexSPEED.txt' &
# su pi -c 'cd /home/pi/SRF/ && /usr/bin/python spotter.pyc > /tmp/run_spotter.pyc.txt' &
## Port Forward
# sysctl -w net.ipv4.ip_forward=1 ## 포트포워딩 허용
# iptables -A FORWARD -i eth0 -j ACCEPT
# iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
# iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport 8443 -j DNAT --to-destination 169.254.254.254:443

exit 0