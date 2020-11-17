#!/bin/bash

#if [ ! -d "env" ]; then
#  #  does not exist
#  if [ ! -d "venv" ]; then
#    #  does not exist
#    echo 1
#  else
#    echo "activating VENV"
#    . venv/bin/activate
#  fi
#  echo 1
#else
#  echo "activating ENV"
#  . env/bin/activate
#fi

echo "[>>>] installing requirements"
pip install -r logi_web/requirements.txt

sudo systemctl stop logitab-web.service
sudo systemctl start logitab-web.service
sudo systemctl enable myapp.service
