#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

REMOTE_PATH='/home/pi/apollo'

header "Install system libraries"
sudo apt-get install -y git zip nmap nginx supervisor
sudo apt-get install -y python3-pip python3-dev python3-virtualenv python3-smbus libopenjp2-7-dev libatlas-base-dev

header "Setup database and sensors file"
touch $REMOTE_PATH/db.json
touch $REMOTE_PATH/sensors.json

header "Clone sources and install app requirements"
git clone git@github.com:manti-by/Apollo.git $REMOTE_PATH/src
sudo pip3 install -r $REMOTE_PATH/src/server/requirements.txt
cp $REMOTE_PATH/src/server/core/local.py.example $REMOTE_PATH/src/server/core/local.py

header "Update server configs and start it"
sudo ln -s $REMOTE_PATH/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
sudo service nginx restart

sudo ln -s $REMOTE_PATH/src/deploy/confs/supervisord.conf /etc/supervisor/conf.d/apollo.conf
sudo supervisorctl update
sudo supervisorctl start apollo

header "Add worker crontab"
echo "*/5 * * * *    /usr/bin/python3 /home/pi/apollo/server/worker.py" | sudo tee -a /var/spool/cron/crontabs/pi
echo "57 * * * *    /usr/bin/python3 /home/pi/apollo/server/scanner.py" | sudo tee -a /var/spool/cron/crontabs/pi

header "All operations have done"