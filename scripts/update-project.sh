#!/bin/bash

cd ~/logi-back-py/
echo $PWD

echo "[>>] pulling updates"
git pull
git submodule update --init --force --remote

echo "[>>] update config"
cp config/config.py /var/www/
