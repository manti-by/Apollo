Pibot App
==========================================================

Paspberry Pi App


Installation:
----------------------------------------------------------

1. Install system libraries:

    $ sudo apt-get install -y python-dev libmysqlclient-dev

2. Install and create virtualenv:

    $ sudo apt-get install -y python-virtualenv
    $ mkdir ~/venv && cd ~/venv

3. Create virtualenvs:

    $ virtualenv --no-site-packages application
    $ virtualenv --no-site-packages worker 

4. Install application requirements:

    $ source ~/venv/application/bin/activate
    $ pip install -r ~/pibot/application/requirements.txt

5. Install worker requirements:

    $ source ~/venv/worker/bin/activate
    $ pip install -r ~/pibot/worker/requirements.txt

6. Run server:

    $ python app.py

7. Add worker crontab:

    1/60 * * * *    ~/venv/worker/bin/python ~/pibot/worker/worker.py