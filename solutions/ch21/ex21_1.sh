#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
# from a machine on the management subnet
nmap -sS -p- pi-lab-01.local
# expected: only 22/tcp open
# from a machine outside the management subnet
nmap -sS -p 22,8000,11434 pi-lab-01.local
# expected: all filtered
