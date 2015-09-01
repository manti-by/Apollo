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

    $ source application/bin/activate
    $ pip install -r application/requirements.txt

5. Install worker requirements:

    $ source worker/bin/activate
    $ pip install -r worker/requirements.txt

7. Run server:

    $ python app.py

8. Run worker:

    $ celery beat -A app