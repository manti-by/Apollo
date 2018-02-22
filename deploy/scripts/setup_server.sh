#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

REMOTE_REMOTE = '/home/pi/apollo'

header "Install system libraries"
sudo apt-get install -y zip nginx supervisor postgresql
sudo apt-get install -y python-pip python-dev python-virtualenv libpq-dev libjpeg-dev libjpeg8-dev python-smbus

header "Setup postgres database"
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

header "Migrate, collect static files and create superuser"
$REMOTE_PATH/server/manage.py migrate
$REMOTE_PATH/server/manage.py collectstatic -v 0 --no-input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | $REMOTE_PATH/server/manage.py shell

header "Update server configs and start it"
sudo ln -s $REMOTE_PATH/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
sudo service nginx restart

sudo ln -s $REMOTE_PATH/src/deploy/confs/supervisor.conf /etc/supervisor/conf.d/apollo.conf
sudo supervisorctl update
sudo supervisorctl start apollo

header "Add worker crontab"
echo "1/60 * * * *    /usr/bin/python /home/pi/apollo/server/manage.py worker" | sudo tee -a /var/spool/cron/crontabs/pi

header "All operations have done"