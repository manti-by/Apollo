Apollo IoT App
====


About
----

Raspberry Pi app for monitoring

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/benjamin/

Requirements:

    Raspberry Pi, ESP8266, Soil Moisture + MCP3008 and DHT22 sensors


Setup
----

1. Install python pip
    
    $ sudo apt install python-pip sqlite3 supervisor
    
2. Install, create and activate virtualenv

    $ sudo pip install virtualenv
    
    $ virtualenv -p python3 --no-site-packages --prompt=ben- venv
    
    $ source venv/bin/activate
    
3. Clone sources and install pip packages
    
    $ mkdir benjamin && cd benjamin/

    $ git clone https://bitbucket.org/manti_by/benjamin.git src
    
    $ pip install -r src/app/requirements.txt
    
4. Run flask server under supervisor

    $ sudo ln -s /home/pi/benjamin/src/svctl.conf /etc/supervisorctl/conf.d/benjamin.conf
    
    $ sudo supervisorctl update
    
5. Install crontab for worker

    */5 * * * *    /home/pi/benjamin/venv/bin/python /home/pi/benjamin/src/app/worker.py


Notes
----

Install locally DHT library on non Raspberry Pi device
    
    $ pip install --install-option="--force-pi" Adafruit_DHT