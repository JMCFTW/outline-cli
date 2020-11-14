#!/bin/bash

pip install -r requirements.txt
pip install flake8 coverage
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
mv example-app.ini app.ini
coverage run --source=./src/outline_cli/ -m unittest discover ./src/
coverage report -m
mv app.ini example-app.ini
rm .coverage
