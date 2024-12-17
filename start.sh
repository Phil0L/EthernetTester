#!/usr/bin/env sh
# location of startup script: /etc/init.d/ethernettester
sleep 3s
cd ~/EthernetTester || exit
~/EthernetTester/.venv/bin/python graphicstest.py 2
