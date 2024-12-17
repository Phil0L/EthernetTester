#!/usr/bin/env sh
# location of startup script: /etc/init.d/ethernettester
sleep 3s
cd /home/philipp/EthernetTester || exit
source .venv/bin/activate
python graphicstest.py 2
