#!/bin/bash

apt install python3-pip
python3 -m venv ./ui-venv
source ./ui-venv/Scripts/activate
pip install requirements.txt
python3 main.py