#!/bin/sh

vagrant ssh -c "cd /vagrant && sudo pip3 install -U -r requirements.txt && python3 server.py"
vagrant ssh -c "cd /vagrant && sudo pip3 install --upgrade pip3 && python3 server.py"
