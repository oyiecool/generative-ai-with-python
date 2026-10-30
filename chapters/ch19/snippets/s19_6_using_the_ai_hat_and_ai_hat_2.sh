#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
sudo apt install dkms
sudo apt install hailo-all        # AI HAT+ (Hailo-8 / Hailo-8L)
# or
sudo apt install hailo-h10-all    # AI HAT+ 2 (Hailo-10H)
sudo reboot
hailortcli fw-control identify    # confirms the accelerator is detected
