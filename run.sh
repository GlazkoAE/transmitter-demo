#!/usr/bin/env bash

BASEDIR=$PWD
echo "Executing App in '$BASEDIR'"

source $BASEDIR/venv/bin/activate

sudo chmod 666 /dev/ttyUSB0

python3 main.py
