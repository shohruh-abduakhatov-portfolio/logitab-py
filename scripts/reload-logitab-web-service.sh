# !/bin/bash

sudo cp ./logitab-web.service /lib/systemd/system/

sudo chmod 644 /lib/systemd/system/logitab-web.service
sudo systemctl daemon-reload
sudo systemctl stop logitab-web.service
sudo systemctl enable logitab-web.service
sudo systemctl start logitab-web.service