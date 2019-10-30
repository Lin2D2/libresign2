#!/bin/bash

home="${PWD}/.."

# TODO "apt-get install virtualenv python3-xdo python3-tk"
echo you have to run "apt-get install virtualenv python3-xdo python3-tk"
REQUIERMENTS=True

if [ ! -d "/usr/bin/virtualenv" ]; then
    echo you dont have virtualenv installed
    REQUIERMENTS=False
fi

if [ ! -d "/usr/bin/xdotool" ]; then
    echo you dont have xdotool installed
    REQUIERMENTS=False
fi

if [ ! -d "/usr/share/doc/python-tk" ]; then
    echo you dont have tkinter installed
    REQUIERMENTS=False
fi

if [ REQUIERMENTS==False ]; then
    echo requirments not satisfied, quiting...
    break
fi

if [ ! -d "env" ]; then
    echo "crearing virtual env: "
    virtualenv --system-site-packages -p python3 env
    echo "virtual env created, activating..."
    source env/bin/activate
    echo "installing packages: "
    pip3 install Flask Pillow python-libxdo ipython gevent-websocket ifcfg qrcode uno
fi
