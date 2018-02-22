#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

LOCAL_PATH=$(dirname $(dirname $(pwd)))

header "Compiling new firmware"
make -f $LOCAL_PATH/client/Makefile

header "Deploying firmware to the client"
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 $LOCAL_PATH/client/firmware.hex

