#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

export REMOTE_PATH='/home/pi/apollo'

header "Install system libraries"
sudo apt-get install -y git zip nginx supervisor postgresql
sudo apt-get install -y python-pip python-dev python-virtualenv build-essential \
    python-smbus python-numpy python-imaging libpq-dev libjpeg-dev libjpeg8-dev

header "Setup postgres database"
sudo -u postgres dropdb apollo
sudo -u postgres psql -c "CREATE DATABASE apollo;"
sudo -u postgres psql -c "CREATE USER apollo WITH PASSWORD 'pa55word';"
sudo -u postgres psql -c "ALTER ROLE apollo SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE apollo SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE apollo SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE apollo TO apollo;"

header "Clone sources and install app requirements"
git clone git@github.com:manti-by/Apollo.git $REMOTE_PATH
sudo pip install -r $REMOTE_PATH/server/requirements.txt
cp $REMOTE_PATH/server/apollo/settings/local.py.example $REMOTE_PATH/server/apollo/settings/local.py

header "Create log directory"
sudo mkdir /var/log/apollo/
sudo chown pi:pi /var/log/apollo/

header "Migrate, collect static files and create superuser"
sudo $REMOTE_PATH/server/manage.py migrate
sudo $REMOTE_PATH/server/manage.py collectstatic -v 0 --no-input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | sudo $REMOTE_PATH/server/manage.py shell

header "Update server configs and start it"
sudo ln -s $REMOTE_PATH/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
sudo service nginx restart

sudo ln -s $REMOTE_PATH/deploy/confs/supervisord.conf /etc/supervisor/conf.d/apollo.conf
sudo supervisorctl update
sudo supervisorctl start apollo

header "Add worker crontab"
echo "1/60 * * * *    /usr/bin/python /home/pi/apollo/server/manage.py worker" | sudo tee -a /var/spool/cron/crontabs/pi

header "All operations have done"