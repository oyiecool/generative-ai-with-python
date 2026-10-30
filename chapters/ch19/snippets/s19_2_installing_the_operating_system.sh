#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
sudo apt update && sudo apt full-upgrade -y
sudo rpi-eeprom-update -a
sudo reboot
