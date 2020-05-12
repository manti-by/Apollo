Apollo IoT App
====

[![Adafruit](https://img.shields.io/pypi/pyversions/Adafruit-MCP3008.svg)](https://github.com/adafruit/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/Apollo/master/LICENSE)  

About
----

Raspberry Pi monitoring app

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/Apollo/

Requirements:

- Raspberry Pi
- MCP3002 AD converter (v1 - MCP3008)
- Soil Moisture sensor
- Light sensor
- DHT22 sensor

First version
----

![Apollo](deploy/media/v1.jpg)

Second version
----

![Apollo](deploy/media/v2.jpg)

Setup Apollo application
----

1. Install python pip and lessc

        $ sudo apt install -y python-pip sqlite3 supervisor
        $ sudo npm install -g less

2. Install, create and activate virtualenv

        $ sudo pip install virtualenv
        $ virtualenv -p python3 --no-site-packages --prompt=apollo- venv
        $ source venv/bin/activate

3. Clone sources and install pip packages

        $ mkdir apollo/ && cd apollo/
        $ git clone https://github.com/manti-by/Apollo.git src
        $ pip install -r src/app/requirements.txt
    
4. Run flask server under supervisor

        $ sudo ln -s /home/pi/apollo/src/svctl.conf /etc/supervisorctl/conf.d/apollo.conf
        $ sudo supervisorctl update

5. Install crontabs

        */5 * * * *       /home/pi/apollo/venv/bin/python /home/pi/apollo/src/app/worker.py
        2-59/5 * * * *    raspistill -o /home/pi/images/$(date +\%Y-\%m-\%d_\%H-\%M-\%S).jpg
        0 * * * *         find /home/pi/images -name '*.jpg' -type f -mmin +480 -delete


Setup Helios application
----

1. Install python and necessary libraries

        $ sudo apt install -y build-essential ccache git zlib1g-dev python3.8 python3.8-dev \
            libncurses5:i386 libstdc++6:i386 zlib1g:i386 openjdk-8-jdk unzip ant ccache autoconf libtool libffi-dev


Notes
----

Install locally DHT library on non Raspberry Pi device

        $ pip install --install-option="--force-pi" Adafruit_DHT
