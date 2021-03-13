#!/usr/bin/env bash

pip install virtualenv
virtualenv .env

pip freeze > requirements.txt

pip install -r requirements.txt

source .env/bin/activate

py main.py
