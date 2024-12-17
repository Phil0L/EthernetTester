#!/usr/bin/env sh
# location of startup script: /etc/init.d/ethernettester
sleep 10s
cd /home/philipp/EthernetTester || exit
/home/philipp/EthernetTester/.venv/bin/python main.py logfile > log.txt
