#!/bin/bash

home="${PWD}/.."

# run
libo=$1

if [ ${#1} -eq 0 ]; then
    echo "./run.sh /path/to/libreoffice"
    echo "Trying /usr/lib/libreoffice..."
    libo="/usr/lib/libreoffice"
fi

# it wont run without this venv you have to copy this from libresign "1"
source env/bin/activate

export PYTHONPATH=$libo:'./libresign2'
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
export FLASK_APP=app.py
python3 -c "import main; main.setup()" "$@"
