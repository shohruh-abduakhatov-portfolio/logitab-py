# !/bin/bash

cp ./logitab-web.service /lib/systemd/system/

sudo chmod 644 /lib/systemd/system/logitab-web.service
sudo systemctl daemon-reload
sudo systemctl enable logitab-web.service
sudo systemctl start logitab-web.service
sudo systemctl status logitab-web.service