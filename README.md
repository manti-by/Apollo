Apollo App
==========


Installation:
-------------

1. Install system libraries:

        $ sudo apt-get install -y zip nginx supervisor postgresql python-pip python-dev python-virtualenv  libpq-dev python-smbus

2. Clone source and install app requirements:

        $ git clone git@bitbucket.org:manti_by/apollo.git ~/apollo/src/
        $ sudo pip install -r ~/apollo/src/app/requirements.txt

3. Migrate and run server:

        $ cd ~/apollo/src/app/
        $ python ./manage.py migrate
        $ python ./manage.py runserver 0.0.0.0:8000

4. Add worker crontab:

        $ echo "1/60 * * * *    ~/venv/bin/python ~/apollo/src/app/manage.py worker" | tee -a /var/spool/cron/crontabs/pi
