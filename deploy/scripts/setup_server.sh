#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

REMOTE_REMOTE = '/home/pi/apollo'

header "Install system libraries"
sudo apt-get install -y git zip nmap nginx supervisor
sudo apt-get install -y python3-pip python3-dev python-virtualenv libpq-dev libjpeg-dev libjpeg8-dev python-smbus

header "Setup database and sensors file"
touch $REMOTE_REMOTE/db.json
touch $REMOTE_REMOTE/sensors.json

header "Clone sources and install app requirements"
# git clone git@github.com:manti-by/Apollo.git $REMOTE_PATH
sudo pip install -r $REMOTE_PATH/server/requirements.txt
cp $REMOTE_PATH/server/core/local.py.example $REMOTE_PATH/server/core/local.py

header "Update server configs and start it"
sudo ln -s $REMOTE_PATH/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
sudo service nginx restart

sudo ln -s $REMOTE_PATH/src/deploy/confs/supervisor.conf /etc/supervisor/conf.d/apollo.conf
sudo supervisorctl update
sudo supervisorctl start apollo

header "Add worker crontab"
echo "*/5 * * * *    /usr/bin/python3 /home/pi/apollo/server/worker" | sudo tee -a /var/spool/cron/crontabs/pi
echo "57 * * * *    /usr/bin/python3 /home/pi/apollo/server/scanner" | sudo tee -a /var/spool/cron/crontabs/pi

header "All operations have done"