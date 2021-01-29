import glob
import logging.config
import os

import requests

from apollo.conf import (HELIOS_PASS, HELIOS_URL, HELIOS_USER, LOGGING,
                         PHOTO_PATH)
from apollo.database import get_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    headers = {"Content-Type": "application/json"}
    data = {"email": HELIOS_USER, "password": HELIOS_PASS}
    response = requests.post(f"{HELIOS_URL}/api/sensors/", data=data, headers=headers)
    if not response.ok:
        logger.error("Can't login to Helios server")
        exit(response.status_code)

    headers["token"] = response.json().get("token")
    data = get_sensors_data()
    response = requests.post(f"{HELIOS_URL}/api/sensors/", data=data, headers=headers)
    if not response.ok:
        logger.error(f"Error when sending sensors data: {response.reason}")
        exit(response.status_code)

    headers["Content-Type"] = "multipart/form-data"
    list_of_files = glob.glob(f"{PHOTO_PATH}/*.jpg")
    if not list_of_files:
        logger.error(f"Can't find any files in {PHOTO_PATH}")
        exit(404)

    latest_file = max(list_of_files, key=os.path.getctime)
    files = {"file": open(latest_file, "rb")}
    response = requests.post(f"{HELIOS_URL}/api/sensors/photo/", files=files, headers=headers)
    if not response.ok:
        logger.error(f"Error when uploading photo: {response.reason}")
        exit(response.status_code)

    logger.info("Data is successfully uploaded to Helios server")
