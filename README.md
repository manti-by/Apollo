Apollo App
==========


Installation:
----------------------------------------------------------

1. Install system libraries:

        $ sudo apt-get install -y zip nginx supervisor postgresql python-pip python-dev python-virtualenv  libpq-dev python-smbus

2. Install and create virtualenv on RPI:

        $ sudo apt-get install -y python-virtualenv
        $ virtualenv --no-site-packages --prompt="apollo-venv-" venv 

3. Install worker requirements:

        $ source ~/venv/bin/activate
        $ pip install -r ~/apollo/src/app/requirements.txt

4. Migrate and run server:

        $ python ~/apollo/src/app/manage.py migrate
        $ python ~/apollo/src/app/manage.py runserver 0.0.0.0:8000

5. Add worker crontab:

        $ echo "1/60 * * * *    ~/venv/bin/python ~/apollo/src/app/manage.py worker" | tee -a /var/spool/cron/crontabs/pi
