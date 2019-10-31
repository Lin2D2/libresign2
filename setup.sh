#!/bin/bash

home="${PWD}/.."
args=("$@")

echo runn with ${args[0]}

if [[ ${args[1]} = "--help" ]]; then
    echo "--setup   to start setup"
    echo "--ignore if you want to not quit if the requirements are not satisfied"
    echo "    you may have to do this because the paths to check if th requirements are satisfied are not on all systems the same"
    echo ""
    echo "  more feathers are planned"
    exit
fi

if [[ ${args[1]} = "--setup" ]]; then
    echo "you are not in setup mode. In order to start setup: --setup or --help for more arguments"
    exit
fi

# TODO "apt-get install virtualenv python3-xdo python3-tk"
echo you have to run "apt-get install virtualenv python3-xdo python3-tk python3-uno"
REQUIERMENTS="True"

if [[ ! -d "/usr/bin/virtualenv" ]]; then
    echo you dont have virtualenv installed python3-uno
    REQUIERMENTS="False"
fi

if [[ ! -d "/usr/bin/xdotool" ]]; then
    echo you dont have xdotool installed
    REQUIERMENTS="False"
fi

if [[ ! -d "/usr/share/doc/python-tk" ]]; then
    echo you dont have python3-tk installed
    REQUIERMENTS="False"
fi

if [[ ! -d "/usr/share/doc/python3-uno" ]]; then
    echo you dont have python3-uno installed
    REQUIERMENTS="False"
fi

if [[ "$REQUIERMENTS" = "False" ]] || [[ ${args[1]} = "--ignore" ]]; then
    echo requirments not satisfied, quiting...
    exit
fi

if [[ ! -d "env" ]]; then
    echo "crearing virtual env: "
    virtualenv --system-site-packages -p python3 env
    echo "virtual env created, activating..."
    source env/bin/activate
    echo "installing packages: "
    pip3 install --force-reinstall Flask Pillow python-libxdo ipython gevent-websocket ifcfg qrcode
fi
