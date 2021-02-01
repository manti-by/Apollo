import glob
import logging.config
import os

import requests

from apollo.conf import (
    HELIOS_PASS,
    HELIOS_URL,
    HELIOS_USER,
    LOGGING,
    PHOTO_PATH,
    TOKEN_PATH,
)
from apollo.database import get_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def get_token():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as f:
            return f.read()
    response = requests.post(
        f"{HELIOS_URL}/api/v1/user/login/",
        json={"email": HELIOS_USER, "password": HELIOS_PASS},
        headers={"Content-Type": "application/json"},
    )
    if response.ok:
        token = response.json().get("token")
        with open(TOKEN_PATH, "w") as f:
            f.write(token)
        return token


def delete_token():
    return os.remove(TOKEN_PATH)


if __name__ == "__main__":
    token = get_token()
    if not token:
        logger.error("Can't retrieve token, please check helios credentials")
        exit(-1)

    response = requests.post(
        f"{HELIOS_URL}/api/v1/sensors/",
        json=get_sensors_data(),
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"}
    )
    if not response.ok:
        logger.error(f"Error when sending sensors data: {response.reason}")
        delete_token()
        exit(-1)

    list_of_files = glob.glob(f"{PHOTO_PATH}/*.jpg")
    if not list_of_files:
        logger.error(f"Can't find any files in {PHOTO_PATH}")
        exit(-1)

    latest_file = max(list_of_files, key=os.path.getctime)
    response = requests.post(
        f"{HELIOS_URL}/api/v1/sensors/photos/",
        files={"file": open(latest_file, "rb")},
        headers={"Authorization": f"Token {token}"}
    )
    if not response.ok:
        logger.error(f"Error when uploading photo: {response.reason}")
        delete_token()
        exit(-1)

    logger.info("Data is successfully uploaded to Helios server")
