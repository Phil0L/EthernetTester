#!/usr/bin/env sh
# location of startup script: /etc/init.d/ethernettester
sleep 3s
cd /home/philipp/EthernetTester || exit
/home/philipp/EthernetTester/.venv/bin/python graphicstest.py 2
