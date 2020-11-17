# !/bin/bash

cp ../config/config.py /var/www/
rm var/www/__pycache__

sudo supervisorctl reread
sudo supervisorctl update
