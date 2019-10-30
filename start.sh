#!/bin/bash

home="${PWD}/.."

# run
libo=$1

if [ ${#1} -eq 0 ]; then
    echo "./run.sh /path/to/libreoffice"
    echo "Trying /usr/lib/libreoffice..."
    libo="/usr/lib/libreoffice"
fi

source env/bin/activate

export PYTHONPATH=$libo:'./libresign2':'../irpjs'
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
python3 -c "import main; main.setup()" $@ --libresign-home $home
