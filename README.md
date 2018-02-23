Apollo IoT App
==============


Server setup (Raspberry Pi 3 Model B)
-------------------------------------

NOTE: You can simply run setup_server.sh on your Raspberry PI. Also, all commands running from sudo user because we
need full access to some system sockets to get data from sensors

1. Install libraries on the server

        $ sudo apt-get install -y git zip nginx supervisor postgresql
        $ sudo apt-get install -y python-pip python-dev python-virtualenv build-essential \
          python-smbus python-numpy python-imaging libpq-dev libjpeg-dev libjpeg8-dev


3. Setup postgres database

        $ sudo -u postgres psql -c "CREATE DATABASE apollo;"
        $ sudo -u postgres psql -c "CREATE USER apollo WITH PASSWORD 'pa55word';"
        $ sudo -u postgres psql -c "ALTER ROLE apollo SET client_encoding TO 'utf8';"
        $ sudo -u postgres psql -c "ALTER ROLE apollo SET default_transaction_isolation TO 'read committed';"
        $ sudo -u postgres psql -c "ALTER ROLE apollo SET timezone TO 'UTC';"
        $ sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE apollo TO apollo;"


3. Clone sources, install app requirements and setup local config

        $ git clone git@github.com:manti-by/Apollo.git /home/pi/apollo/
        $ sudo pip install -r /home/pi/apollo/server/requirements.txt
        $ cp /home/pi/apollo/server/apollo/settings/local.py.example /home/pi/apollo/server/apollo/settings/local.py

NOTE: If you have problem with installing some packages, try this command or something like

        $ sudo pip install uwsgi --index-url=https://pypi.python.org/simple/


4. Migrate and collect static files

        $ sudo /home/pi/apollo/server/manage.py migrate
        $ sudo /home/pi/apollo/server/manage.py collectstatic -v 0 --no-input
        $ echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | sudo /home/pi/apollo/server/manage.py shell


5. Update server configs and start it

        $ sudo ln -s home/pi/apollo/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
        $ sudo service nginx restart

        $ sudo ln -s home/pi/apollo/src/deploy/confs/supervisor.conf /etc/supervisor/conf.d/apollo.conf
        $ sudo supervisorctl update
        $ sudo supervisorctl start apollo


6. Add worker crontab

        $ echo "1/60 * * * *    /usr/bin/python /home/pi/apollo/server/manage.py worker" | sudo tee -a /var/spool/cron/crontabs/pi



Client Setup (Arduino Nano V3.0 ATmega328P)
-------------------------------------------

1. Install Arduino system libraries 

        $ sudo apt-get install arduino arduino-core arduino-mk


2. Clone sources, compile firmware and upload to Arduino 

        $ git clone git@github.com:manti-by/Apollo.git
        $ cd Apollo/client/
        $ make
        $ make upload