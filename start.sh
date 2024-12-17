#!/usr/bin/env sh
# location of startup script: /etc/init.d/ethernettester
# command to test if x server is running: ps -e | grep X
sleep 10s
cd /home/philipp/EthernetTester || exit
/home/philipp/EthernetTester/.venv/bin/python main.py logfile &
