#!/bin/sh
ROOT_PATH="$(dirname "$(pwd)")"

DEFAULT_ENVIRONMENT="dev"
CURRENT_ENVIRONMENT=${1:-"echo $DEFAULT_ENVIRONMENT"}

echo "Install and create virtualenv"
sudo apt-get install -y python-virtualenv python-dev python3-dev
mkdir ~/venv && cd ~/venv
virtualenv --no-site-packages pibot
virtualenv -p python3 pibot
source pibot/bin/activate

echo "Install enviroments"
cd ROOT_PATH/worker
pip install -r requirements.txt
cd ROOT_PATH/application
pip install -r requirements.txt


