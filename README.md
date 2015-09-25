Apollo App
==========================================================

Paspberry Pi App


Installation:
----------------------------------------------------------

1. Install system libraries:

    $ sudo apt-get install -y python-dev libmysqlclient-dev

2. Install and create virtualenv on RPI:

    $ sudo apt-get install -y python-virtualenv
    $ mkdir ~/venv && cd ~/venv
    $ virtualenv --no-site-packages worker 

3. Install application GTK+ library:

    $ sudo add-apt-repository ppa:gnome3-team/gnome3
    $ sudo add-apt-repository ppa:gnome3-team/gnome3-staging
    $ sudo add-apt-repository ppa:ubuntuhandbook1/corebird

    $ sudo apt-get update
    $ sudo apt-get install corebird
    $ sudo add-apt-repository -r ppa:gnome3-team/gnome3-staging

4. Install worker requirements:

    $ source ~/venv/worker/bin/activate
    $ pip install -r ~/apollo/worker/requirements.txt

5. Run server:

    $ python ~/apollo/worker/app.py

6. Add worker crontab:

    1/60 * * * *    ~/venv/worker/bin/python ~/apollo/worker/worker.py
    
7. Run notifier:

    $ python ~/apollo/application/app.py