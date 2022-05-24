#!/usr/bin/env bash

BASEDIR=$PWD
echo "Installing App in '$BASEDIR'"

if ! ([[ -d "$BASEDIR/venv" ]])
then
    echo "Creating a virtual environment ..."
    python3 -m venv $BASEDIR/venv
fi

source $BASEDIR/venv/bin/activate

$BASEDIR/venv/bin/pip install -r requirements.txt
