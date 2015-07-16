#!/usr/bin/env bash

apt-get update
apt-get install -y python3 python3-pip
pip3 install django==1.8
pip3 install --upgrade selenium
