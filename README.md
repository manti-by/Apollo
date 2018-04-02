Apollo IoT App
==============


Server setup (Raspberry Pi 3 Model B)
-------------------------------------

NOTE: You can simply run setup_server.sh on your Raspberry PI

1. Install libraries on the server

        $ sudo apt-get install -y git zip nmap nginx supervisor
        $ sudo apt-get install -y python3-pip python3-dev python3-virtualenv \
             python3-smbus libopenjp2-7-dev libatlas-base-dev


2. Clone sources, install app requirements and setup local config

        $ git clone git@github.com:manti-by/Apollo.git /home/pi/apollo/src/
        $ sudo pip install -r /home/pi/apollo/src/server/requirements.txt


3. Update server configs and start it

        $ sudo ln -s home/pi/apollo/src/deploy/confs/nginx.conf /etc/nginx/sites-enabled/apollo.conf
        $ sudo service nginx restart

        $ sudo ln -s home/pi/apollo/src/deploy/confs/supervisor.conf /etc/supervisor/conf.d/apollo.conf
        $ sudo supervisorctl update
        $ sudo supervisorctl start apollo


4. Add worker crontab

        $ echo "*/5 * * * *    /usr/bin/python3 /home/pi/apollo/src/server/worker.py" | sudo tee -a /var/spool/cron/crontabs/root
        $ echo "57 * * * *    /usr/bin/python3 /home/pi/apollo/src/server/scanner.py" | sudo tee -a /var/spool/cron/crontabs/root



Sensor Setup (ESP8266 + DNT22)
------------------------------

1. Install Arduino system libraries 

        $ sudo apt-get install arduino arduino-core arduino-mk


2. Clone sources, compile firmware and upload to Arduino 

        $ git clone git@github.com:manti-by/Apollo.git
        $ cd Apollo/client/
        $ make
        $ make upload
